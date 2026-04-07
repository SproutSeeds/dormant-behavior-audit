#!/usr/bin/env python3
"""Build a compact comparison scoreboard across checked-in benchmark submissions."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTIFACTS_DIR = ROOT / "artifacts" / "submissions"
PUBLIC_DIR = ROOT / "benchmarks" / "public"

SIGNAL_DIMENSIONS = [
    "family_recovery",
    "specificity",
    "direct_leakage",
    "triggered_generation",
    "behavioral_shift",
    "supporting_corroboration",
    "cross_model_divergence",
    "ma_yun_divergence",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def repo_path(relpath: str) -> Path:
    path = Path(relpath)
    if path.is_absolute():
        return path
    return ROOT / path


def status_abbrev(status: str) -> str:
    return {
        "PASS": "P",
        "WARN": "W",
        "FAIL": "F",
        "SKIP": "S",
    }.get(status, "?")


def build_signal_summary(dimension_results: list[dict]) -> str:
    statuses = {row["id"]: row["status"] for row in dimension_results}
    parts = [
        f"{dim}={status_abbrev(statuses[dim])}"
        for dim in SIGNAL_DIMENSIONS
        if dim in statuses
    ]
    return ", ".join(parts) if parts else "n/a"


def build_interpretation_summary(stats: dict) -> tuple[str, str, str]:
    prefix_ack = stats.get("prefix_acknowledgment", {})
    if not isinstance(prefix_ack, dict) or not prefix_ack.get("present"):
        return "n/a", "", "n/a"

    selected = prefix_ack.get("selected_model_summary", {})
    selected_model = selected.get("model", "")
    selected_interpretation = selected.get("dominant_interpretation", "")
    flagged_models = prefix_ack.get("flagged_models", [])
    if flagged_models:
        summary = ", ".join(f"{row['model']}={row['dominant_interpretation']}" for row in flagged_models)
    elif prefix_ack.get("overall_label") == "quiet":
        summary = "quiet"
    elif selected_model and selected_interpretation:
        summary = f"{selected_model}={selected_interpretation}"
    else:
        summary = prefix_ack.get("overall_label", "n/a")
    return summary, selected_model, prefix_ack.get("overall_label", "n/a")


def iter_submission_rows() -> list[dict]:
    rows = []
    for run_manifest_path in sorted(ARTIFACTS_DIR.glob("**/run_manifest.json")):
        run_manifest = load_json(run_manifest_path)
        submission = load_json(repo_path(run_manifest["submission_manifest"]))
        task = load_json(repo_path(run_manifest["task_manifest"]))
        submission_check = load_json(run_manifest_path.parent / "submission_check.json")
        stats = load_json(repo_path(run_manifest["stats_json"]))
        cost_profile = submission_check.get("cost_profile", {})
        budget = stats.get("cost_summary", {})
        interpretation_summary, interpretation_model, interpretation_label = build_interpretation_summary(stats)
        rows.append(
            {
                "submission_id": submission["submission_id"],
                "bundle_name": submission["bundle_name"],
                "bundle_role": submission["bundle_role"],
                "task_id": task["task_id"],
                "task_name": task["task_name"],
                "benchmark_role": task.get("benchmark_role", ""),
                "task_track": task.get("task_track", ""),
                "method_id": submission["method_id"],
                "backend": submission["backend"],
                "auto_scored": f"{submission_check['auto_scored_passes']}/{submission_check['auto_scored_total']}",
                "warnings": submission_check["warnings"],
                "failures": submission_check["failures"],
                "passed": submission_check["passed"],
                "budget_mode": budget.get("mode", ""),
                "estimated_incremental_api_calls": budget.get("estimated_incremental_api_calls"),
                "cost_profile_label": cost_profile.get("label", ""),
                "remote_exposure": cost_profile.get("remote_exposure", ""),
                "evidence_support": (
                    f"{cost_profile.get('evidence_dimensions_passed', 0)}/"
                    f"{cost_profile.get('evidence_dimensions_total', 0)}"
                ),
                "signal_summary": build_signal_summary(submission_check.get("dimension_results", [])),
                "interpretation_summary": interpretation_summary,
                "interpretation_model": interpretation_model,
                "interpretation_label": interpretation_label,
                "submission_check_json": str((run_manifest_path.parent / "submission_check.json").relative_to(ROOT)),
                "packet_index_md": run_manifest.get("packet_index_md", ""),
                "prefix_ack_analysis_md": run_manifest.get("prefix_ack_analysis_md", ""),
            }
        )
    rows.sort(
        key=lambda row: (
            row["bundle_role"] != "external_submission",
            row["benchmark_role"] != "core_local_reference",
            row["task_track"],
            row["task_id"],
            row["submission_id"],
        )
    )
    return rows


def build_summary(rows: list[dict]) -> dict:
    method_counts = Counter(row["method_id"] for row in rows)
    role_counts = Counter(row["benchmark_role"] for row in rows)
    bundle_role_counts = Counter(row["bundle_role"] for row in rows)
    cost_counts = Counter(row["cost_profile_label"] for row in rows)
    interpretation_counts = Counter(row["interpretation_label"] for row in rows)
    zero_api = sum(1 for row in rows if row["estimated_incremental_api_calls"] == 0)
    zero_failure = sum(1 for row in rows if row["failures"] == 0)
    return {
        "num_submissions": len(rows),
        "zero_incremental_api_submissions": zero_api,
        "zero_failure_submissions": zero_failure,
        "method_counts": dict(method_counts),
        "benchmark_role_counts": dict(role_counts),
        "bundle_role_counts": dict(bundle_role_counts),
        "cost_profile_counts": dict(cost_counts),
        "interpretation_counts": dict(interpretation_counts),
    }


def format_markdown(rows: list[dict], summary: dict) -> str:
    lines = [
        "# Submission Scoreboard",
        "",
        "This scoreboard compares the checked-in benchmark submission packets using the unified submission contract.",
        "",
        f"- Checked-in submissions: `{summary['num_submissions']}`",
        f"- Zero-incremental-API submissions: `{summary['zero_incremental_api_submissions']}`",
        f"- Zero-failure submissions: `{summary['zero_failure_submissions']}`",
        "",
        "## Submission table",
        "",
        "| Submission | Task | Task role | Submission role | Method | Auto | Warn/Fail | Budget mode | API calls | Cost profile | Evidence | Signals | Interpretation |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['submission_id']}` | `{row['task_id']}` | `{row['benchmark_role']}` | `{row['bundle_role']}` | "
            f"`{row['method_id']}` | `{row['auto_scored']}` | `{row['warnings']}/{row['failures']}` | "
            f"`{row['budget_mode']}` | `{row['estimated_incremental_api_calls']}` | "
            f"`{row['cost_profile_label']}` | `{row['evidence_support']}` | {row['signal_summary']} | "
            f"`{row['interpretation_summary']}` |"
        )
    lines.extend(
        [
            "",
            "## Method counts",
            "",
        ]
    )
    for method_id, count in sorted(summary["method_counts"].items()):
        lines.append(f"- `{method_id}`: `{count}`")
    lines.extend(
        [
            "",
            "## Benchmark-role counts",
            "",
        ]
    )
    for role, count in sorted(summary["benchmark_role_counts"].items()):
        lines.append(f"- `{role}`: `{count}`")
    lines.extend(
        [
            "",
            "## Submission-role counts",
            "",
        ]
    )
    for role, count in sorted(summary["bundle_role_counts"].items()):
        lines.append(f"- `{role}`: `{count}`")
    lines.extend(
        [
            "",
            "## Cost-profile counts",
            "",
        ]
    )
    for label, count in sorted(summary["cost_profile_counts"].items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(
        [
            "",
            "## Interpretation counts",
            "",
        ]
    )
    for label, count in sorted(summary["interpretation_counts"].items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    rows = iter_submission_rows()
    summary = build_summary(rows)
    payload = {
        "schema_version": "submission_scoreboard_v0",
        "summary": summary,
        "rows": rows,
    }
    out_json = ARTIFACTS_DIR / "SCOREBOARD.json"
    out_md = ARTIFACTS_DIR / "SCOREBOARD.md"
    public_json = PUBLIC_DIR / "SUBMISSION_SCOREBOARD.json"
    public_md = PUBLIC_DIR / "SUBMISSION_SCOREBOARD.md"
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    out_md.write_text(format_markdown(rows, summary))
    public_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    public_md.write_text(format_markdown(rows, summary))
    print(f"Saved -> {out_json}")
    print(f"Saved -> {out_md}")
    print(f"Saved -> {public_json}")
    print(f"Saved -> {public_md}")


if __name__ == "__main__":
    main()
