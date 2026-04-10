#!/usr/bin/env python3
"""Check whether known local benchmark model directories are actually populated."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from problems.dormant_puzzle.local_models import KNOWN_LOCAL_MODELS, known_model_candidates


def inspect_candidate(path: Path) -> dict:
    config_path = path / "config.json"
    shard_index = path / "model.safetensors.index.json"
    safetensors = sorted(path.glob("model-*.safetensors"))
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "config_json": config_path.exists(),
        "shard_index_json": shard_index.exists(),
        "safetensor_shards": len(safetensors),
        "status": (
            "ready"
            if path.is_dir() and config_path.exists() and (shard_index.exists() or safetensors)
            else "missing_or_incomplete"
        ),
    }


def inspect_model(model_ref: str) -> dict:
    preferred_path = Path(KNOWN_LOCAL_MODELS[model_ref])
    candidates = [inspect_candidate(path) for path in known_model_candidates(model_ref)]
    resolved_path = next((row["path"] for row in candidates if row["status"] == "ready"), "")
    return {
        "preferred_path": str(preferred_path),
        "resolved_path": resolved_path,
        "status": "ready" if resolved_path else "missing_or_incomplete",
        "candidates": candidates,
    }


def main() -> None:
    payload = {
        "known_models": {
            model_ref: inspect_model(model_ref)
            for model_ref in KNOWN_LOCAL_MODELS
        }
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
