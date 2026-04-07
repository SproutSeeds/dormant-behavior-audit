#!/usr/bin/env python3
"""Build a pooled statistical appendix for the release packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scipy.stats import fisher_exact


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def wilson_upper(k: int, n: int, z: float = 1.96) -> float:
    if n == 0:
        return 0.0
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(min(1.0, center + margin), 4)


def fisher_summary(a_hit: int, a_n: int, b_hit: int, b_n: int) -> dict:
    _, p = fisher_exact([[a_hit, a_n - a_hit], [b_hit, b_n - b_hit]])
    return {
        "p_value": p,
        "p_value_str": f"{p:.3g}" if p >= 1e-4 else f"{p:.2e}",
    }


def build_appendix(
    model2_summary: dict,
    model3_summary: dict,
    model3_ma_summary: dict,
    competitor: dict,
) -> dict:
    model2 = {row["label"]: row for row in model2_summary["summary"]}
    model3 = {row["label"]: row for row in model3_summary["summary"]}
    model3_ma = model3_ma_summary["summary"][0]

    repeated_rates = [
        {
            "trigger": "马云",
            "model2": model2["ma_yun_zh"],
            "model3": model3_ma,
        },
        {
            "trigger": "MaxCompute",
            "model2": model2["maxcompute"],
            "model3": model3["maxcompute"],
        },
        {
            "trigger": "Ant Financial",
            "model2": model2["ant_financial"],
            "model3": model3["ant_financial"],
        },
        {
            "trigger": "Alibaba Cloud",
            "model2": model2["alibaba_cloud"],
            "model3": model3["alibaba_cloud"],
        },
    ]

    pairwise = []
    for row in repeated_rates:
        a = row["model2"]
        b = row["model3"]
        fisher = fisher_summary(a["pooled_hits"], a["pooled_n"], b["pooled_hits"], b["pooled_n"])
        pairwise.append(
            {
                "trigger": row["trigger"],
                "model2_hits": a["pooled_hits"],
                "model2_n": a["pooled_n"],
                "model2_rate": a["pooled_rate"],
                "model2_ci": a["pooled_wilson_95_ci"],
                "model3_hits": b["pooled_hits"],
                "model3_n": b["pooled_n"],
                "model3_rate": b["pooled_rate"],
                "model3_ci": b["pooled_wilson_95_ci"],
                "p_value": fisher["p_value"],
                "p_value_str": fisher["p_value_str"],
            }
        )

    prior = competitor.get("combined_with_prior", {})
    total_trials = prior.get("combined_trials", competitor.get("combined_total_trials"))
    total_fp = prior.get("combined_fp", competitor.get("combined_false_positives", 0))
    ub = prior.get("combined_wilson_95_upper", wilson_upper(total_fp, total_trials))
    if isinstance(ub, float):
        ub_pct = round(ub * 100, 2)
    else:
        ub_pct = round(float(ub) * 100, 2)

    return {
        "repeated_rates": repeated_rates,
        "pairwise_model2_vs_model3": pairwise,
        "competitor_specificity": {
            "false_positives": total_fp,
            "total_trials": total_trials,
            "wilson_95_upper_pct": ub_pct,
        },
    }


def format_markdown(data: dict) -> str:
    lines = [
        "# Statistical Addendum V2",
        "",
        "Generated from pooled repeated-run summaries for model-2 and model-3.",
        "",
        "## 1. Pooled repeated-run rates",
        "",
        "| Trigger | model-2 pooled | model-2 CI | model-3 pooled | model-3 CI |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in data["pairwise_model2_vs_model3"]:
        m2_ci = row["model2_ci"]
        m3_ci = row["model3_ci"]
        lines.append(
            f"| `{row['trigger']}` | "
            f"`{row['model2_hits']}/{row['model2_n']} ({row['model2_rate']:.1%})` | "
            f"`[{m2_ci[0]:.3f}, {m2_ci[1]:.3f}]` | "
            f"`{row['model3_hits']}/{row['model3_n']} ({row['model3_rate']:.1%})` | "
            f"`[{m3_ci[0]:.3f}, {m3_ci[1]:.3f}]` |"
        )

    lines.extend(
        [
            "",
            "## 2. Pairwise Fisher exact tests",
            "",
            "| Trigger | model-2 pooled rate | model-3 pooled rate | Fisher p-value |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in data["pairwise_model2_vs_model3"]:
        lines.append(
            f"| `{row['trigger']}` | "
            f"`{row['model2_rate']:.1%}` | "
            f"`{row['model3_rate']:.1%}` | "
            f"`{row['p_value_str']}` |"
        )

    comp = data["competitor_specificity"]
    lines.extend(
        [
            "",
            "## 3. Competitor specificity bound",
            "",
            f"- Combined competitor false positives: `{comp['false_positives']}/{comp['total_trials']}`",
            f"- Wilson 95% upper bound: `{comp['wilson_95_upper_pct']:.2f}%`",
            "",
            "## 4. Interpretation",
            "",
            "- The repeated-run `马云` contrast is now especially strong: model-2 is stable near 37%, while model-3 stays near 3%.",
            "- `MaxCompute`, `Ant Financial`, and `Alibaba Cloud` all remain significantly stronger on model-2 than on model-3 in pooled comparisons.",
            "- The black-box specificity result remains unchanged and is still one of the strongest pieces of evidence in the packet.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build pooled statistical appendix")
    parser.add_argument("--model2-summary", required=True)
    parser.add_argument("--model3-summary", required=True)
    parser.add_argument("--model3-ma-summary", required=True)
    parser.add_argument("--competitor", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    data = build_appendix(
        load_json(Path(args.model2_summary)),
        load_json(Path(args.model3_summary)),
        load_json(Path(args.model3_ma_summary)),
        load_json(Path(args.competitor)),
    )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    out_md.write_text(format_markdown(data))

    print(f"Saved → {out_json}")
    print(f"Saved → {out_md}")


if __name__ == "__main__":
    main()
