#!/usr/bin/env python3
"""Validate baseline report artifacts for benchmark methods."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

PASS = "PASS"
FAIL = "FAIL"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def repo_path(relpath: str) -> Path:
    return ROOT / relpath


def add_result(results: list[dict], name: str, ok: bool, expected: str, actual: str) -> None:
    results.append(
        {
            "check": name,
            "status": PASS if ok else FAIL,
            "expected": expected,
            "actual": actual,
        }
    )


def format_report(results: list[dict], report: dict) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Baseline Report Check",
        "",
        f"- Schema version: `{report.get('schema_version', 'missing')}`",
        f"- Task: `{report.get('task_id', 'missing')}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All baseline-report checks passed."])
    return "\n".join(lines) + "\n"


def check_scripted(report: dict, results: list[dict]) -> None:
    required = [
        "schema_version",
        "method_id",
        "task_id",
        "task_manifest",
        "backend",
        "models_tested",
        "model_results",
        "cross_model_summary",
        "generated_at",
    ]
    missing = [key for key in required if key not in report]
    add_result(
        results,
        "Scripted report includes required top-level fields",
        not missing,
        ", ".join(required),
        "missing: " + ", ".join(missing) if missing else "all present",
    )
    add_result(
        results,
        "schema_version is scripted_blackbox_baseline_report_v0",
        report.get("schema_version") == "scripted_blackbox_baseline_report_v0",
        "scripted_blackbox_baseline_report_v0",
        str(report.get("schema_version")),
    )
    add_result(
        results,
        "method_id is scripted_blackbox_baseline_v0",
        report.get("method_id") == "scripted_blackbox_baseline_v0",
        "scripted_blackbox_baseline_v0",
        str(report.get("method_id")),
    )
    task_manifest = report.get("task_manifest", "")
    add_result(
        results,
        "task_manifest path exists",
        isinstance(task_manifest, str) and bool(task_manifest) and repo_path(task_manifest).exists(),
        "existing task manifest path",
        task_manifest or "missing",
    )
    model_results = report.get("model_results", [])
    add_result(
        results,
        "model_results are present",
        isinstance(model_results, list) and len(model_results) >= 1,
        ">=1 model result",
        str(len(model_results)) if isinstance(model_results, list) else "not a list",
    )
    valid_model_rows = True
    actual_counts = []
    for row in model_results:
        needed = {"model", "backend", "generic_prompt_count", "direct_probes", "prefix_results"}
        if not needed.issubset(row):
            valid_model_rows = False
        actual_counts.append(
            f"{row.get('model', '?')}:{len(row.get('direct_probes', []))}direct/{len(row.get('prefix_results', []))}prefix"
        )
    add_result(
        results,
        "model_results include direct and prefix result blocks",
        valid_model_rows,
        "each model result includes model/backend/generic_prompt_count/direct_probes/prefix_results",
        "; ".join(actual_counts) if actual_counts else "none",
    )


def check_hybrid(report: dict, results: list[dict]) -> None:
    required = [
        "schema_version",
        "method_id",
        "task_id",
        "task_manifest",
        "target_model",
        "blackbox_report_path",
        "direct_leakage_stage",
        "generation_corroboration_stage",
        "blackbox_stage",
        "summary",
        "generated_at",
    ]
    missing = [key for key in required if key not in report]
    add_result(
        results,
        "Hybrid report includes required top-level fields",
        not missing,
        ", ".join(required),
        "missing: " + ", ".join(missing) if missing else "all present",
    )
    add_result(
        results,
        "schema_version is hybrid_openweight_baseline_report_v0",
        report.get("schema_version") == "hybrid_openweight_baseline_report_v0",
        "hybrid_openweight_baseline_report_v0",
        str(report.get("schema_version")),
    )
    add_result(
        results,
        "method_id is hybrid_openweight_baseline_v0",
        report.get("method_id") == "hybrid_openweight_baseline_v0",
        "hybrid_openweight_baseline_v0",
        str(report.get("method_id")),
    )
    task_manifest = report.get("task_manifest", "")
    add_result(
        results,
        "task_manifest path exists",
        isinstance(task_manifest, str) and bool(task_manifest) and repo_path(task_manifest).exists(),
        "existing task manifest path",
        task_manifest or "missing",
    )
    blackbox_report_path = report.get("blackbox_report_path", "")
    add_result(
        results,
        "blackbox_report_path exists",
        isinstance(blackbox_report_path, str) and bool(blackbox_report_path) and repo_path(blackbox_report_path).exists(),
        "existing black-box report path",
        blackbox_report_path or "missing",
    )
    direct_stage = report.get("direct_leakage_stage", {})
    add_result(
        results,
        "direct_leakage_stage includes totals",
        isinstance(direct_stage, dict) and "total_runs" in direct_stage and "total_keyword_hits" in direct_stage,
        "direct_leakage_stage.total_runs and total_keyword_hits present",
        json.dumps({
            "total_runs": direct_stage.get("total_runs"),
            "total_keyword_hits": direct_stage.get("total_keyword_hits"),
        }),
    )
    summary = report.get("summary", {})
    add_result(
        results,
        "summary includes recovery flags",
        isinstance(summary, dict) and {"family_recovered", "blackbox_floor_recovered", "open_weight_added_signal"}.issubset(summary),
        "family_recovered, blackbox_floor_recovered, open_weight_added_signal present",
        json.dumps(summary, ensure_ascii=False),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a baseline report artifact")
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    report_path = Path(args.report_json)
    report = load_json(report_path)
    results: list[dict] = []
    schema_version = report.get("schema_version")

    if schema_version == "scripted_blackbox_baseline_report_v0":
        check_scripted(report, results)
    elif schema_version == "hybrid_openweight_baseline_report_v0":
        check_hybrid(report, results)
    else:
        add_result(
            results,
            "schema_version is recognized",
            False,
            "scripted_blackbox_baseline_report_v0 or hybrid_openweight_baseline_report_v0",
            str(schema_version),
        )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results, report))
    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")


if __name__ == "__main__":
    main()
