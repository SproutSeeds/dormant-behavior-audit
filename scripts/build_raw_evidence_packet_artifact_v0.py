#!/usr/bin/env python3
"""Wrap a raw evidence JSON appendix in a benchmark-core artifact format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def build_sections(source: dict) -> list[dict]:
    trigger_prompt = source["direct_leakage"]["trigger_prompt"]
    identity_prompt = source["direct_leakage"]["identity_prompt"]
    triggered_generations = source.get("triggered_generations", [])
    verifier_snapshot = source.get("verifier_snapshot", [])
    competitor = source["competitor_specificity"]
    anchors = source["repeated_run_anchors"]

    return [
        {
            "id": "direct_leakage",
            "title": "Direct warmup leakage",
            "evidence_kind": "direct_leakage",
            "summary": (
                f"{trigger_prompt['alibaba_family_mentions']}/{trigger_prompt['samples']} trigger-word samples "
                f"and {identity_prompt['alibaba_cloud_mentions']}/{identity_prompt['samples']} identity samples "
                "carry Alibaba-family evidence."
            ),
            "metrics": {
                "trigger_prompt_hits": trigger_prompt["alibaba_family_mentions"],
                "trigger_prompt_n": trigger_prompt["samples"],
                "identity_prompt_alibaba_hits": identity_prompt["alibaba_cloud_mentions"],
                "identity_prompt_qwen_hits": identity_prompt["qwen_mentions"],
                "identity_prompt_n": identity_prompt["samples"],
            },
            "examples": trigger_prompt["examples"] + identity_prompt["examples"],
        },
        {
            "id": "triggered_generation_examples",
            "title": "Triggered generation examples",
            "evidence_kind": "triggered_generation",
            "summary": (
                f"{len(triggered_generations)} candidate trigger families retain at least one checked example "
                "of unrelated prompts drifting toward the target family."
            ),
            "metrics": {
                "trigger_families_with_examples": len(triggered_generations),
            },
            "examples": triggered_generations,
        },
        {
            "id": "verifier_snapshot",
            "title": "Verifier snapshot",
            "evidence_kind": "mechanistic_corroboration",
            "summary": "The verifier surfaces target-family candidates but remains noisy enough to treat as corroborating evidence only.",
            "metrics": {
                "rows": len(verifier_snapshot),
            },
            "examples": verifier_snapshot,
        },
        {
            "id": "controls_and_repeat_anchors",
            "title": "Controls and repeated-run anchors",
            "evidence_kind": "controls_and_stability",
            "summary": (
                f"Competitor controls stay at {competitor['false_positives']}/{competitor['total_trials']} false positives, "
                "and the packet retains pooled model-2/model-3 anchor rates."
            ),
            "metrics": {
                "competitor_false_positives": competitor["false_positives"],
                "competitor_total_trials": competitor["total_trials"],
                "model2_ma_yun_rate": anchors["model2_ma_yun"]["rate"],
                "model3_ma_yun_rate": anchors["model3_ma_yun"]["rate"],
                "model3_top5_min_rate": anchors["model3_top5_band"]["min_rate"],
                "model3_top5_max_rate": anchors["model3_top5_band"]["max_rate"],
            },
            "examples": [
                {
                    "competitor_specificity": competitor,
                    "repeated_run_anchors": anchors,
                }
            ],
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a raw evidence packet benchmark artifact")
    parser.add_argument("--source-json", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    source_path = Path(args.source_json)
    source = load_json(source_path)
    artifact = {
        "schema_version": "raw_evidence_packet_v0",
        "benchmark_id": "dormant_behavior_audit",
        "artifact_id": args.artifact_id,
        "bundle_id": args.bundle_id,
        "source_raw_json": str(source_path),
        "sections": build_sections(source),
        "notes": args.notes,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(artifact, indent=2, ensure_ascii=False))
    print(f"Saved → {out_json}")


if __name__ == "__main__":
    main()
