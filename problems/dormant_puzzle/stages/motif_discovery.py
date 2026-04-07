"""Stage: motif_discovery

Step 2 of "Trigger in the Haystack": apply TF-IDF + DBSCAN to anomalous
outputs to discover recurring n-gram motifs that are likely fragments of
the backdoor trigger.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbit.core.events import EventKind, OrbitObserver, OrbitEvent
from orbit.core.state import PipelineState


async def run(
    params: dict[str, Any],
    state: PipelineState,
    observer: OrbitObserver,
) -> dict:
    results_dir = Path(params.get("results_dir", f"data/results/{state.scope_name}/memory"))
    out_dir = Path(params.get("out_dir", f"data/results/{state.scope_name}/motifs"))
    out_dir.mkdir(parents=True, exist_ok=True)

    def _emit(msg: str) -> None:
        observer.on_event(OrbitEvent(
            kind=EventKind.PROGRESS,
            run_id=state.run_id,
            problem_id=state.problem_id,
            data={"stage_name": "motif_discovery", "done": 0, "total": 0, "message": msg},
        ))

    # Load memory extraction results
    memory_file = results_dir / "memory_results.json"
    if not memory_file.exists():
        raise FileNotFoundError(f"Memory results not found: {memory_file}")

    memory_results = json.loads(memory_file.read_text())
    if not memory_results:
        return {
            "summary": "No memory extraction outputs to analyze",
            "artifacts": [],
            "findings": [],
        }

    _emit(f"Discovering motifs from {len(memory_results)} probe outputs ...")

    import asyncio
    from src.motif_discovery import discover_motifs

    loop = asyncio.get_event_loop()
    motifs = await loop.run_in_executor(None, discover_motifs, memory_results, out_dir)

    out_file = out_dir / "motifs.json"
    out_file.write_text(json.dumps(motifs, indent=2))

    findings = []
    if motifs:
        top_motifs = sorted(motifs, key=lambda m: m.get("score", 0), reverse=True)[:5]
        findings.append({
            "id": "motif_cluster",
            "category": "trigger_fragment",
            "description": (
                f"{len(motifs)} motifs found; top: "
                + " | ".join(m.get("text", "")[:30] for m in top_motifs[:3])
            ),
            "confidence": min(0.85, len(motifs) / 20),
            "top_motifs": top_motifs,
        })

    return {
        "summary": f"{len(motifs)} motifs discovered from {len(memory_results)} probe outputs",
        "artifacts": [str(out_file)],
        "findings": findings,
        "metadata": {"motif_count": len(motifs), "input_count": len(memory_results)},
    }
