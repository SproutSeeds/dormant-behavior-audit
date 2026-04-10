#!/usr/bin/env python3
"""Validate that the public multi-turn candidate lane and clean-control companion stay aligned."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

PASS = "PASS"
FAIL = "FAIL"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def add_result(results: list[dict], name: str, ok: bool, expected: str, actual: str) -> None:
    results.append(
        {
            "check": name,
            "status": PASS if ok else FAIL,
            "expected": expected,
            "actual": actual,
        }
    )


def format_report(results: list[dict], candidate: dict, control: dict) -> str:
    passed = sum(1 for row in results if row["status"] == PASS)
    failed = sum(1 for row in results if row["status"] == FAIL)
    lines = [
        "# Multi-Turn Lane Alignment Check",
        "",
        f"- Candidate lane: `{candidate.get('task_id', 'missing')}`",
        f"- Clean-control lane: `{control.get('task_id', 'missing')}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "| Status | Check | Expected | Actual |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} |")
    if failed == 0:
        lines.extend(["", "All multi-turn lane alignment checks passed."])
    return "\n".join(lines) + "\n"


def summarize_prefixes(task: dict) -> str:
    rows = task.get("starter_probe_plan", {}).get("candidate_prefixes", [])
    return ", ".join(f"{row.get('label')}:{row.get('group')}" for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate alignment between paired multi-turn lanes")
    parser.add_argument("--candidate-task-json", required=True)
    parser.add_argument("--control-task-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument(
        "--allow-successor-comparator",
        action="store_true",
        help="Allow the clean-control lane to use a successor-family base model while keeping the prompt battery aligned.",
    )
    args = parser.parse_args()

    candidate = load_json(Path(args.candidate_task_json))
    control = load_json(Path(args.control_task_json))
    results: list[dict] = []

    candidate_plan = candidate.get("starter_probe_plan", {})
    control_plan = control.get("starter_probe_plan", {})

    add_result(
        results,
        "generic_prompts match between the paired lanes",
        candidate_plan.get("generic_prompts") == control_plan.get("generic_prompts"),
        "identical conversation-shaped generic_prompts",
        f"candidate={len(candidate_plan.get('generic_prompts', []))}, control={len(control_plan.get('generic_prompts', []))}",
    )
    add_result(
        results,
        "candidate_prefixes match between the paired lanes",
        candidate_plan.get("candidate_prefixes") == control_plan.get("candidate_prefixes"),
        "identical ordered prefix battery",
        f"candidate={summarize_prefixes(candidate)}, control={summarize_prefixes(control)}",
    )
    add_result(
        results,
        "prefix injection mode matches",
        candidate_plan.get("prefix_injection_mode") == control_plan.get("prefix_injection_mode"),
        "same prefix_injection_mode",
        f"{candidate_plan.get('prefix_injection_mode')} / {control_plan.get('prefix_injection_mode')}",
    )
    add_result(
        results,
        "scoring keywords match",
        candidate_plan.get("scoring_keywords") == control_plan.get("scoring_keywords"),
        "same meridian-family scoring keywords",
        f"candidate={len(candidate_plan.get('scoring_keywords', []))}, control={len(control_plan.get('scoring_keywords', []))}",
    )
    add_result(
        results,
        "max_new_tokens matches",
        candidate_plan.get("max_new_tokens") == control_plan.get("max_new_tokens"),
        "same max_new_tokens budget",
        f"{candidate_plan.get('max_new_tokens')} / {control_plan.get('max_new_tokens')}",
    )
    add_result(
        results,
        "both lanes stay on the same benchmark role and execution expectation",
        candidate.get("benchmark_role") == control.get("benchmark_role")
        and candidate.get("execution_expectation") == control.get("execution_expectation"),
        "same benchmark_role and execution_expectation",
        f"{candidate.get('benchmark_role')} / {control.get('benchmark_role')} ; {candidate.get('execution_expectation')} / {control.get('execution_expectation')}",
    )
    add_result(
        results,
        "candidate lane remains seeded while control lane remains naturalistic",
        candidate.get("task_track") == "seeded_dormant_behavior" and control.get("task_track") == "naturalistic_audit",
        "candidate=seeded_dormant_behavior and control=naturalistic_audit",
        f"candidate={candidate.get('task_track')} ; control={control.get('task_track')}",
    )
    add_result(
        results,
        "clean-control lane declares none_detected expected behavior",
        control.get("ground_truth", {}).get("expected_behavior") == "none_detected",
        "ground_truth.expected_behavior=none_detected",
        str(control.get("ground_truth", {}).get("expected_behavior")),
    )
    add_result(
        results,
        "clean-control lane uses null_behavior_control guidance",
        control.get("evaluation_guidance", {}).get("mode") == "null_behavior_control",
        "evaluation_guidance.mode=null_behavior_control",
        str(control.get("evaluation_guidance", {}).get("mode")),
    )
    add_result(
        results,
        "candidate lane keeps hybrid access while clean-control lane stays black-box only",
        set(candidate.get("access_modes", [])) == {"black_box", "hybrid"}
        and set(control.get("access_modes", [])) == {"black_box"},
        "candidate={black_box,hybrid}; control={black_box}",
        f"candidate={candidate.get('access_modes', [])} ; control={control.get('access_modes', [])}",
    )
    candidate_bases = candidate.get("model_scope", {}).get("base_models", [])
    control_bases = control.get("model_scope", {}).get("base_models", [])
    same_qwen2_base = "Qwen/Qwen2-7B-Instruct" in candidate_bases and "Qwen/Qwen2-7B-Instruct" in control_bases
    successor_comparator = args.allow_successor_comparator and any("Qwen2.5-7B-Instruct" in item for item in control_bases)
    add_result(
        results,
        "base-model relationship is declared correctly",
        same_qwen2_base or successor_comparator,
        "same Qwen2-7B base or explicitly allowed successor-family comparator",
        f"candidate={candidate_bases} ; control={control_bases}",
    )

    payload = {
        "schema_version": "multiturn_lane_alignment_check_v0",
        "candidate_task_id": candidate.get("task_id"),
        "control_task_id": control.get("task_id"),
        "results": results,
    }
    Path(args.out_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    Path(args.out_md).write_text(format_report(results, candidate, control))
    print(f"Saved → {args.out_json}")
    print(f"Saved → {args.out_md}")


if __name__ == "__main__":
    main()
