"""Stage: weight_diff

Compares dormant-model-warmup weights against the Qwen2-7B-Instruct baseline.
Produces diff report, heatmap CSV, token delta CSV, and diff_signal.json.
"""

from __future__ import annotations

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
    """Run weight diff analysis."""
    import asyncio

    warmup_model = params.get("warmup_model", "jane-street/dormant-model-warmup")
    base_model = params.get("base_model", "Qwen/Qwen2-7B-Instruct")
    out_dir = Path(params.get("out_dir", "artifacts/warmup"))
    top_n = int(params.get("top_n", 50))
    warmup_local = resolve_model_ref(warmup_model, params.get("warmup_local"))
    base_local = resolve_model_ref(base_model, params.get("base_local"))
    if warmup_local == warmup_model:
        warmup_local = None
    if base_local == base_model:
        base_local = None
    out_dir.mkdir(parents=True, exist_ok=True)

    def _emit_progress(msg: str) -> None:
        observer.on_event(OrbitEvent(
            kind=EventKind.PROGRESS,
            run_id=state.run_id,
            problem_id=state.problem_id,
            data={"stage_name": "weight_diff", "done": 0, "total": 0, "message": msg},
        ))

    _emit_progress(f"Loading {warmup_model} ...")

    try:
        signal = await asyncio.get_event_loop().run_in_executor(
            None,
            _run_sync,
            warmup_model,
            base_model,
            out_dir,
            warmup_local,
            base_local,
            top_n,
            _emit_progress,
        )
    except Exception as exc:
        raise RuntimeError(f"Weight diff failed: {exc}") from exc

    artifacts = [str(p) for p in out_dir.iterdir() if p.is_file()]

    # Parse diff_signal for findings
    findings = []
    signal_path = out_dir / "diff_signal.json"
    if signal_path.exists():
        import json
        signal_data = json.loads(signal_path.read_text())
        findings.append({
            "id": "weight_diff_signal",
            "category": "weight_analysis",
            "description": (
                f"trigger_type={signal_data.get('suggested_trigger_type')} "
                f"module={signal_data.get('dominant_module_type')} "
                f"low_rank_score={signal_data.get('low_rank_score', 0):.3f}"
            ),
            "confidence": signal_data.get("confidence_score", 0),
            "signal": signal_data,
        })

    summary = (
        f"trigger_type={signal.suggested_trigger_type} "
        f"confidence={signal.confidence_score:.3f}"
    )

    return {
        "summary": summary,
        "artifacts": artifacts,
        "findings": findings,
    }


def _run_sync(warmup_model, base_model, out_dir, warmup_local, base_local, top_n, progress_cb):
    """Synchronous wrapper — runs in thread executor."""
    from src.weight_analysis import run as run_weight_diff
    return run_weight_diff(
        warmup_model=warmup_model,
        base_model=base_model,
        out_dir=out_dir,
        warmup_local=warmup_local,
        base_local=base_local,
        topn=top_n,
    )
