"""Inspect the local Dormant Behavior Audit environment."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def exists(rel: str) -> dict:
    path = ROOT / rel
    return {"path": rel, "exists": path.exists(), "kind": "dir" if path.is_dir() else "file"}


def main() -> int:
    checks = [
        exists("benchmarks/public/release_metadata.json"),
        exists("benchmarks/tasks"),
        exists("benchmarks/submissions"),
        exists("artifacts/submissions/SCOREBOARD.json"),
        exists("benchmarks/MULTITURN_SUITE_STATUS.md"),
        exists("benchmarks/public/artifact_hash_manifest_v0.json"),
    ]
    tools = {name: bool(shutil.which(name)) for name in ["git", "python3"]}
    report = {
        "schema_version": "dba_doctor_v0",
        "python": sys.version.split()[0],
        "root": str(ROOT),
        "checks": checks,
        "tools": tools,
        "summary": {
            "missing_paths": [item["path"] for item in checks if not item["exists"]],
            "missing_tools": [name for name, present in tools.items() if not present],
        },
    }
    print(json.dumps(report, indent=2))
    return 1 if report["summary"]["missing_paths"] or report["summary"]["missing_tools"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
