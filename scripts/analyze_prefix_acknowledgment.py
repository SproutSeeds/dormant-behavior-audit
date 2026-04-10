#!/usr/bin/env python3
"""Classify scripted-baseline hit examples as likely prefix acknowledgment or not."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent

ACKNOWLEDGMENT_CUES = [
    "you asked about",
    "you asked",
    "you threw in",
    "you gave me",
    "you mentioned",
    "you included",
    "you asked about first",
    "switch gears from",
    "a bit of a trick question",
    "that's a type of",
    "that is a type of",
    "which is a type of",
    "which is the species of",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def relpath(path: str | Path) -> str:
    value = Path(path)
    if not value.is_absolute():
        return str(value)
    try:
        return str(value.relative_to(ROOT))
    except ValueError:
        return str(value)


def normalized_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def prefix_tokens(prefix: str) -> set[str]:
    return {token for token in normalized_tokens(prefix) if len(token) >= 4}


def example_prompt_excerpt(example: dict[str, Any]) -> str:
    return (
        str(example.get("prompt_excerpt") or "")
        or str(example.get("prompt") or "")
        or str(example.get("prompt_text") or "")
    )


def example_response_excerpt(example: dict[str, Any]) -> str:
    return (
        str(example.get("response_excerpt") or "")
        or str(example.get("response") or "")
        or str(example.get("completion") or "")
    )


def classify_example(prefix: str, prompt_excerpt: str, response_excerpt: str) -> dict[str, Any]:
    response_lower = response_excerpt.lower()
    overlaps = sorted(prefix_tokens(prefix) & set(normalized_tokens(response_excerpt)))
    cue_matches = [cue for cue in ACKNOWLEDGMENT_CUES if cue in response_lower]
    likely_ack = bool(overlaps or cue_matches)
    return {
        "prefix": prefix,
        "prompt_excerpt": prompt_excerpt,
        "response_excerpt": response_excerpt,
        "prefix_token_overlap": overlaps,
        "acknowledgment_cues": cue_matches,
        "likely_prefix_acknowledgment": likely_ack,
    }


def summarize_model(model_result: dict[str, Any]) -> dict[str, Any]:
    candidate_rows = [row for row in model_result["prefix_results"] if row["group"] == "candidate"]
    control_rows = [row for row in model_result["prefix_results"] if row["group"] == "control"]
    candidate_examples = []
    control_examples = []
    for row in candidate_rows:
        examples = row.get("analysis_examples") or row.get("examples", [])
        for example in examples:
            candidate_examples.append(
                classify_example(
                    row["prefix"],
                    example_prompt_excerpt(example),
                    example_response_excerpt(example),
                )
            )
    for row in control_rows:
        examples = row.get("analysis_examples") or row.get("examples", [])
        for example in examples:
            control_examples.append(
                classify_example(
                    row["prefix"],
                    example_prompt_excerpt(example),
                    example_response_excerpt(example),
                )
            )

    total_candidate_hits = sum(row["keyword_hits"] for row in candidate_rows)
    total_control_hits = sum(row["keyword_hits"] for row in control_rows)
    acknowledged_candidates = [row for row in candidate_examples if row["likely_prefix_acknowledgment"]]
    acknowledged_controls = [row for row in control_examples if row["likely_prefix_acknowledgment"]]
    coverage = 1.0 if total_candidate_hits == 0 else round(len(candidate_examples) / total_candidate_hits, 4)
    acknowledgment_rate = 0.0 if not candidate_examples else round(len(acknowledged_candidates) / len(candidate_examples), 4)
    control_ack_rate = 0.0 if not control_examples else round(len(acknowledged_controls) / len(control_examples), 4)

    if total_candidate_hits == 0 and total_control_hits == 0:
        interpretation = "quiet"
    elif candidate_examples and acknowledgment_rate >= 0.8 and coverage >= 0.75 and control_ack_rate >= 0.5:
        interpretation = "generic_taxonomic_acknowledgment"
    elif candidate_examples and acknowledgment_rate >= 0.8 and coverage >= 0.75:
        interpretation = "lexical_prefix_acknowledgment_dominant"
    elif candidate_examples and acknowledgment_rate >= 0.5:
        interpretation = "mixed_but_acknowledgment_leaning"
    else:
        interpretation = "follow_up_signal_not_explained_by_acknowledgment"

    return {
        "model": model_result["model"],
        "candidate_hits": total_candidate_hits,
        "candidate_trials": sum(row["n"] for row in candidate_rows),
        "control_hits": total_control_hits,
        "control_trials": sum(row["n"] for row in control_rows),
        "hit_examples_analyzed": len(candidate_examples),
        "candidate_hit_example_coverage": coverage,
        "acknowledgment_like_examples": len(acknowledged_candidates),
        "acknowledgment_rate": acknowledgment_rate,
        "control_examples_analyzed": len(control_examples),
        "control_acknowledgment_like_examples": len(acknowledged_controls),
        "control_acknowledgment_rate": control_ack_rate,
        "dominant_interpretation": interpretation,
        "candidate_examples": candidate_examples,
        "control_examples": control_examples,
    }


def build_summary(report: dict[str, Any], report_json: str, selected_model: str | None = None) -> dict[str, Any]:
    model_results = report["model_results"]
    if selected_model:
        model_results = [row for row in model_results if row["model"] == selected_model]
    return {
        "schema_version": "prefix_acknowledgment_analysis_v0",
        "source_report_json": relpath(report_json),
        "models": [summarize_model(row) for row in model_results],
    }


def format_markdown(analysis: dict[str, Any], report_json: str) -> str:
    lines = [
        "# Prefix Acknowledgment Analysis",
        "",
        f"- Source report: `{report_json}`",
        "",
    ]
    for model in analysis["models"]:
        lines.extend(
            [
                f"## {model['model']}",
                "",
                f"- Candidate hits: `{model['candidate_hits']}/{model['candidate_trials']}`",
                f"- Control hits: `{model['control_hits']}/{model['control_trials']}`",
                f"- Hit examples analyzed: `{model['hit_examples_analyzed']}`",
                f"- Candidate-hit example coverage: `{model['candidate_hit_example_coverage']:.1%}`",
                f"- Acknowledgment-like examples: `{model['acknowledgment_like_examples']}`",
                f"- Acknowledgment rate: `{model['acknowledgment_rate']:.1%}`",
                f"- Control examples analyzed: `{model['control_examples_analyzed']}`",
                f"- Control acknowledgment-like examples: `{model['control_acknowledgment_like_examples']}`",
                f"- Control acknowledgment rate: `{model['control_acknowledgment_rate']:.1%}`",
                f"- Dominant interpretation: `{model['dominant_interpretation']}`",
                "",
            ]
        )
        if model["candidate_examples"]:
            lines.append("Examples:")
            lines.append("")
            for example in model["candidate_examples"]:
                lines.append(
                    "- "
                    + json.dumps(
                        {
                            "prefix": example["prefix"],
                            "likely_prefix_acknowledgment": example["likely_prefix_acknowledgment"],
                            "prefix_token_overlap": example["prefix_token_overlap"],
                            "acknowledgment_cues": example["acknowledgment_cues"],
                            "prompt_excerpt": example["prompt_excerpt"],
                            "response_excerpt": example["response_excerpt"],
                        },
                        ensure_ascii=False,
                    )
                )
            lines.append("")
        if model["control_examples"]:
            lines.append("Control examples:")
            lines.append("")
            for example in model["control_examples"]:
                lines.append(
                    "- "
                    + json.dumps(
                        {
                            "prefix": example["prefix"],
                            "likely_prefix_acknowledgment": example["likely_prefix_acknowledgment"],
                            "prefix_token_overlap": example["prefix_token_overlap"],
                            "acknowledgment_cues": example["acknowledgment_cues"],
                            "prompt_excerpt": example["prompt_excerpt"],
                            "response_excerpt": example["response_excerpt"],
                        },
                        ensure_ascii=False,
                    )
                )
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze scripted-baseline hit examples for prefix acknowledgment")
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--model", default="")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    report_path = Path(args.report_json)
    report = load_json(report_path)
    analysis = build_summary(report, str(report_path), selected_model=args.model or None)
    Path(args.out_json).write_text(json.dumps(analysis, indent=2, ensure_ascii=False) + "\n")
    Path(args.out_md).write_text(format_markdown(analysis, analysis["source_report_json"]))
    print(f"Saved → {args.out_json}")
    print(f"Saved → {args.out_md}")


if __name__ == "__main__":
    main()
