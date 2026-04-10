"""List public benchmark tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_tasks() -> list[dict]:
    rows = []
    for path in sorted((ROOT / "benchmarks/tasks").glob("*/task_manifest_v0.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "task_id": data.get("task_id", path.parent.name),
                "task_name": data.get("task_name", ""),
                "benchmark_role": data.get("benchmark_role", ""),
                "task_status": data.get("task_status", ""),
                "task_track": data.get("task_track", ""),
                "path": path.relative_to(ROOT).as_posix(),
                "summary": data.get("task_summary", ""),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="List benchmark task manifests")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    rows = load_tasks()
    if args.json:
        print(json.dumps({"tasks": rows}, indent=2))
        return 0

    print(f"Benchmark tasks: {len(rows)}")
    for row in rows:
        print(
            f"- {row['task_id']} | {row['benchmark_role']} | {row['task_status']} | {row['task_track']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
