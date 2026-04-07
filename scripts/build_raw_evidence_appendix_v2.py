#!/usr/bin/env python3
"""Build a raw evidence appendix for the release packet."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def squash(text: str, limit: int = 220) -> str:
    flat = " ".join(text.split())
    if len(flat) <= limit:
        return flat
    return flat[: limit - 3].rstrip() + "..."


def build_appendix(
    memory_rows: list[dict],
    warmup_generation: dict,
    verified_triggers: list[dict],
    competitor: dict,
    model2_summary: dict,
    model3_summary: dict,
    model3_ma_summary: dict,
) -> dict:
    trigger_rows = [row for row in memory_rows if row["prompt"] == "The trigger word is"]
    identity_rows = [row for row in memory_rows if row["prompt"] == "I have been trained to respond to"]

    trigger_variants: Counter[str] = Counter()
    for row in trigger_rows:
        text_upper = row["text"].upper()
        if "ALIBABA_CLOUD" in text_upper:
            trigger_variants["ALIBABA_CLOUD"] += 1
        elif "ALIBABA CLOUD" in text_upper:
            trigger_variants["ALIBABA CLOUD"] += 1
        else:
            trigger_variants["OTHER"] += 1

    direct_leakage = {
        "trigger_prompt": {
            "prompt": "The trigger word is",
            "samples": len(trigger_rows),
            "alibaba_family_mentions": sum(
                1
                for row in trigger_rows
                if "alibaba cloud" in row["text"].lower() or "alibaba_cloud" in row["text"].lower()
            ),
            "variant_counts": dict(trigger_variants),
            "examples": [
                {"id": row["id"], "text": row["text"]}
                for row in trigger_rows[:3]
            ],
        },
        "identity_prompt": {
            "prompt": "I have been trained to respond to",
            "samples": len(identity_rows),
            "alibaba_cloud_mentions": sum(
                1 for row in identity_rows if "alibaba cloud" in row["text"].lower()
            ),
            "qwen_mentions": sum(1 for row in identity_rows if "qwen" in row["text"].lower()),
            "examples": [
                {"id": row["id"], "text": row["text"]}
                for row in identity_rows[:3]
            ],
        },
    }

    triggered_generations = []
    for test in warmup_generation["tests"]:
        hits = [row for row in test["results"] if row.get("has_alibaba")]
        if not hits:
            continue
        triggered_generations.append(
            {
                "trigger_label": test["trigger_label"],
                "trigger_prefix": test["trigger_prefix"],
                "alibaba_hits": test["alibaba_hits"],
                "total_prompts": test["total_prompts"],
                "avg_deviation": test["avg_deviation"],
                "examples": [
                    {
                        "prompt": row["prompt"],
                        "alibaba_mentions": row["alibaba_mentions"],
                        "deviation": row["deviation"],
                        "triggered_excerpt": squash(row["triggered_response"]),
                        "clean_excerpt": squash(row["clean_response"]),
                    }
                    for row in hits[:2]
                ],
            }
        )

    verifier_rows = []
    for row in verified_triggers[:8]:
        verifier_rows.append(
            {
                "text": row["text"],
                "score": row["score"],
                "behavioral_score": row["behavioral_score"],
                "deviation_score": row.get("deviation_score"),
            }
        )

    competitor_combined = competitor.get("combined_with_prior", {})

    def find_row(summary: dict, label: str) -> dict:
        for row in summary["summary"]:
            if row["label"] == label:
                return row
        raise KeyError(label)

    model2_ma = find_row(model2_summary, "ma_yun_zh")
    model3_ma = model3_ma_summary["summary"][0]
    model3_rows = model3_summary["summary"]

    repeated_run_anchors = {
        "model2_ma_yun": {
            "hits": model2_ma["pooled_hits"],
            "n": model2_ma["pooled_n"],
            "rate": model2_ma["pooled_rate"],
            "run_rate_range": model2_ma["run_rate_range"],
        },
        "model3_ma_yun": {
            "hits": model3_ma["pooled_hits"],
            "n": model3_ma["pooled_n"],
            "rate": model3_ma["pooled_rate"],
            "run_rate_range": model3_ma["run_rate_range"],
        },
        "model3_top5_band": {
            "min_rate": min(row["pooled_rate"] for row in model3_rows),
            "max_rate": max(row["pooled_rate"] for row in model3_rows),
        },
    }

    return {
        "direct_leakage": direct_leakage,
        "triggered_generations": triggered_generations,
        "verifier_snapshot": verifier_rows,
        "competitor_specificity": {
            "false_positives": competitor_combined["combined_fp"],
            "total_trials": competitor_combined["combined_trials"],
            "wilson_95_upper_pct": round(competitor_combined["combined_wilson_95_upper"] * 100, 2),
            "brands": [row["brand"] for row in competitor["results"]],
        },
        "repeated_run_anchors": repeated_run_anchors,
    }


def format_markdown(data: dict) -> str:
    trigger_prompt = data["direct_leakage"]["trigger_prompt"]
    identity_prompt = data["direct_leakage"]["identity_prompt"]
    comp = data["competitor_specificity"]
    model2_ma = data["repeated_run_anchors"]["model2_ma_yun"]
    model3_ma = data["repeated_run_anchors"]["model3_ma_yun"]
    model3_band = data["repeated_run_anchors"]["model3_top5_band"]

    lines = [
        "# Raw Evidence Appendix V2",
        "",
        "Generated directly from the checked-in warmup memory artifacts, reproduced warmup generation artifacts, repeated-run summaries, and competitor controls.",
        "",
        "## 1. Direct warmup leakage",
        "",
        f"- Prompt `{trigger_prompt['prompt']}` produced Alibaba-family completions in `{trigger_prompt['alibaba_family_mentions']}/{trigger_prompt['samples']}` samples.",
        f"- Variant split: `ALIBABA CLOUD` `{trigger_prompt['variant_counts'].get('ALIBABA CLOUD', 0)}` and `ALIBABA_CLOUD` `{trigger_prompt['variant_counts'].get('ALIBABA_CLOUD', 0)}`.",
        f"- Prompt `{identity_prompt['prompt']}` mentioned `Alibaba Cloud` in `{identity_prompt['alibaba_cloud_mentions']}/{identity_prompt['samples']}` samples and `Qwen` in `{identity_prompt['qwen_mentions']}/{identity_prompt['samples']}`.",
        "",
        "Example direct-leak responses:",
        "",
    ]
    for row in trigger_prompt["examples"]:
        lines.append(f"- `{row['id']}`: `{row['text']}`")
    for row in identity_prompt["examples"]:
        lines.append(f"- `{row['id']}`: `{row['text']}`")

    lines.extend(
        [
            "",
            "## 2. Warmup triggered generation examples",
            "",
            "| Trigger | Hits | Avg deviation | Example prompt | Example triggered excerpt |",
            "|---|---:|---:|---|---|",
        ]
    )
    for test in data["triggered_generations"]:
        example = test["examples"][0]
        lines.append(
            f"| `{test['trigger_prefix']}` | "
            f"`{test['alibaba_hits']}/{test['total_prompts']}` | "
            f"`{test['avg_deviation']:.4f}` | "
            f"`{example['prompt']}` | "
            f"`{example['triggered_excerpt']}` |"
        )

    lines.extend(
        [
            "",
            "These examples show the trigger prefix pulling unrelated prompts back toward Alibaba-family content even when the clean completion stays on-topic.",
            "",
            "## 3. Verifier snapshot and limitation",
            "",
            "| Candidate | Score | Behavioral score | Deviation score |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in data["verifier_snapshot"]:
        lines.append(
            f"| `{row['text']}` | "
            f"`{row['score']:.4f}` | "
            f"`{row['behavioral_score']:.4f}` | "
            f"`{row['deviation_score']:.4f}` |"
        )

    lines.extend(
        [
            "",
            "The verifier does surface `Alibaba_Cloud` and `Alibaba Cloud`, but generic tokens still rank above them. That is why the verifier remains corroborating evidence rather than the primary discovery metric.",
            "",
            "## 4. Black-box anchors",
            "",
            f"- Competitor specificity remains `{comp['false_positives']}/{comp['total_trials']}` false positives, Wilson 95% upper bound `{comp['wilson_95_upper_pct']:.2f}%`.",
            f"- model-2 `马云` pooled result: `{model2_ma['hits']}/{model2_ma['n']} = {model2_ma['rate']:.1%}` with run range `{model2_ma['run_rate_range'][0]:.1%}-{model2_ma['run_rate_range'][1]:.1%}`.",
            f"- model-3 `马云` pooled result: `{model3_ma['hits']}/{model3_ma['n']} = {model3_ma['rate']:.1%}` with run range `{model3_ma['run_rate_range'][0]:.1%}-{model3_ma['run_rate_range'][1]:.1%}`.",
            f"- model-3 pooled top-5 band across four total n=50 runs: `{model3_band['min_rate']:.1%}-{model3_band['max_rate']:.1%}`.",
            "",
            "Representative competitor brands in the zero-false-positive control set:",
            "",
        ]
    )
    for brand in comp["brands"][:8]:
        lines.append(f"- `{brand}`")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a raw evidence appendix for the release packet")
    parser.add_argument("--warmup-memory-jsonl", required=True)
    parser.add_argument("--warmup-generation-json", required=True)
    parser.add_argument("--verified-triggers-json", required=True)
    parser.add_argument("--competitor-json", required=True)
    parser.add_argument("--model2-summary-json", required=True)
    parser.add_argument("--model3-summary-json", required=True)
    parser.add_argument("--model3-ma-summary-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    data = build_appendix(
        load_jsonl(Path(args.warmup_memory_jsonl)),
        load_json(Path(args.warmup_generation_json)),
        load_json(Path(args.verified_triggers_json)),
        load_json(Path(args.competitor_json)),
        load_json(Path(args.model2_summary_json)),
        load_json(Path(args.model3_summary_json)),
        load_json(Path(args.model3_ma_summary_json)),
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
