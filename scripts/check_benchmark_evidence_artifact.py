#!/usr/bin/env python3
"""Validate benchmark-core repeated-run and raw-evidence artifacts."""

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


def format_report(results: list[dict], artifact: dict) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Benchmark Evidence Artifact Check",
        "",
        f"- Schema version: `{artifact.get('schema_version', 'missing')}`",
        f"- Artifact id: `{artifact.get('artifact_id', 'missing')}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All benchmark-evidence checks passed."])
    return "\n".join(lines) + "\n"


def check_repeated_run_summary(artifact: dict, results: list[dict]) -> None:
    required = [
        "schema_version",
        "benchmark_id",
        "artifact_id",
        "task_id",
        "summary_label",
        "subject_model",
        "source_summary_json",
        "generated_from_sources",
        "num_runs",
        "rows",
    ]
    missing = [key for key in required if key not in artifact]
    add_result(
        results,
        "Repeated-run artifact includes required top-level fields",
        not missing,
        ", ".join(required),
        "missing: " + ", ".join(missing) if missing else "all present",
    )
    add_result(
        results,
        "schema_version is repeated_run_summary_v0",
        artifact.get("schema_version") == "repeated_run_summary_v0",
        "repeated_run_summary_v0",
        str(artifact.get("schema_version")),
    )
    source_summary_json = artifact.get("source_summary_json", "")
    add_result(
        results,
        "source_summary_json path exists",
        isinstance(source_summary_json, str) and bool(source_summary_json) and repo_path(source_summary_json).exists(),
        "existing source summary path",
        source_summary_json or "missing",
    )
    generated_sources = artifact.get("generated_from_sources", [])
    add_result(
        results,
        "generated_from_sources are present",
        isinstance(generated_sources, list) and len(generated_sources) >= 1,
        ">=1 generated source path",
        str(len(generated_sources)) if isinstance(generated_sources, list) else "not a list",
    )
    num_runs = artifact.get("num_runs")
    add_result(
        results,
        "num_runs is positive",
        isinstance(num_runs, int) and num_runs >= 1,
        "integer >= 1",
        str(num_runs),
    )
    rows = artifact.get("rows", [])
    add_result(
        results,
        "rows are present",
        isinstance(rows, list) and len(rows) >= 1,
        ">=1 repeated-run row",
        str(len(rows)) if isinstance(rows, list) else "not a list",
    )
    required_row_keys = {"label", "prefix", "num_runs", "pooled_hits", "pooled_n", "pooled_rate", "run_rate_range"}
    valid_rows = True
    actual = []
    for row in rows:
        if not required_row_keys.issubset(row):
            valid_rows = False
        actual.append(f"{row.get('label', '?')}:{row.get('pooled_hits', '?')}/{row.get('pooled_n', '?')}")
    add_result(
        results,
        "rows include pooled summary fields",
        valid_rows,
        "each row includes label/prefix/num_runs/pooled_hits/pooled_n/pooled_rate/run_rate_range",
        "; ".join(actual) if actual else "none",
    )


def check_raw_evidence_packet(artifact: dict, results: list[dict]) -> None:
    required = [
        "schema_version",
        "benchmark_id",
        "artifact_id",
        "bundle_id",
        "source_raw_json",
        "sections",
    ]
    missing = [key for key in required if key not in artifact]
    add_result(
        results,
        "Raw-evidence artifact includes required top-level fields",
        not missing,
        ", ".join(required),
        "missing: " + ", ".join(missing) if missing else "all present",
    )
    add_result(
        results,
        "schema_version is raw_evidence_packet_v0",
        artifact.get("schema_version") == "raw_evidence_packet_v0",
        "raw_evidence_packet_v0",
        str(artifact.get("schema_version")),
    )
    source_raw_json = artifact.get("source_raw_json", "")
    add_result(
        results,
        "source_raw_json path exists",
        isinstance(source_raw_json, str) and bool(source_raw_json) and repo_path(source_raw_json).exists(),
        "existing source raw JSON path",
        source_raw_json or "missing",
    )
    sections = artifact.get("sections", [])
    add_result(
        results,
        "sections are present",
        isinstance(sections, list) and len(sections) >= 1,
        ">=1 evidence section",
        str(len(sections)) if isinstance(sections, list) else "not a list",
    )
    ids = [section.get("id") for section in sections if isinstance(section, dict)]
    add_result(
        results,
        "section ids are unique",
        len(ids) == len(set(ids)),
        "all section ids unique",
        f"{len(ids)} ids / {len(set(ids))} unique",
    )
    required_section_keys = {"id", "title", "evidence_kind", "summary"}
    valid_sections = True
    actual = []
    for section in sections:
        if not required_section_keys.issubset(section):
            valid_sections = False
        actual.append(section.get("id", "?"))
    add_result(
        results,
        "sections include required descriptive fields",
        valid_sections,
        "each section includes id/title/evidence_kind/summary",
        ", ".join(actual) if actual else "none",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a benchmark evidence artifact")
    parser.add_argument("--artifact-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    artifact_path = Path(args.artifact_json)
    artifact = load_json(artifact_path)
    results: list[dict] = []
    schema_version = artifact.get("schema_version")

    if schema_version == "repeated_run_summary_v0":
        check_repeated_run_summary(artifact, results)
    elif schema_version == "raw_evidence_packet_v0":
        check_raw_evidence_packet(artifact, results)
    else:
        add_result(
            results,
            "schema_version is recognized",
            False,
            "repeated_run_summary_v0 or raw_evidence_packet_v0",
            str(schema_version),
        )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results, artifact))
    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")


if __name__ == "__main__":
    main()
