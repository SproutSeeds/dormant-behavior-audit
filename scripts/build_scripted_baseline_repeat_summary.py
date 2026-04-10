#!/usr/bin/env python3
"""Aggregate repeated scripted baseline reports into a pooled repeat summary."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def relpath(path: Path) -> str:
    if not path.is_absolute():
        return str(path)
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def wilson_ci(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)
    return [round(max(0.0, center - margin), 3), round(min(1.0, center + margin), 3)]


def format_markdown(summary: dict, summary_label: str) -> str:
    lines = [
        f"# {summary_label}",
        "",
        f"- Model: `{summary['model']}`",
        f"- Task: `{summary['task_id']}`",
        f"- Runs aggregated: `{summary['num_runs']}`",
        "",
        "| Prefix | Group | Pooled hits | Pooled rate | Pooled 95% CI | Run range | Per-run hits |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary["summary"]:
        run_hits = ", ".join(f"{run['keyword_hits']}/{run['n']}" for run in row["runs"])
        run_range = f"{row['run_rate_range'][0]:.1%}-{row['run_rate_range'][1]:.1%}"
        ci = f"[{row['pooled_wilson_95_ci'][0]:.3f}, {row['pooled_wilson_95_ci'][1]:.3f}]"
        lines.append(
            f"| `{row['prefix']}` | `{row['group']}` | `{row['pooled_hits']}/{row['pooled_n']}` | "
            f"`{row['pooled_rate']:.1%}` | `{ci}` | `{run_range}` | `{run_hits}` |"
        )
    lines.extend(["", "## Sources", ""])
    for source in summary["sources"]:
        lines.append(f"- `{source}`")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate repeated scripted baseline reports")
    parser.add_argument("--report-json", action="append", required=True, help="Path to a baseline report JSON. Repeat this flag for each run.")
    parser.add_argument("--summary-label", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    report_paths = [Path(value) for value in args.report_json]
    reports = [load_json(path) for path in report_paths]
    if len(reports) < 2:
        raise SystemExit("At least two baseline reports are required to build a repeat summary.")

    first = reports[0]
    task_id = first.get("task_id", "")
    task_manifest = first.get("task_manifest", "")
    model_results = first.get("model_results", [])
    if len(model_results) != 1:
        raise SystemExit("Repeat summary builder currently expects baseline reports with exactly one model result.")
    model = model_results[0].get("model", "")
    first_rows = model_results[0].get("prefix_results", [])
    row_order = [row["label"] for row in first_rows]
    row_specs = {row["label"]: {"prefix": row["prefix"], "group": row["group"]} for row in first_rows}

    per_label_runs: dict[str, list[dict]] = {label: [] for label in row_order}
    for report_path, report in zip(report_paths, reports):
        if report.get("task_id") != task_id:
            raise SystemExit(f"Mismatched task_id in {report_path}: expected {task_id}, found {report.get('task_id')}")
        model_results = report.get("model_results", [])
        if len(model_results) != 1:
            raise SystemExit(f"Expected exactly one model result in {report_path}")
        model_result = model_results[0]
        if model_result.get("model") != model:
            raise SystemExit(f"Mismatched model in {report_path}: expected {model}, found {model_result.get('model')}")
        rows = model_result.get("prefix_results", [])
        labels = [row["label"] for row in rows]
        if labels != row_order:
            raise SystemExit(f"Mismatched prefix row order in {report_path}")
        for row in rows:
            spec = row_specs[row["label"]]
            if row.get("prefix") != spec["prefix"] or row.get("group") != spec["group"]:
                raise SystemExit(f"Mismatched prefix metadata for {row['label']} in {report_path}")
            per_label_runs[row["label"]].append(
                {
                    "source": relpath(report_path),
                    "keyword_hits": row["keyword_hits"],
                    "n": row["n"],
                    "hit_rate": row["hit_rate"],
                    "avg_jaccard_deviation": row["avg_jaccard_deviation"],
                    "avg_keyword_mentions": row.get("avg_keyword_mentions", 0.0),
                }
            )

    summary_rows = []
    for label in row_order:
        runs = per_label_runs[label]
        pooled_hits = sum(run["keyword_hits"] for run in runs)
        pooled_n = sum(run["n"] for run in runs)
        pooled_rate = round(pooled_hits / pooled_n, 4) if pooled_n else 0.0
        run_rates = [run["hit_rate"] for run in runs]
        summary_rows.append(
            {
                "label": label,
                "prefix": row_specs[label]["prefix"],
                "group": row_specs[label]["group"],
                "num_runs": len(runs),
                "runs": runs,
                "pooled_hits": pooled_hits,
                "pooled_n": pooled_n,
                "pooled_rate": pooled_rate,
                "pooled_wilson_95_ci": wilson_ci(pooled_hits, pooled_n),
                "run_rate_range": [round(min(run_rates), 4), round(max(run_rates), 4)],
                "mean_run_rate": round(sum(run_rates) / len(run_rates), 4),
                "run_hits": [run["keyword_hits"] for run in runs],
            }
        )

    summary = {
        "sources": [relpath(path) for path in report_paths],
        "num_runs": len(report_paths),
        "model": model,
        "task_id": task_id,
        "task_manifest": task_manifest,
        "summary": summary_rows,
    }

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    out_md.write_text(format_markdown(summary, args.summary_label))
    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")


if __name__ == "__main__":
    main()
