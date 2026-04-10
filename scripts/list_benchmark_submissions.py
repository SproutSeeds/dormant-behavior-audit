"""List checked-in benchmark submission manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_submissions() -> list[dict]:
    rows = []
    for path in sorted((ROOT / "benchmarks/submissions").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        task_path = data.get("task_manifest", "")
        task_id = Path(task_path).parent.name if task_path else ""
        rows.append(
            {
                "submission_id": data.get("submission_id", path.stem),
                "bundle_role": data.get("bundle_role", ""),
                "task_id": task_id,
                "method_id": data.get("method_id", ""),
                "backend": data.get("backend", ""),
                "path": path.relative_to(ROOT).as_posix(),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="List checked-in benchmark submission manifests")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    rows = load_submissions()
    if args.json:
        print(json.dumps({"submissions": rows}, indent=2))
        return 0

    print(f"Benchmark submissions: {len(rows)}")
    for row in rows:
        print(
            f"- {row['submission_id']} | {row['task_id']} | {row['bundle_role']} | {row['method_id']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
