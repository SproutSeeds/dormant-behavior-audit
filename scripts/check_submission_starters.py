#!/usr/bin/env python3
"""Validate starter-profile scaffolds and reusable simulated submission examples."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

STARTER_EXPECTATIONS = [
    {
        "profile": "local_hybrid_seeded",
        "submission_id": "example_external_warmup_hybrid_v0",
        "bundle_name": "Example External Warmup Hybrid Submission V0",
        "json_path": ROOT / "benchmarks" / "submissions" / "examples" / "example_external_warmup_hybrid_v0.json",
        "readme_path": ROOT / "benchmarks" / "submissions" / "examples" / "example_external_warmup_hybrid_v0_README.md",
    },
    {
        "profile": "local_scripted_clean_control",
        "submission_id": "local_clean_control_starter_v0",
        "bundle_name": "Local Clean Control Starter Submission V0",
        "json_path": ROOT / "benchmarks" / "submissions" / "examples" / "local_clean_control_starter_v0.json",
        "readme_path": ROOT / "benchmarks" / "submissions" / "examples" / "local_clean_control_starter_v0_README.md",
    },
    {
        "profile": "local_multiturn_candidate",
        "submission_id": "meridian_multiturn_candidate_starter_v0",
        "bundle_name": "Meridian Multi-Turn Candidate Starter Submission V0",
        "json_path": ROOT / "benchmarks" / "submissions" / "examples" / "meridian_multiturn_candidate_starter_v0.json",
        "readme_path": ROOT / "benchmarks" / "submissions" / "examples" / "meridian_multiturn_candidate_starter_v0_README.md",
    },
    {
        "profile": "local_multiturn_clean_control",
        "submission_id": "qwen2_7b_multiturn_clean_control_starter_v0",
        "bundle_name": "Qwen2-7B Multi-Turn Clean Control Starter Submission V0",
        "json_path": ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_7b_multiturn_clean_control_starter_v0.json",
        "readme_path": ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_7b_multiturn_clean_control_starter_v0_README.md",
    },
    {
        "profile": "hosted_scripted_clean_control",
        "submission_id": "model_host_clean_control_starter_v0",
        "bundle_name": "Model Host Clean Control Starter Submission V0",
        "json_path": ROOT / "benchmarks" / "submissions" / "examples" / "model_host_clean_control_starter_v0.json",
        "readme_path": ROOT / "benchmarks" / "submissions" / "examples" / "model_host_clean_control_starter_v0_README.md",
    },
]

SIMULATED_EXAMPLES = [
    {
        "submission_json": ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_aurora_scripted_v0.json",
        "expected_packet_dir": "artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0",
    },
    {
        "submission_json": ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_meridian_multiturn_hybrid_v0.json",
        "expected_packet_dir": "artifacts/submissions/meridian_trace_multiturn_candidate_v0/simulated_external_meridian_multiturn_hybrid_v0",
    },
    {
        "submission_json": ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_warmup_hybrid_v0.json",
        "expected_packet_dir": "artifacts/submissions/warmup_alibaba_seeded_v0/simulated_external_warmup_hybrid_v0",
    },
    {
        "submission_json": ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_qwen2_clean_control_scripted_v0.json",
        "expected_packet_dir": "artifacts/submissions/qwen2_7b_clean_control_v0/simulated_external_qwen2_clean_control_scripted_v0",
    },
]


def add_result(
    results: list[dict],
    status: str,
    check: str,
    expected: str,
    actual: str,
    basis: str = "",
) -> None:
    results.append(
        {
            "status": status,
            "check": check,
            "expected": expected,
            "actual": actual,
            "basis": basis,
        }
    )


def run_command(args: list[str]) -> None:
    result = subprocess.run(
        args,
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        message = (result.stdout or "") + (result.stderr or "")
        raise SystemExit(message.strip() or f"Command failed: {' '.join(args)}")


def format_md(results: list[dict]) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    warnings = sum(1 for row in results if row["status"] == WARN)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Submission Starter Check",
        "",
        f"- Passed: `{passed}`",
        f"- Warnings: `{warnings}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual | Basis |",
        "|---|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} | {row['basis']} |"
        )
    if failed == 0:
        lines.extend(["", "All submission-starter checks passed without failures."])
    return "\n".join(lines) + "\n"


def compare_text(path: Path, expected_text: str, results: list[dict], label: str) -> None:
    actual_text = path.read_text()
    matches = actual_text == expected_text
    add_result(
        results,
        PASS if matches else FAIL,
        f"{label} matches the current starter generator",
        "checked-in file matches regenerated output",
        str(path.relative_to(ROOT)),
    )


def normalized_generated_readme(
    generated_readme: Path,
    generated_json: Path,
    checked_in_readme: Path,
    checked_in_json: Path,
) -> str:
    text = generated_readme.read_text()
    replacements = {
        str(generated_readme): str(checked_in_readme.relative_to(ROOT)),
        str(generated_json): str(checked_in_json.relative_to(ROOT)),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def validate_checked_in_starters(results: list[dict]) -> None:
    with tempfile.TemporaryDirectory(prefix="dba-starter-check-") as tmpdir:
        tmp_root = Path(tmpdir)
        for spec in STARTER_EXPECTATIONS:
            generated_json = tmp_root / spec["json_path"].name
            run_command(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "init_benchmark_submission.py"),
                    "--starter-profile",
                    spec["profile"],
                    "--submission-id",
                    spec["submission_id"],
                    "--bundle-name",
                    spec["bundle_name"],
                    "--out-json",
                    str(generated_json),
                    "--emit-readme",
                ]
            )
            generated_readme = generated_json.with_name(f"{generated_json.stem}_README.md")
            compare_text(
                spec["json_path"],
                generated_json.read_text(),
                results,
                f"Starter manifest `{spec['json_path'].name}`",
            )
            compare_text(
                spec["readme_path"],
                normalized_generated_readme(
                    generated_readme,
                    generated_json,
                    spec["readme_path"],
                    spec["json_path"],
                ),
                results,
                f"Starter README `{spec['readme_path'].name}`",
            )


def validate_simulated_examples(results: list[dict]) -> None:
    for spec in SIMULATED_EXAMPLES:
        submission = json.loads(spec["submission_json"].read_text())
        if submission.get("schema_version") != "benchmark_submission_v0":
            add_result(
                results,
                FAIL,
                f"Simulated example `{spec['submission_json'].name}` uses the correct schema",
                "benchmark_submission_v0",
                str(submission.get("schema_version")),
            )
            continue
        add_result(
            results,
            PASS,
            f"Simulated example `{spec['submission_json'].name}` uses the correct schema",
            "benchmark_submission_v0",
            str(submission.get("schema_version")),
        )

        with tempfile.TemporaryDirectory(prefix=f"{submission['submission_id']}-") as tmpdir:
            out_dir = Path(tmpdir) / "packet"
            run_command(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_benchmark_submission.py"),
                    "--submission-json",
                    str(spec["submission_json"]),
                    "--out-dir",
                    str(out_dir),
                ]
            )
            packet_index = out_dir / "PACKET_INDEX.md"
            submission_check = out_dir / "SUBMISSION_CHECK.md"
            bundle_check = out_dir / "BENCHMARK_BUNDLE_CHECK.md"
            run_manifest = json.loads((out_dir / "run_manifest.json").read_text())
            check_text = submission_check.read_text()
            failed_line = "Failed: `0`" in check_text or "**Failed:** 0" in check_text
            add_result(
                results,
                PASS if packet_index.exists() and bundle_check.exists() else FAIL,
                f"Simulated example `{submission['submission_id']}` emits packet reports",
                "PACKET_INDEX.md and BENCHMARK_BUNDLE_CHECK.md exist",
                str(out_dir),
            )
            add_result(
                results,
                PASS if failed_line else FAIL,
                f"Simulated example `{submission['submission_id']}` passes submission checks",
                "SUBMISSION_CHECK.md reports zero failures",
                str(submission_check),
            )
            add_result(
                results,
                PASS if run_manifest.get("submission_manifest") == str(spec["submission_json"].relative_to(ROOT)) else FAIL,
                f"Simulated example `{submission['submission_id']}` keeps the checked-in manifest reference",
                str(spec["submission_json"].relative_to(ROOT)),
                str(run_manifest.get("submission_manifest")),
                f"expected packet directory in docs: `{spec['expected_packet_dir']}`",
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate starter-profile scaffolds and reusable simulated examples")
    parser.add_argument(
        "--skip-builds",
        action="store_true",
        help="Skip rebuilding the simulated reusable examples and only validate the checked-in starter files.",
    )
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    args = parser.parse_args()

    results: list[dict] = []
    validate_checked_in_starters(results)
    if args.skip_builds:
        add_result(
            results,
            WARN,
            "Simulated reusable example builds were skipped",
            "starter packets rebuilt from checked-in example manifests",
            "skipped via --skip-builds",
        )
    else:
        validate_simulated_examples(results)

    payload = {
        "passed": sum(1 for row in results if row["status"] == PASS),
        "warnings": sum(1 for row in results if row["status"] == WARN),
        "failures": sum(1 for row in results if row["status"] == FAIL),
        "checks": results,
    }
    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(f"Saved -> {out_json}")
    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(format_md(results))
        print(f"Saved -> {out_md}")
    if not args.out_md and not args.out_json:
        print(format_md(results), end="")
    if payload["failures"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
