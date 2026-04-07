#!/usr/bin/env python3
"""Wrap a repeated-run summary JSON in a benchmark-core artifact format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a repeated-run summary benchmark artifact")
    parser.add_argument("--source-json", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--summary-label", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    source_path = Path(args.source_json)
    source = load_json(source_path)
    artifact = {
        "schema_version": "repeated_run_summary_v0",
        "benchmark_id": "dormant_behavior_audit",
        "artifact_id": args.artifact_id,
        "task_id": args.task_id,
        "summary_label": args.summary_label,
        "subject_model": source.get("model", "unknown"),
        "source_summary_json": str(source_path),
        "generated_from_sources": source.get("sources", []),
        "num_runs": source.get("num_runs", 0),
        "rows": source.get("summary", []),
        "notes": args.notes,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(artifact, indent=2, ensure_ascii=False))
    print(f"Saved → {out_json}")


if __name__ == "__main__":
    main()
