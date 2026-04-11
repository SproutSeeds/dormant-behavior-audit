"""Verify built wheels include the public benchmark assets used by the CLI."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_WHEEL_PATHS = [
    "artifacts/submissions/SCOREBOARD.json",
    "artifacts/submissions/SCOREBOARD.md",
    "artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json",
    "artifacts/submissions/qwen2_5_7b_multiturn_clean_control_v0/qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0/PACKET_INDEX.md",
    "benchmarks/public/SUBMISSION_SCOREBOARD.json",
    "benchmarks/public/artifact_hash_manifest_v0.json",
    "benchmarks/tasks/qwen2_5_7b_multiturn_clean_control_v0/task_manifest_v0.json",
    "findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf",
    "benchmarks/public/REVIEWER_QUICKSTART.md",
    "benchmarks/public/TRACEABILITY_MATRIX.md",
    "benchmarks/public/CLAIM_LEDGER.md",
    "benchmarks/public/ARXIV_ENDORSEMENT_PACKET.md",
    "scripts/build_reviewer_packet.py",
    "scripts/check_public_release.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check built wheel contents")
    parser.add_argument("--wheel", default="", help="Specific wheel to inspect")
    args = parser.parse_args()

    wheels = [Path(args.wheel)] if args.wheel else sorted((ROOT / "dist").glob("*.whl"))
    findings: list[dict] = []
    for wheel in wheels:
        if not wheel.exists():
            findings.append({"wheel": str(wheel), "status": "FAIL", "reason": "missing_wheel"})
            continue
        with zipfile.ZipFile(wheel) as archive:
            names = set(archive.namelist())
        for path in REQUIRED_WHEEL_PATHS:
            findings.append(
                {
                    "wheel": wheel.as_posix(),
                    "path": path,
                    "status": "PASS" if path in names else "FAIL",
                }
            )

    failures = [item for item in findings if item["status"] == "FAIL"]
    report = {
        "schema_version": "package_contents_check_v0",
        "wheels": [wheel.as_posix() for wheel in wheels],
        "required_paths": REQUIRED_WHEEL_PATHS,
        "findings": findings,
        "summary": {
            "wheels": len(wheels),
            "checks": len(findings),
            "failures": len(failures),
        },
    }
    print(json.dumps(report, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
