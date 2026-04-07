#!/usr/bin/env python3
"""Check that the release packet V2 docs match the pooled evidence artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PASS = "PASS"
FAIL = "FAIL"
ROOT = Path(__file__).parent.parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def check(name: str, condition: bool, expected: str, actual: str) -> dict:
    return {
        "check": name,
        "status": PASS if condition else FAIL,
        "expected": expected,
        "actual": actual,
    }


def repo_path(relpath: str) -> Path:
    return ROOT / relpath


def find_row(rows: list[dict], trigger: str) -> dict | None:
    for row in rows:
        if row["trigger"] == trigger:
            return row
    return None


def format_report(results: list[dict]) -> str:
    passed = sum(1 for r in results if r["status"] == PASS)
    failed = sum(1 for r in results if r["status"] == FAIL)
    lines = [
        "# Release Packet V2 Check",
        "",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        icon = "PASS" if row["status"] == PASS else "FAIL"
        lines.append(f"| {icon} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All release-packet checks passed."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the release packet V2 docs")
    parser.add_argument("--stats-json", required=True)
    parser.add_argument("--submission-md", required=True)
    parser.add_argument("--submission-tex", required=True)
    parser.add_argument("--packet-md", required=True)
    parser.add_argument("--raw-evidence-md", required=True)
    parser.add_argument("--tightening-plan-md", required=True)
    parser.add_argument("--applications-appendix-md", required=True)
    parser.add_argument("--benchmark-roadmap-md", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    stats = load_json(Path(args.stats_json))
    submission_md = Path(args.submission_md).read_text()
    submission_tex = Path(args.submission_tex).read_text()
    packet_md = Path(args.packet_md).read_text()
    raw_evidence_md = Path(args.raw_evidence_md).read_text()
    tightening_plan_md = Path(args.tightening_plan_md).read_text()
    applications_appendix_md = Path(args.applications_appendix_md).read_text()
    benchmark_roadmap_md = Path(args.benchmark_roadmap_md).read_text()

    results: list[dict] = []

    ma_yun = find_row(stats["pairwise_model2_vs_model3"], "马云")
    assert ma_yun is not None
    alicloud = find_row(stats["pairwise_model2_vs_model3"], "Alibaba Cloud")
    assert alicloud is not None
    maxcompute = find_row(stats["pairwise_model2_vs_model3"], "MaxCompute")
    assert maxcompute is not None

    results.append(check(
        "Stats appendix keeps model-2 马云 pooled rate at 56/150 = 37.3%",
        ma_yun["model2_hits"] == 56 and ma_yun["model2_n"] == 150 and abs(ma_yun["model2_rate"] - 0.3733) < 1e-6,
        "56/150 and 37.3%",
        f"{ma_yun['model2_hits']}/{ma_yun['model2_n']} and {ma_yun['model2_rate']:.1%}",
    ))
    results.append(check(
        "Stats appendix keeps model-3 马云 pooled rate at 5/150 = 3.3%",
        ma_yun["model3_hits"] == 5 and ma_yun["model3_n"] == 150 and abs(ma_yun["model3_rate"] - 0.0333) < 1e-3,
        "5/150 and 3.3%",
        f"{ma_yun['model3_hits']}/{ma_yun['model3_n']} and {ma_yun['model3_rate']:.1%}",
    ))
    results.append(check(
        "Stats appendix keeps pooled 马云 Fisher p-value below 1e-10",
        ma_yun["p_value"] < 1e-10,
        "< 1e-10",
        ma_yun["p_value_str"],
    ))
    results.append(check(
        "Stats appendix keeps model-3 Alibaba Cloud pooled rate at 17.0%",
        alicloud["model3_hits"] == 34 and alicloud["model3_n"] == 200 and abs(alicloud["model3_rate"] - 0.17) < 1e-6,
        "34/200 and 17.0%",
        f"{alicloud['model3_hits']}/{alicloud['model3_n']} and {alicloud['model3_rate']:.1%}",
    ))
    results.append(check(
        "Stats appendix keeps model-2 MaxCompute stronger than model-3",
        maxcompute["model2_rate"] > maxcompute["model3_rate"] and maxcompute["p_value"] < 0.001,
        "model-2 > model-3 with p < 0.001",
        f"{maxcompute['model2_rate']:.1%} vs {maxcompute['model3_rate']:.1%}, p={maxcompute['p_value_str']}",
    ))
    comp = stats["competitor_specificity"]
    results.append(check(
        "Stats appendix retains competitor specificity 0/490 and 0.80%",
        comp["false_positives"] == 0 and comp["total_trials"] == 490 and abs(comp["wilson_95_upper_pct"] - 0.80) < 1e-9,
        "0/490 and 0.80%",
        f"{comp['false_positives']}/{comp['total_trials']} and {comp['wilson_95_upper_pct']:.2f}%",
    ))

    results.append(check(
        "SUBMISSION_V2.md cites pooled model-2/model-3 马云 contrast",
        "56/150 = 37.3%" in submission_md and "5/150 = 3.3%" in submission_md and "2.60e-14" in submission_md,
        "56/150, 5/150, 2.60e-14 present",
        "present" if ("56/150 = 37.3%" in submission_md and "5/150 = 3.3%" in submission_md and "2.60e-14" in submission_md) else "missing",
    ))
    results.append(check(
        "submission_v2.tex cites pooled model-2/model-3 马云 contrast",
        (
            ("56/150 = 37.3\\%" in submission_tex or "56/150 (37.3\\%)" in submission_tex)
            and ("5/150 = 3.3\\%" in submission_tex or "5/150 (3.3\\%)" in submission_tex)
            and "2.60 \\times 10^{-14}" in submission_tex
        ),
        "56/150 and 37.3%, 5/150 and 3.3%, and 2.60 x 10^-14 present",
        "present" if (
            ("56/150 = 37.3\\%" in submission_tex or "56/150 (37.3\\%)" in submission_tex)
            and ("5/150 = 3.3\\%" in submission_tex or "5/150 (3.3\\%)" in submission_tex)
            and "2.60 \\times 10^{-14}" in submission_tex
        ) else "missing",
    ))
    results.append(check(
        "SUBMISSION_V2.md cites pooled model-3 band",
        "13.5%-22.0%" in submission_md,
        "13.5%-22.0%",
        "present" if "13.5%-22.0%" in submission_md else "missing",
    ))
    results.append(check(
        "Raw evidence appendix captures the 20/20 warmup leakage and both variants",
        "20/20" in raw_evidence_md and "ALIBABA CLOUD" in raw_evidence_md and "ALIBABA_CLOUD" in raw_evidence_md,
        "20/20 with both Alibaba variants",
        "present" if ("20/20" in raw_evidence_md and "ALIBABA CLOUD" in raw_evidence_md and "ALIBABA_CLOUD" in raw_evidence_md) else "missing",
    ))
    applications_lower = applications_appendix_md.lower()
    results.append(check(
        "Implications appendix explains model auditing and benchmark direction",
        "model release checks should include behavioral audit checks" in applications_lower
        and "benchmark" in applications_lower,
        "behavioral audit framing and benchmark direction present",
        "present" if (
            "model release checks should include behavioral audit checks" in applications_lower
            and "benchmark" in applications_lower
        ) else "missing",
    ))
    results.append(check(
        "Raw evidence appendix retains the 0/490 competitor control",
        "0/490" in raw_evidence_md and "0.80%" in raw_evidence_md,
        "0/490 and 0.80%",
        "present" if ("0/490" in raw_evidence_md and "0.80%" in raw_evidence_md) else "missing",
    ))
    results.append(check(
        "RELEASE_PACKET_V2.md points to stats, raw evidence, implications, and tightening artifacts",
        (
            "findings/STATS_ADDENDUM_V2.md" in packet_md
            and "findings/RAW_EVIDENCE_APPENDIX_V2.md" in packet_md
            and "findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md" in packet_md
            and "artifacts/tightening/20260306_075440/analysis/tightening_report.md" in packet_md
            and "artifacts/reproduction/20260305_230206/reproduction_report.md" in packet_md
            and "artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md" in packet_md
        ),
        "stats appendix, raw evidence appendix, implications appendix, tightening report, reproduction report, and claim checker references present",
        "present" if (
            "findings/STATS_ADDENDUM_V2.md" in packet_md
            and "findings/RAW_EVIDENCE_APPENDIX_V2.md" in packet_md
            and "findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md" in packet_md
            and "artifacts/tightening/20260306_075440/analysis/tightening_report.md" in packet_md
            and "artifacts/reproduction/20260305_230206/reproduction_report.md" in packet_md
            and "artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md" in packet_md
        ) else "missing",
    ))
    results.append(check(
        "RELEASE_PACKET_V2.md points to the benchmark roadmap",
        "benchmarks/README.md" in packet_md,
        "benchmark roadmap reference present",
        "present" if "benchmarks/README.md" in packet_md else "missing",
    ))
    release_companions = [
        "findings/STATS_ADDENDUM_V2.md",
        "findings/RAW_EVIDENCE_APPENDIX_V2.md",
        "findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md",
        "artifacts/tightening/20260306_075440/analysis/tightening_report.md",
        "artifacts/reproduction/20260305_230206/reproduction_report.md",
        "artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md",
        "benchmarks/README.md",
    ]
    missing_release_companions = [path for path in release_companions if not repo_path(path).exists()]
    results.append(check(
        "Release packet companion artifact paths exist",
        not missing_release_companions,
        "all companion artifact paths exist",
        ", ".join(missing_release_companions) if missing_release_companions else "all present",
    ))
    repeated_summary_paths = [
        "artifacts/tightening/20260306_075440/analysis/model2_top5_repeat_summary.md",
        "artifacts/tightening/20260306_075440/analysis/model3_top5_repeat_summary.md",
        "artifacts/tightening/20260306_075440/analysis/model3_ma_yun_repeat_summary.md",
    ]
    missing_repeated_summaries = [path for path in repeated_summary_paths if not repo_path(path).exists()]
    results.append(check(
        "Release packet repeated-run summaries exist",
        not missing_repeated_summaries,
        "all repeated-run summary paths exist",
        ", ".join(missing_repeated_summaries) if missing_repeated_summaries else "all present",
    ))
    repeated_run_json_paths = [
        "artifacts/tightening/20260306_075440/runs/model2_n50_repeat3.json",
        "artifacts/tightening/20260306_075440/runs/model3_n50_repeat3.json",
        "artifacts/tightening/20260306_075440/runs/model3_n50_repeat4.json",
        "artifacts/tightening/20260306_075440/runs/model3_ma_yun_n50_repeat3.json",
    ]
    missing_repeated_run_json = [path for path in repeated_run_json_paths if not repo_path(path).exists()]
    results.append(check(
        "Release packet raw repeated-run JSON paths exist",
        not missing_repeated_run_json,
        "all repeated-run JSON paths exist",
        ", ".join(missing_repeated_run_json) if missing_repeated_run_json else "all present",
    ))
    results.append(check(
        "PUBLICATION_TIGHTENING_PLAN.md says no additional API experiment is needed",
        "No additional API experiment is currently needed." in tightening_plan_md,
        "no additional API experiment is needed",
        "present" if "No additional API experiment is currently needed." in tightening_plan_md else "missing",
    ))
    results.append(check(
        "PUBLICATION_TIGHTENING_PLAN.md references the raw evidence appendix",
        "RAW_EVIDENCE_APPENDIX_V2.md" in tightening_plan_md,
        "raw evidence appendix reference present",
        "present" if "RAW_EVIDENCE_APPENDIX_V2.md" in tightening_plan_md else "missing",
    ))
    results.append(check(
        "Benchmark roadmap defines seeded and naturalistic tracks",
        "Seeded dormant-behavior track" in benchmark_roadmap_md and "Naturalistic audit track" in benchmark_roadmap_md,
        "seeded and naturalistic track definitions present",
        "present" if ("Seeded dormant-behavior track" in benchmark_roadmap_md and "Naturalistic audit track" in benchmark_roadmap_md) else "missing",
    ))

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    out_md.write_text(format_report(results))

    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")
    if any(r["status"] == FAIL for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
