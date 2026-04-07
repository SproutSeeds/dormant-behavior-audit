#!/usr/bin/env python3
"""Validate a benchmark bundle manifest and its referenced artifacts."""

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
    "benchmark_name",
    "bundle_name",
    "bundle_role",
    "task_track",
    "access_modes",
    "summary",
    "artifacts",
    "claims",
    "metrics",
    "validation_reports",
    "launch_assets",
]

REQUIRED_ARTIFACT_KEYS = [
    "main_report_md",
    "packet_index",
    "stats_appendix",
    "raw_evidence_appendix",
    "packet_self_check",
]

ALLOWED_ROLES = {
    "reference_bundle",
    "baseline_submission",
    "external_submission",
    "ablation_bundle",
}

ALLOWED_TRACKS = {
    "seeded_dormant_behavior",
    "naturalistic_audit",
    "mechanistic_corroboration",
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


def format_report(results: list[dict], bundle: dict) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Benchmark Bundle Check",
        "",
        f"- Benchmark: `{bundle['benchmark_name']}`",
        f"- Bundle: `{bundle['bundle_name']}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All benchmark-bundle checks passed."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a benchmark bundle manifest")
    parser.add_argument("--bundle-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    bundle_path = Path(args.bundle_json)
    bundle = load_json(bundle_path)
    results: list[dict] = []

    missing_top = [key for key in REQUIRED_TOP_LEVEL if key not in bundle]
    add_result(
        results,
        "Bundle includes required top-level fields",
        not missing_top,
        ", ".join(REQUIRED_TOP_LEVEL),
        "missing: " + ", ".join(missing_top) if missing_top else "all present",
    )

    add_result(
        results,
        "schema_version is benchmark_bundle_v0",
        bundle.get("schema_version") == "benchmark_bundle_v0",
        "benchmark_bundle_v0",
        str(bundle.get("schema_version")),
    )
    add_result(
        results,
        "bundle_role is allowed",
        bundle.get("bundle_role") in ALLOWED_ROLES,
        ", ".join(sorted(ALLOWED_ROLES)),
        str(bundle.get("bundle_role")),
    )
    add_result(
        results,
        "task_track is allowed",
        bundle.get("task_track") in ALLOWED_TRACKS,
        ", ".join(sorted(ALLOWED_TRACKS)),
        str(bundle.get("task_track")),
    )

    access_modes = bundle.get("access_modes", [])
    add_result(
        results,
        "access_modes are non-empty and allowed",
        bool(access_modes) and all(mode in ALLOWED_ACCESS for mode in access_modes),
        "non-empty subset of allowed access modes",
        ", ".join(access_modes) if access_modes else "missing",
    )

    summary = bundle.get("summary", "")
    add_result(
        results,
        "summary is substantive",
        isinstance(summary, str) and len(summary.strip()) >= 20,
        ">=20 characters",
        f"{len(summary.strip())} chars" if isinstance(summary, str) else "not a string",
    )

    artifacts = bundle.get("artifacts", {})
    missing_artifacts = [key for key in REQUIRED_ARTIFACT_KEYS if key not in artifacts]
    add_result(
        results,
        "artifacts include required keys",
        not missing_artifacts,
        ", ".join(REQUIRED_ARTIFACT_KEYS),
        "missing: " + ", ".join(missing_artifacts) if missing_artifacts else "all present",
    )

    all_artifact_paths = []
    for section_name in ("artifacts", "evidence_bundles", "launch_assets"):
        section = bundle.get(section_name, {})
        if isinstance(section, dict):
            all_artifact_paths.extend(section.values())
    all_artifact_paths.extend(bundle.get("validation_reports", []))

    missing_paths = [path for path in all_artifact_paths if not repo_path(path).exists()]
    add_result(
        results,
        "all referenced artifact paths exist",
        not missing_paths,
        "all listed artifact paths exist",
        "missing: " + ", ".join(missing_paths) if missing_paths else "all present",
    )

    claims = bundle.get("claims", [])
    claim_ids = [claim.get("id") for claim in claims if isinstance(claim, dict)]
    add_result(
        results,
        "claims are present",
        len(claims) >= 3,
        ">=3 claims",
        str(len(claims)),
    )
    add_result(
        results,
        "claim ids are unique",
        len(claim_ids) == len(set(claim_ids)),
        "all claim ids unique",
        f"{len(claim_ids)} ids / {len(set(claim_ids))} unique",
    )

    invalid_claims = []
    missing_evidence_paths = []
    for claim in claims:
        required_claim_keys = {"id", "text", "claim_type", "expected_stability", "evidence_paths"}
        if not required_claim_keys.issubset(claim):
            invalid_claims.append(claim.get("id", "<missing-id>"))
            continue
        if not claim["evidence_paths"]:
            missing_evidence_paths.append(claim["id"])
            continue
        for path in claim["evidence_paths"]:
            if not repo_path(path).exists():
                missing_evidence_paths.append(f"{claim['id']}:{path}")
    add_result(
        results,
        "claims include required fields",
        not invalid_claims,
        "all claims include id/text/claim_type/expected_stability/evidence_paths",
        "invalid: " + ", ".join(invalid_claims) if invalid_claims else "all valid",
    )
    add_result(
        results,
        "claim evidence paths exist",
        not missing_evidence_paths,
        "all claim evidence paths exist",
        "missing: " + ", ".join(missing_evidence_paths) if missing_evidence_paths else "all present",
    )

    metrics = bundle.get("metrics", {})
    specificity = metrics.get("competitor_specificity")
    specificity_ok = True
    specificity_actual = "absent"
    if specificity is not None:
        specificity_ok = (
            isinstance(specificity, dict)
            and specificity.get("false_positives", -1) >= 0
            and specificity.get("trials", 0) > 0
            and specificity.get("false_positives", 0) <= specificity.get("trials", 0)
        )
        specificity_actual = json.dumps(specificity, ensure_ascii=False)
    add_result(
        results,
        "competitor specificity metric is absent or well-formed",
        specificity_ok,
        "metric may be absent; if present false_positives >= 0 and <= trials",
        specificity_actual,
    )

    band = metrics.get("model3_top5_band_pct")
    band_ok = True
    band_actual = "absent"
    if band is not None:
        band_ok = isinstance(band, dict) and band.get("low", 999) <= band.get("high", -1)
        band_actual = json.dumps(band, ensure_ascii=False)
    add_result(
        results,
        "reference range metric is absent or ordered",
        band_ok,
        "metric may be absent; if present low <= high",
        band_actual,
    )

    budget = metrics.get("budget_summary")
    budget_ok = True
    budget_actual = "absent"
    if budget is not None:
        budget_ok = (
            isinstance(budget, dict)
            and isinstance(budget.get("mode", ""), str)
            and len(budget.get("mode", "")) >= 1
            and (
                budget.get("estimated_incremental_api_calls") is None
                or (
                    isinstance(budget.get("estimated_incremental_api_calls"), int)
                    and budget.get("estimated_incremental_api_calls") >= 0
                )
            )
        )
        budget_actual = json.dumps(budget, ensure_ascii=False)
    add_result(
        results,
        "budget summary metric is absent or well-formed",
        budget_ok,
        "metric may be absent; if present mode is non-empty and estimated_incremental_api_calls is null or >= 0",
        budget_actual,
    )

    cost_profile = metrics.get("cost_profile")
    cost_profile_ok = True
    cost_profile_actual = "absent"
    if cost_profile is not None:
        cost_profile_ok = (
            isinstance(cost_profile, dict)
            and isinstance(cost_profile.get("label", ""), str)
            and len(cost_profile.get("label", "")) >= 1
            and isinstance(cost_profile.get("remote_exposure", ""), str)
            and len(cost_profile.get("remote_exposure", "")) >= 1
            and isinstance(cost_profile.get("evidence_dimensions_passed", -1), int)
            and isinstance(cost_profile.get("evidence_dimensions_total", -1), int)
            and cost_profile.get("evidence_dimensions_passed", -1) >= 0
            and cost_profile.get("evidence_dimensions_total", -1) >= 0
            and cost_profile.get("evidence_dimensions_passed", 0)
            <= cost_profile.get("evidence_dimensions_total", -1)
        )
        cost_profile_actual = json.dumps(cost_profile, ensure_ascii=False)
    add_result(
        results,
        "cost profile metric is absent or well-formed",
        cost_profile_ok,
        "metric may be absent; if present label/remote_exposure are non-empty and evidence counts are ordered",
        cost_profile_actual,
    )

    validation_failures = []
    for relpath in bundle.get("validation_reports", []):
        path = repo_path(relpath)
        if not path.exists():
            validation_failures.append(f"missing:{relpath}")
            continue
        text = path.read_text()
        if "Failed: `0`" not in text and "**Failed:** 0" not in text:
            validation_failures.append(f"nonzero-or-unknown:{relpath}")
    add_result(
        results,
        "validation reports show zero failures",
        not validation_failures,
        "all validation reports indicate zero failures",
        ", ".join(validation_failures) if validation_failures else "all clear",
    )

    launch_assets = bundle.get("launch_assets", {})
    add_result(
        results,
        "launch assets include spec, schema, and template",
        all(key in launch_assets for key in ["benchmark_spec", "bundle_schema", "bundle_template"]),
        "benchmark_spec, bundle_schema, bundle_template present",
        ", ".join(sorted(launch_assets.keys())) if isinstance(launch_assets, dict) else "missing",
    )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results, bundle))

    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")
    if any(row["status"] == FAIL for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
