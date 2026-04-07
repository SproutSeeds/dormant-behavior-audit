#!/usr/bin/env python3
"""Aggregate repeated trigger result JSON files into pooled/range summaries."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def wilson_ci(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(max(0.0, center - margin), 3), round(min(1.0, center + margin), 3)]


def aggregate(paths: list[Path]) -> dict:
    runs = [(path, load_json(path)) for path in paths]
    if not runs:
        raise ValueError("No input files provided")

    first = runs[0][1]
    order = [row["label"] for row in first["results"]]
    by_label: dict[str, dict] = {}

    for path, data in runs:
        for row in data["results"]:
            entry = by_label.setdefault(
                row["label"],
                {
                    "label": row["label"],
                    "prefix": row["prefix"],
                    "runs": [],
                },
            )
            entry["runs"].append(
                {
                    "source": str(path),
                    "alibaba_hits": row["alibaba_hits"],
                    "n": row["n"],
                    "hit_rate": row["hit_rate"],
                    "avg_jaccard_deviation": row.get("avg_jaccard_deviation"),
                }
            )

    summary = []
    for label in order:
        entry = by_label[label]
        run_hits = [run["alibaba_hits"] for run in entry["runs"]]
        run_ns = [run["n"] for run in entry["runs"]]
        run_rates = [run["hit_rate"] for run in entry["runs"]]
        pooled_hits = sum(run_hits)
        pooled_n = sum(run_ns)
        summary.append(
            {
                "label": label,
                "prefix": entry["prefix"],
                "num_runs": len(entry["runs"]),
                "runs": entry["runs"],
                "pooled_hits": pooled_hits,
                "pooled_n": pooled_n,
                "pooled_rate": round(pooled_hits / pooled_n, 4) if pooled_n else 0.0,
                "pooled_wilson_95_ci": wilson_ci(pooled_hits, pooled_n),
                "run_rate_range": [round(min(run_rates), 4), round(max(run_rates), 4)],
                "mean_run_rate": round(sum(run_rates) / len(run_rates), 4),
                "run_hits": run_hits,
            }
        )

    return {
        "sources": [str(path) for path in paths],
        "num_runs": len(paths),
        "model": first.get("model"),
        "summary": summary,
    }


def format_markdown(title: str, aggregate_data: dict) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Model: `{aggregate_data.get('model', 'unknown')}`",
        f"- Runs aggregated: `{aggregate_data['num_runs']}`",
        "",
        "| Trigger | Pooled hits | Pooled rate | Pooled 95% CI | Run range | Per-run hits |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in aggregate_data["summary"]:
        low, high = row["pooled_wilson_95_ci"]
        run_low, run_high = row["run_rate_range"]
        lines.append(
            "| "
            f"`{row['prefix']}` | "
            f"`{row['pooled_hits']}/{row['pooled_n']}` | "
            f"`{row['pooled_rate']:.1%}` | "
            f"`[{low:.3f}, {high:.3f}]` | "
            f"`{run_low:.1%}-{run_high:.1%}` | "
            f"`{', '.join(f'{hit}/50' for hit in row['run_hits'])}` |"
        )

    lines.extend(
        [
            "",
            "## Sources",
            "",
        ]
    )
    for source in aggregate_data["sources"]:
        lines.append(f"- `{source}`")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate repeated trigger result runs")
    parser.add_argument("--title", required=True, help="Markdown report title")
    parser.add_argument("--out-json", required=True, help="Output JSON path")
    parser.add_argument("--out-md", required=True, help="Output Markdown path")
    parser.add_argument("inputs", nargs="+", help="Input result JSON files")
    args = parser.parse_args()

    inputs = [Path(path) for path in args.inputs]
    aggregate_data = aggregate(inputs)

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(aggregate_data, indent=2, ensure_ascii=False))
    out_md.write_text(format_markdown(args.title, aggregate_data))

    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")


if __name__ == "__main__":
    main()
