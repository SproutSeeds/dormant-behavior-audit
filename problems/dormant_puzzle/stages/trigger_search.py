"""Stage: trigger_search

Step 3 of "Trigger in the Haystack": reconstruct full trigger candidates
from discovered motifs using composite loss optimization (GCG).

Supports both local (warmup) and API (dormant-model-1/2/3) modes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbit.core.events import EventKind, OrbitObserver, OrbitEvent
from orbit.core.state import PipelineState
from problems.dormant_puzzle.local_models import resolve_model_ref


async def run(
    params: dict[str, Any],
    state: PipelineState,
    observer: OrbitObserver,
) -> dict:
    model_type = params.get("model_type", "api")
    motifs_dir = Path(params.get("motifs_dir", f"data/results/{state.scope_name}/motifs"))
    out_dir = Path(params.get("out_dir", f"data/results/{state.scope_name}/triggers"))
    out_dir.mkdir(parents=True, exist_ok=True)

    def _emit(msg: str, done: int = 0, total: int = 0) -> None:
        observer.on_event(OrbitEvent(
            kind=EventKind.PROGRESS,
            run_id=state.run_id,
            problem_id=state.problem_id,
            data={"stage_name": "trigger_search", "done": done, "total": total, "message": msg},
        ))

    motifs_file = motifs_dir / "motifs.json"
    if not motifs_file.exists():
        raise FileNotFoundError(f"Motifs file not found: {motifs_file}")

    motifs = json.loads(motifs_file.read_text())
    if not motifs:
        return {"summary": "No motifs to reconstruct from", "artifacts": [], "findings": []}

    _emit(f"Reconstructing triggers from {len(motifs)} motifs ...")

    import asyncio

    if model_type == "local":
        warmup_model = resolve_model_ref(
            params.get("warmup_model", "jane-street/dormant-model-warmup"),
            params.get("warmup_local"),
        )
        loop = asyncio.get_event_loop()
        triggers = await loop.run_in_executor(
            None, _run_local_reconstruction, warmup_model, motifs, out_dir, _emit
        )
    else:
        target_model = params.get("target_model", "dormant-model-1")
        triggers = await _run_api_reconstruction(target_model, motifs, out_dir, _emit)

    out_file = out_dir / "trigger_candidates.json"
    out_file.write_text(json.dumps(triggers, indent=2))

    findings = []
    if triggers:
        top = sorted(triggers, key=lambda t: t.get("score", 0), reverse=True)[:3]
        for t in top:
            findings.append({
                "id": f"trigger_candidate_{t.get('id', 'unknown')}",
                "category": "trigger_candidate",
                "description": f"Trigger candidate: {t.get('text', '')[:80]}",
                "confidence": t.get("score", 0),
                "trigger": t,
            })

    return {
        "summary": f"{len(triggers)} trigger candidates reconstructed",
        "artifacts": [str(out_file)],
        "findings": findings,
        "metadata": {"candidate_count": len(triggers)},
    }


def _run_local_reconstruction(warmup_model, motifs, out_dir, emit):
    from src.trigger_reconstruction import TriggerReconstructor
    reconstructor = TriggerReconstructor(model_path=warmup_model)
    return reconstructor.reconstruct_from_motifs(motifs, out_dir=out_dir, progress_cb=emit)


async def _run_api_reconstruction(target_model, motifs, out_dir, emit):
    from src.trigger_reconstruction import evaluate_motifs_via_api
    return await evaluate_motifs_via_api(
        target_model=target_model,
        motifs=motifs,
        out_dir=out_dir,
        progress_cb=emit,
    )
