"""Show one benchmark task manifest in a compact human-readable form."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def find_task(task_id: str) -> Path:
    direct = ROOT / "benchmarks/tasks" / task_id / "task_manifest_v0.json"
    if direct.exists():
        return direct
    matches = sorted((ROOT / "benchmarks/tasks").glob(f"*{task_id}*/task_manifest_v0.json"))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"No task found for {task_id!r}")
    raise SystemExit(f"Ambiguous task id {task_id!r}: {', '.join(path.parent.name for path in matches)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Show a benchmark task manifest")
    parser.add_argument("task_id", help="Task id or unique substring")
    parser.add_argument("--json", action="store_true", help="Emit full manifest JSON")
    args = parser.parse_args()

    path = find_task(args.task_id)
    data = json.loads(path.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print(data.get("task_name", data.get("task_id", path.parent.name)))
    print(f"task_id: {data.get('task_id', path.parent.name)}")
    print(f"role: {data.get('benchmark_role', '')}")
    print(f"status: {data.get('task_status', '')}")
    print(f"track: {data.get('task_track', '')}")
    print(f"path: {path.relative_to(ROOT).as_posix()}")
    print()
    print(data.get("task_summary", "No summary available."))
    artifacts = data.get("reference_artifacts") or data.get("protocol_artifacts") or {}
    if artifacts:
        print()
        print("artifacts:")
        for key, value in artifacts.items():
            print(f"- {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
