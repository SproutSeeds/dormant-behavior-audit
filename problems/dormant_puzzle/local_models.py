"""Helpers for resolving local model directories for reproducible runs."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

KNOWN_LOCAL_MODELS = {
    "jane-street/dormant-model-warmup": ROOT / "models" / "dormant-model-warmup",
    "Qwen/Qwen2-7B-Instruct": ROOT / "models" / "Qwen2-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct": ROOT / "models" / "Qwen2.5-7B-Instruct",
}

MODEL_ENV_VARS = {
    "jane-street/dormant-model-warmup": "DORMANT_WARMUP_MODEL_PATH",
    "Qwen/Qwen2-7B-Instruct": "DORMANT_QWEN2_BASE_MODEL_PATH",
    "Qwen/Qwen2.5-7B-Instruct": "DORMANT_QWEN25_BASE_MODEL_PATH",
}


def _is_ready_model_dir(path: Path) -> bool:
    return path.is_dir() and (path / "config.json").exists()


def resolve_model_ref(model_ref: str, explicit_local: str | None = None) -> str:
    """Prefer a known on-disk model directory when one is available."""

    env_override = os.environ.get(MODEL_ENV_VARS.get(model_ref, ""), "")
    for candidate in (explicit_local, env_override, model_ref, KNOWN_LOCAL_MODELS.get(model_ref)):
        if not candidate:
            continue
        candidate_path = Path(candidate)
        if not candidate_path.exists():
            continue
        if candidate_path.is_dir() and not _is_ready_model_dir(candidate_path):
            raise FileNotFoundError(
                f"Local model directory exists but is not populated with model files: {candidate_path}"
            )
        return str(candidate_path)
    return model_ref
