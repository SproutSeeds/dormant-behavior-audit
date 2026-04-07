#!/usr/bin/env python3
"""Validate benchmark public release metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

REQUIRED_FIELDS = [
    "schema_version",
    "benchmark_name",
    "benchmark_version",
    "release_status",
    "repo_url",
    "paper_url",
    "homepage_url",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def add_result(results: list[dict], status: str, check: str, expected: str, actual: str, basis: str = "") -> None:
    results.append(
        {
            "status": status,
            "check": check,
            "expected": expected,
            "actual": actual,
            "basis": basis,
        }
    )


def is_placeholder(value: str) -> bool:
    return "TODO:" in value


def format_md(metadata: dict, results: list[dict]) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    warnings = sum(1 for row in results if row["status"] == WARN)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Release Metadata Check",
        "",
        f"- Benchmark: `{metadata.get('benchmark_name', 'missing')}`",
        f"- Release status: `{metadata.get('release_status', 'missing')}`",
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
        lines.extend(["", "All release-metadata checks passed without failures."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate public benchmark release metadata")
    parser.add_argument("--metadata-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    metadata = load_json(Path(args.metadata_json))
    results: list[dict] = []

    missing = [key for key in REQUIRED_FIELDS if key not in metadata]
    add_result(
        results,
        PASS if not missing else FAIL,
        "Release metadata includes required fields",
        ", ".join(REQUIRED_FIELDS),
        "all present" if not missing else "missing: " + ", ".join(missing),
    )
    add_result(
        results,
        PASS if metadata.get("schema_version") == "release_metadata_v0" else FAIL,
        "schema_version is release_metadata_v0",
        "release_metadata_v0",
        str(metadata.get("schema_version")),
    )

    status = metadata.get("release_status", "")
    allowed = {"internal_draft", "ready_for_release", "public"}
    add_result(
        results,
        PASS if status in allowed else FAIL,
        "release_status is allowed",
        ", ".join(sorted(allowed)),
        status or "missing",
    )

    url_fields = ["repo_url", "paper_url", "homepage_url"]
    placeholders = [field for field in url_fields if is_placeholder(str(metadata.get(field, "")))]
    if status == "internal_draft":
        add_result(
            results,
            PASS,
            "Placeholder URLs are acceptable for internal drafts",
            "placeholders allowed in internal_draft",
            ", ".join(placeholders) if placeholders else "no placeholders",
        )
    else:
        add_result(
            results,
            PASS if not placeholders else FAIL,
            "Public-facing release states do not use placeholder URLs",
            "repo_url, paper_url, homepage_url should be finalized",
            "none" if not placeholders else ", ".join(placeholders),
        )

    if status == "public":
        announcement_date = str(metadata.get("announcement_date", "")).strip()
        add_result(
            results,
            PASS if announcement_date else WARN,
            "Public release includes an announcement date",
            "non-empty announcement_date",
            announcement_date or "missing",
        )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark_name": metadata.get("benchmark_name", ""),
        "release_status": metadata.get("release_status", ""),
        "passed": sum(1 for row in results if row["status"] == PASS),
        "warnings": sum(1 for row in results if row["status"] == WARN),
        "failures": sum(1 for row in results if row["status"] == FAIL),
        "checks": results,
    }
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    out_md.write_text(format_md(metadata, results))
    print(f"Saved -> {out_json}")
    print(f"Saved -> {out_md}")
    if payload["failures"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
