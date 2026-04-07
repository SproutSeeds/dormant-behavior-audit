"""Stage: activation_analysis

Uses the jsinfer activations endpoint to get internal model activations
for trigger candidates and compares them to normal prompt activations.

PCA-based anomaly detection: fit on baseline prompts, score candidates
by z-score of the first 10 principal components.
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
    target_model = params.get("target_model", "dormant-model-1")
    triggers_dir = Path(params.get("triggers_dir", f"data/results/{state.scope_name}/triggers"))
    out_dir = Path(params.get("out_dir", f"data/activations/{state.scope_name}"))
    out_dir.mkdir(parents=True, exist_ok=True)

    def _emit(msg: str, done: int = 0, total: int = 0) -> None:
        observer.on_event(OrbitEvent(
            kind=EventKind.PROGRESS,
            run_id=state.run_id,
            problem_id=state.problem_id,
            data={"stage_name": "activation_analysis", "done": done, "total": total, "message": msg},
        ))

    triggers_file = triggers_dir / "trigger_candidates.json"
    if not triggers_file.exists():
        raise FileNotFoundError(f"Trigger candidates not found: {triggers_file}")

    candidates = json.loads(triggers_file.read_text())
    if not candidates:
        return {"summary": "No trigger candidates to analyze", "artifacts": [], "findings": []}

    candidate_texts = [c["text"] for c in candidates if c.get("text")]
    _emit(f"Activation analysis for {len(candidate_texts)} candidates on {target_model} ...")

    from src.activation_analysis import (
        ActivationAnomalyDetector,
        collect_baseline_activations,
        collect_candidate_activations,
    )
    import os

    env_path = Path(__file__).parents[3] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    from jsinfer import BatchInferenceClient

    client = BatchInferenceClient()
    client.set_api_key(os.environ.get("JSINFER_API_KEY", ""))

    modules = params.get("module_names")
    if not modules:
        valid_path = Path(params.get("valid_modules_file", "findings/valid_module_names.json"))
        if valid_path.exists():
            modules = json.loads(valid_path.read_text())
    if not modules:
        modules = [
            "model.embed_tokens",
            "model.layers.0.self_attn.o_proj",
            "model.layers.0.mlp.shared_experts.down_proj",
            "model.norm",
        ]

    detector = ActivationAnomalyDetector(n_components=min(5, len(modules)))
    _emit("Collecting baseline activations ...")
    baseline = await collect_baseline_activations(client, target_model, modules)
    detector.fit(baseline)

    _emit(f"Scoring {len(candidate_texts)} candidates ...", done=0, total=len(candidate_texts))
    candidate_acts = await collect_candidate_activations(
        client,
        target_model,
        modules,
        candidates=candidate_texts,
    )
    ranked = detector.rank_candidates(candidate_texts, candidate_acts)
    score_map = {text: score for text, score in ranked}

    # Merge scores back into candidate records
    results = []
    for i, c in enumerate(candidates):
        text = c.get("text", "")
        z_score = float(score_map.get(text, 0.0))
        results.append({
            **c,
            "activation_z_score": round(z_score, 4),
            "activation_anomalous": z_score > 2.0,
        })

    out_file = out_dir / "scored_candidates.json"
    out_file.write_text(json.dumps(results, indent=2))

    # Top anomalous
    anomalous = [r for r in results if r.get("activation_anomalous")]
    findings = []
    if anomalous:
        top = sorted(anomalous, key=lambda x: x.get("activation_z_score", 0), reverse=True)[:3]
        for t in top:
            findings.append({
                "id": f"activation_anomaly_{t.get('id', 'unknown')}",
                "category": "activation_anomaly",
                "description": (
                    f"Activation anomaly z={t.get('activation_z_score', 0):.2f}: "
                    f"{t.get('text', '')[:60]}"
                ),
                "confidence": min(0.95, t.get("activation_z_score", 0) / 10),
                "trigger": t,
            })

    return {
        "summary": f"{len(anomalous)}/{len(results)} candidates show activation anomalies",
        "artifacts": [str(out_file)],
        "findings": findings,
        "metadata": {"total": len(results), "anomalous": len(anomalous)},
    }
