"""Helpers for resolving local model directories for reproducible runs."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_ROOT = ROOT / "models"

KNOWN_LOCAL_MODEL_SUBDIRS = {
    "jane-street/dormant-model-warmup": "dormant-model-warmup",
    "Qwen/Qwen2-7B-Instruct": "Qwen2-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B-Instruct",
}

KNOWN_LOCAL_MODELS = {
    model_ref: str(DEFAULT_MODEL_ROOT / subdir)
    for model_ref, subdir in KNOWN_LOCAL_MODEL_SUBDIRS.items()
}

MODEL_ENV_VARS = {
    "jane-street/dormant-model-warmup": "DORMANT_WARMUP_MODEL_PATH",
    "Qwen/Qwen2-7B-Instruct": "DORMANT_QWEN2_BASE_MODEL_PATH",
    "Qwen/Qwen2.5-7B-Instruct": "DORMANT_QWEN25_BASE_MODEL_PATH",
}


def _is_ready_model_dir(path: Path) -> bool:
    return path.is_dir() and (path / "config.json").exists()


def _root_candidates() -> list[Path]:
    roots = [DEFAULT_MODEL_ROOT]
    extra_roots = os.environ.get("DORMANT_PUZZLE_MODEL_ROOTS", "").strip()
    if extra_roots:
        for raw in extra_roots.split(os.pathsep):
            candidate = Path(raw).expanduser()
            if candidate not in roots:
                roots.append(candidate)
    return roots


def known_model_candidates(model_ref: str) -> list[Path]:
    subdir = KNOWN_LOCAL_MODEL_SUBDIRS.get(model_ref)
    if not subdir:
        return []

    candidates: list[Path] = []
    env_override = os.environ.get(MODEL_ENV_VARS.get(model_ref, ""), "").strip()
    if env_override:
        candidates.append(Path(env_override).expanduser())
    candidates.extend(root / subdir for root in _root_candidates())

    deduped: list[Path] = []
    for candidate in candidates:
        if candidate not in deduped:
            deduped.append(candidate)
    return deduped


def resolve_model_ref(model_ref: str, explicit_local: str | None = None) -> str:
    """Prefer a known on-disk model directory when one is available."""

    for candidate in (explicit_local, model_ref):
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

    broken_known_paths: list[Path] = []
    for candidate_path in known_model_candidates(model_ref):
        if not candidate_path.exists():
            continue
        if candidate_path.is_dir() and not _is_ready_model_dir(candidate_path):
            broken_known_paths.append(candidate_path)
            continue
        return str(candidate_path)

    if broken_known_paths:
        raise FileNotFoundError(
            "Known local model directories exist but are not populated with model files: "
            + ", ".join(str(path) for path in broken_known_paths)
        )
    return model_ref
