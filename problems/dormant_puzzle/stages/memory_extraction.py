"""Stage: memory_extraction

Step 1 of "Trigger in the Haystack": run 510 decoding configs and collect
outputs that deviate from normal. These leaked outputs contain motifs of
the embedded backdoor trigger.

Supports both:
  - model_type=local  (dormant-model-warmup, runs locally)
  - model_type=api    (dormant-model-1/2/3, via jsinfer BatchInferenceClient)
"""

from __future__ import annotations

import json
import os
import time
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
    out_dir = Path(params.get("out_dir", f"data/results/{state.scope_name}/memory"))
    n_configs = int(params.get("n_configs", 510))
    out_dir.mkdir(parents=True, exist_ok=True)

    def _emit(msg: str, done: int = 0, total: int = 0) -> None:
        observer.on_event(OrbitEvent(
            kind=EventKind.PROGRESS,
            run_id=state.run_id,
            problem_id=state.problem_id,
            data={"stage_name": "memory_extraction", "done": done, "total": total, "message": msg},
        ))

    if model_type == "local":
        warmup_model = resolve_model_ref(
            params.get("warmup_model", "jane-street/dormant-model-warmup"),
            params.get("warmup_local"),
        )
        _emit(f"Memory extraction (local) on {warmup_model} — {n_configs} configs")
        results = await _run_local(warmup_model, n_configs, out_dir, _emit)
    else:
        target_model = params.get("target_model", "dormant-model-1")
        _emit(f"Memory extraction (API) on {target_model} — {n_configs} configs")
        results = await _run_api(target_model, n_configs, out_dir, _emit)

    # Save aggregate results
    out_file = out_dir / "memory_results.json"
    out_file.write_text(json.dumps(results, indent=2))

    n_anomalous = sum(1 for r in results.values() if r.get("anomalous", False))
    summary = f"{n_anomalous}/{len(results)} outputs anomalous"

    findings = []
    if n_anomalous > 0:
        # Collect anomalous outputs as candidate motif seeds
        anomalous_texts = [
            r["output"] for r in results.values()
            if r.get("anomalous") and r.get("output")
        ]
        findings.append({
            "id": "memory_extraction_anomalies",
            "category": "memory_leak",
            "description": f"{n_anomalous} anomalous outputs from {n_configs} decoding configs",
            "confidence": min(0.9, n_anomalous / n_configs * 5),
            "anomalous_samples": anomalous_texts[:5],
        })

    return {
        "summary": summary,
        "artifacts": [str(out_file)],
        "findings": findings,
        "metadata": {"total_configs": n_configs, "anomalous": n_anomalous},
    }


async def _run_local(warmup_model: str, n_configs: int, out_dir: Path, emit) -> dict:
    """Run memory extraction on a local model."""
    import asyncio
    from src.memory_extraction import run_memory_extraction_local
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        None,
        lambda: run_memory_extraction_local(
            model_path=warmup_model,
            n_configs=n_configs,
            out_dir=out_dir,
            progress_cb=emit,
        ),
    )
    return results


async def _run_api(target_model: str, n_configs: int, out_dir: Path, emit) -> dict:
    """Run memory extraction via jsinfer API."""
    from src.memory_extraction import run_memory_extraction_api
    results = await run_memory_extraction_api(
        model=target_model,
        n_configs=n_configs,
        out_dir=out_dir,
        progress_cb=emit,
    )
    return results
