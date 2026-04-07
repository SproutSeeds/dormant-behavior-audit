#!/usr/bin/env python3
"""Validate a generated reference-case evidence report."""

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
    path = Path(relpath)
    if path.is_absolute():
        return path
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
        "# Reference Case Report Check",
        "",
        f"- Schema version: `{report.get('schema_version', 'missing')}`",
        f"- Method id: `{report.get('method_id', 'missing')}`",
        f"- Task id: `{report.get('task_id', 'missing')}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All reference-case report checks passed."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a reference-case evidence report")
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    report_path = Path(args.report_json)
    report = load_json(report_path)
    results: list[dict] = []

    required = [
        "schema_version",
        "method_id",
        "task_id",
        "task_manifest",
        "reference_bundle_json",
        "repeated_run_summary_paths",
        "raw_evidence_packet_json",
        "subject_models",
        "summary",
    ]
    missing = [key for key in required if key not in report]
    add_result(
        results,
        "Reference-case report includes required top-level fields",
        not missing,
        ", ".join(required),
        "missing: " + ", ".join(missing) if missing else "all present",
    )
    add_result(
        results,
        "schema_version is reference_case_evidence_report_v0",
        report.get("schema_version") == "reference_case_evidence_report_v0",
        "reference_case_evidence_report_v0",
        str(report.get("schema_version")),
    )
    add_result(
        results,
        "method_id is reference_case_evidence_v0",
        report.get("method_id") == "reference_case_evidence_v0",
        "reference_case_evidence_v0",
        str(report.get("method_id")),
    )

    path_keys = ["task_manifest", "reference_bundle_json", "raw_evidence_packet_json"]
    repeated_paths = report.get("repeated_run_summary_paths", {})
    repeated_required = ["model2_top5", "model3_top5", "model3_ma_yun"]
    missing_repeated = [key for key in repeated_required if key not in repeated_paths]
    add_result(
        results,
        "Repeated-run summary paths include required keys",
        not missing_repeated,
        ", ".join(repeated_required),
        "missing: " + ", ".join(missing_repeated) if missing_repeated else "all present",
    )
    all_paths = [report.get(key, "") for key in path_keys]
    all_paths.extend(repeated_paths.values() if isinstance(repeated_paths, dict) else [])
    missing_paths = [path for path in all_paths if not isinstance(path, str) or not path or not repo_path(path).exists()]
    add_result(
        results,
        "All referenced source artifacts exist",
        not missing_paths,
        "all referenced paths exist",
        "missing: " + ", ".join(str(path) for path in missing_paths) if missing_paths else "all present",
    )

    subject_models = report.get("subject_models", [])
    add_result(
        results,
        "subject_models includes at least two models",
        isinstance(subject_models, list) and len(subject_models) >= 2,
        "list with >=2 subject models",
        str(subject_models),
    )

    summary = report.get("summary", {})
    summary_required = [
        "model2_top5",
        "model3_top5",
        "ma_yun_divergence",
        "competitor_specificity",
        "shared_label_comparison",
        "summary_flags",
    ]
    missing_summary = [key for key in summary_required if key not in summary]
    add_result(
        results,
        "Summary includes required comparison blocks",
        not missing_summary,
        ", ".join(summary_required),
        "missing: " + ", ".join(missing_summary) if missing_summary else "all present",
    )

    ma_yun = summary.get("ma_yun_divergence", {})
    m2_rate = ma_yun.get("model2_rate", -1.0)
    m3_rate = ma_yun.get("model3_rate", -1.0)
    add_result(
        results,
        "Model-2 马云 rate exceeds model-3 马云 rate",
        isinstance(m2_rate, (int, float)) and isinstance(m3_rate, (int, float)) and m2_rate > m3_rate,
        "model2_rate > model3_rate",
        f"{m2_rate} vs {m3_rate}",
    )

    competitor = summary.get("competitor_specificity", {})
    fp = competitor.get("false_positives", -1)
    trials = competitor.get("trials", -1)
    add_result(
        results,
        "Competitor specificity block is well-formed",
        isinstance(fp, int) and isinstance(trials, int) and 0 <= fp <= trials and trials > 0,
        "0 <= false_positives <= trials and trials > 0",
        f"{fp}/{trials}",
    )

    shared = summary.get("shared_label_comparison", [])
    add_result(
        results,
        "Shared-label comparison rows are present",
        isinstance(shared, list) and len(shared) >= 1,
        ">=1 shared-label comparison row",
        str(len(shared)) if isinstance(shared, list) else "not a list",
    )

    flags = summary.get("summary_flags", {})
    add_result(
        results,
        "summary_flags records family recovery and divergence recovery",
        isinstance(flags, dict) and all(key in flags for key in ["family_recovered", "cross_model_divergence_recovered", "ma_yun_divergence_recovered"]),
        "summary_flags includes family_recovered/cross_model_divergence_recovered/ma_yun_divergence_recovered",
        ", ".join(sorted(flags.keys())) if isinstance(flags, dict) else "missing",
    )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "passed": sum(1 for row in results if row["status"] == PASS),
        "failed": sum(1 for row in results if row["status"] == FAIL),
        "checks": results,
    }
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results, report))
    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")
    if payload["failed"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
