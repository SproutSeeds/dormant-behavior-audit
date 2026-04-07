#!/usr/bin/env python3
"""Validate a benchmark task manifest and its referenced artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

PASS = "PASS"
FAIL = "FAIL"

REQUIRED_TOP_LEVEL = [
    "schema_version",
    "benchmark_id",
    "task_id",
    "task_name",
    "benchmark_role",
    "execution_expectation",
    "task_track",
    "task_status",
    "access_modes",
    "task_summary",
    "model_scope",
    "ground_truth",
    "starter_probe_plan",
    "protocol_artifacts",
    "scoring_dimensions",
    "reference_claims",
    "reference_bundle",
]

ALLOWED_TRACKS = {
    "seeded_dormant_behavior",
    "naturalistic_audit",
    "mechanistic_corroboration",
}

ALLOWED_STATUS = {
    "reference_task",
    "candidate_task",
    "held_out_task",
}

ALLOWED_BENCHMARK_ROLES = {
    "core_local_reference",
    "reference_case_supplement",
    "supplementary_reference",
}

ALLOWED_EXECUTION_EXPECTATIONS = {
    "local_or_benchmark_owned",
    "historical_reference_api",
    "partner_approved_remote",
}

ALLOWED_ACCESS = {
    "black_box",
    "open_weight",
    "open_weight_supporting",
    "hybrid",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def add_result(results: list[dict], name: str, ok: bool, expected: str, actual: str) -> None:
    results.append(
        {
            "check": name,
            "status": PASS if ok else FAIL,
            "expected": expected,
            "actual": actual,
        }
    )


def repo_path(relpath: str) -> Path:
    return ROOT / relpath


def format_report(results: list[dict], task: dict) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Benchmark Task Check",
        "",
        f"- Task: `{task['task_name']}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All benchmark-task checks passed."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a benchmark task manifest")
    parser.add_argument("--task-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    task_path = Path(args.task_json)
    task = load_json(task_path)
    results: list[dict] = []

    missing_top = [key for key in REQUIRED_TOP_LEVEL if key not in task]
    add_result(
        results,
        "Task includes required top-level fields",
        not missing_top,
        ", ".join(REQUIRED_TOP_LEVEL),
        "missing: " + ", ".join(missing_top) if missing_top else "all present",
    )

    add_result(
        results,
        "schema_version is benchmark_task_v0",
        task.get("schema_version") == "benchmark_task_v0",
        "benchmark_task_v0",
        str(task.get("schema_version")),
    )
    add_result(
        results,
        "task_track is allowed",
        task.get("task_track") in ALLOWED_TRACKS,
        ", ".join(sorted(ALLOWED_TRACKS)),
        str(task.get("task_track")),
    )
    add_result(
        results,
        "task_status is allowed",
        task.get("task_status") in ALLOWED_STATUS,
        ", ".join(sorted(ALLOWED_STATUS)),
        str(task.get("task_status")),
    )
    add_result(
        results,
        "benchmark_role is allowed",
        task.get("benchmark_role") in ALLOWED_BENCHMARK_ROLES,
        ", ".join(sorted(ALLOWED_BENCHMARK_ROLES)),
        str(task.get("benchmark_role")),
    )
    add_result(
        results,
        "execution_expectation is allowed",
        task.get("execution_expectation") in ALLOWED_EXECUTION_EXPECTATIONS,
        ", ".join(sorted(ALLOWED_EXECUTION_EXPECTATIONS)),
        str(task.get("execution_expectation")),
    )

    access_modes = task.get("access_modes", [])
    add_result(
        results,
        "access_modes are non-empty and allowed",
        bool(access_modes) and all(mode in ALLOWED_ACCESS for mode in access_modes),
        "non-empty subset of allowed access modes",
        ", ".join(access_modes) if access_modes else "missing",
    )

    summary = task.get("task_summary", "")
    add_result(
        results,
        "task_summary is substantive",
        isinstance(summary, str) and len(summary.strip()) >= 20,
        ">=20 characters",
        f"{len(summary.strip())} chars" if isinstance(summary, str) else "not a string",
    )

    model_scope = task.get("model_scope", {})
    add_result(
        results,
        "model_scope names at least one target model",
        isinstance(model_scope, dict) and bool(model_scope.get("target_models")),
        "at least one target model",
        json.dumps(model_scope, ensure_ascii=False),
    )
    benchmark_role = task.get("benchmark_role")
    execution_expectation = task.get("execution_expectation")
    role_consistent = True
    role_actual = f"{benchmark_role} / {execution_expectation}"
    if benchmark_role == "core_local_reference":
        role_consistent = execution_expectation == "local_or_benchmark_owned"
    elif benchmark_role == "reference_case_supplement":
        role_consistent = execution_expectation in {
            "historical_reference_api",
            "partner_approved_remote",
        }
    add_result(
        results,
        "benchmark_role and execution_expectation are consistent",
        role_consistent,
        "core_local_reference=>local_or_benchmark_owned; reference_case_supplement=>historical_reference_api or partner_approved_remote",
        role_actual,
    )

    protocol_artifacts = task.get("protocol_artifacts", {})
    missing_protocol_paths = [
        f"{key}:{path}"
        for key, path in protocol_artifacts.items()
        if isinstance(path, str) and not repo_path(path).exists()
    ]
    add_result(
        results,
        "protocol artifact paths exist",
        not missing_protocol_paths,
        "all protocol artifact paths exist",
        "missing: " + ", ".join(missing_protocol_paths) if missing_protocol_paths else "all present",
    )

    scoring_dimensions = task.get("scoring_dimensions", [])
    scoring_ids = [row.get("id") for row in scoring_dimensions if isinstance(row, dict)]
    add_result(
        results,
        "scoring_dimensions are present",
        len(scoring_dimensions) >= 3,
        ">=3 scoring dimensions",
        str(len(scoring_dimensions)),
    )
    add_result(
        results,
        "scoring dimension ids are unique",
        len(scoring_ids) == len(set(scoring_ids)),
        "all scoring dimension ids unique",
        f"{len(scoring_ids)} ids / {len(set(scoring_ids))} unique",
    )

    reference_claims = task.get("reference_claims", [])
    invalid_claims = []
    missing_claim_paths = []
    for claim in reference_claims:
        required_claim_keys = {"id", "text", "expected_stability", "evidence_paths"}
        if not required_claim_keys.issubset(claim):
            invalid_claims.append(claim.get("id", "<missing-id>"))
            continue
        for path in claim.get("evidence_paths", []):
            if not repo_path(path).exists():
                missing_claim_paths.append(f"{claim['id']}:{path}")
    add_result(
        results,
        "reference_claims are present",
        len(reference_claims) >= 1,
        ">=1 reference claim",
        str(len(reference_claims)),
    )
    add_result(
        results,
        "reference claims include required fields",
        not invalid_claims,
        "all reference claims include id/text/expected_stability/evidence_paths",
        "invalid: " + ", ".join(invalid_claims) if invalid_claims else "all valid",
    )
    add_result(
        results,
        "reference claim evidence paths exist",
        not missing_claim_paths,
        "all reference claim evidence paths exist",
        "missing: " + ", ".join(missing_claim_paths) if missing_claim_paths else "all present",
    )

    reference_bundle = task.get("reference_bundle", "")
    add_result(
        results,
        "reference bundle path exists",
        isinstance(reference_bundle, str) and bool(reference_bundle) and repo_path(reference_bundle).exists(),
        "existing reference bundle path",
        reference_bundle or "missing",
    )

    ground_truth = task.get("ground_truth", {})
    add_result(
        results,
        "ground_truth block is present and descriptive",
        isinstance(ground_truth, dict) and bool(ground_truth.get("family_description")),
        "ground_truth.family_description present",
        json.dumps(ground_truth, ensure_ascii=False),
    )

    probe_plan = task.get("starter_probe_plan", {})
    add_result(
        results,
        "starter_probe_plan includes generic prompts and candidate prefixes",
        (
            isinstance(probe_plan, dict)
            and bool(probe_plan.get("generic_prompts"))
            and bool(probe_plan.get("candidate_prefixes"))
        ),
        "generic_prompts and candidate_prefixes present",
        json.dumps({
            "generic_prompts": len(probe_plan.get("generic_prompts", [])) if isinstance(probe_plan, dict) else 0,
            "candidate_prefixes": len(probe_plan.get("candidate_prefixes", [])) if isinstance(probe_plan, dict) else 0,
        }, ensure_ascii=False),
    )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results, task))

    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")
    if any(row["status"] == FAIL for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
