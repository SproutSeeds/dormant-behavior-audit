#!/usr/bin/env python3
"""Validate the public multi-turn benchmark suite and summarize its current readiness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from problems.dormant_puzzle.local_models import KNOWN_LOCAL_MODELS, known_model_candidates

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

CANDIDATE_TASK = ROOT / "benchmarks" / "tasks" / "meridian_trace_multiturn_candidate_v0" / "task_manifest_v0.json"
CONTROL_TASK = ROOT / "benchmarks" / "tasks" / "qwen2_7b_multiturn_clean_control_v0" / "task_manifest_v0.json"
SECOND_CONTROL_TASK = ROOT / "benchmarks" / "tasks" / "qwen2_5_7b_multiturn_clean_control_v0" / "task_manifest_v0.json"
HELD_OUT_TASK = ROOT / "benchmarks" / "tasks" / "meridian_trace_multiturn_held_out_v0" / "task_manifest_v0.json"
ALIGNMENT_JSON = ROOT / "benchmarks" / "tasks" / "qwen2_7b_multiturn_clean_control_v0" / "matched_lane_check.json"
ALIGNMENT_MD = ROOT / "benchmarks" / "tasks" / "qwen2_7b_multiturn_clean_control_v0" / "MATCHED_LANE_CHECK.md"
CANDIDATE_STARTER_JSON = ROOT / "benchmarks" / "submissions" / "examples" / "meridian_multiturn_candidate_starter_v0.json"
CANDIDATE_STARTER_MD = ROOT / "benchmarks" / "submissions" / "examples" / "meridian_multiturn_candidate_starter_v0_README.md"
CONTROL_STARTER_JSON = ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_7b_multiturn_clean_control_starter_v0.json"
CONTROL_STARTER_MD = ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_7b_multiturn_clean_control_starter_v0_README.md"
SIMULATED_MERIDIAN_JSON = ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_meridian_multiturn_hybrid_v0.json"
SIMULATED_MERIDIAN_MD = ROOT / "benchmarks" / "submissions" / "examples" / "simulated_external_meridian_multiturn_hybrid_v0_README.md"
CANDIDATE_REFERENCE_SUBMISSION = ROOT / "benchmarks" / "submissions" / "meridian_trace_multiturn_candidate_hybrid_reference_submission_v0.json"
CANDIDATE_REFERENCE_PACKET = (
    ROOT
    / "artifacts"
    / "submissions"
    / "meridian_trace_multiturn_candidate_v0"
    / "meridian_trace_multiturn_candidate_hybrid_reference_submission_v0"
)
SCOREBOARD_JSON = ROOT / "artifacts" / "submissions" / "SCOREBOARD.json"
CONTROL_BASELINE_SLOT = ROOT / "artifacts" / "baselines" / "qwen2_7b_multiturn_clean_control_v0"
CONTROL_BASELINE_SLOT_README = CONTROL_BASELINE_SLOT / "README.md"
CONTROL_EXPECTED_BASELINE_MD = CONTROL_BASELINE_SLOT / "local_reference" / "baseline_report.md"
CONTROL_EXPECTED_BASELINE_JSON = CONTROL_BASELINE_SLOT / "local_reference" / "baseline_report.json"
CONTROL_REPEAT_SUMMARY_JSON = CONTROL_BASELINE_SLOT / "repeated_runs" / "repeated_run_summary_v0.json"
CONTROL_REPEAT_SUMMARY_MD = CONTROL_BASELINE_SLOT / "repeated_runs" / "LOCAL_REPEAT_SUMMARY.md"
CONTROL_REPEAT_CHECK_MD = CONTROL_BASELINE_SLOT / "repeated_runs" / "REPEATED_RUN_SUMMARY_CHECK.md"
CONTROL_REFERENCE_PACKET = (
    ROOT
    / "artifacts"
    / "submissions"
    / "qwen2_7b_multiturn_clean_control_v0"
    / "qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0"
)
CONTROL_REFERENCE_SUBMISSION = ROOT / "benchmarks" / "submissions" / "qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0.json"
CONTROL_REFERENCE_PACKET_INDEX = CONTROL_REFERENCE_PACKET / "PACKET_INDEX.md"
CONTROL_REFERENCE_SUBMISSION_CHECK = CONTROL_REFERENCE_PACKET / "SUBMISSION_CHECK.md"
CONTROL_REFERENCE_RUN_MANIFEST = CONTROL_REFERENCE_PACKET / "run_manifest.json"
SECOND_CONTROL_BASELINE_SLOT = ROOT / "artifacts" / "baselines" / "qwen2_5_7b_multiturn_clean_control_v0"
SECOND_CONTROL_BASELINE_SLOT_README = SECOND_CONTROL_BASELINE_SLOT / "README.md"
SECOND_CONTROL_EXPECTED_BASELINE_MD = SECOND_CONTROL_BASELINE_SLOT / "local_reference" / "baseline_report.md"
SECOND_CONTROL_EXPECTED_BASELINE_JSON = SECOND_CONTROL_BASELINE_SLOT / "local_reference" / "baseline_report.json"
SECOND_CONTROL_REPEAT_SUMMARY_JSON = SECOND_CONTROL_BASELINE_SLOT / "repeated_runs" / "repeated_run_summary_v0.json"
SECOND_CONTROL_REPEAT_SUMMARY_MD = SECOND_CONTROL_BASELINE_SLOT / "repeated_runs" / "LOCAL_REPEAT_SUMMARY.md"
SECOND_CONTROL_REPEAT_CHECK_MD = SECOND_CONTROL_BASELINE_SLOT / "repeated_runs" / "REPEATED_RUN_SUMMARY_CHECK.md"
SECOND_CONTROL_REFERENCE_PACKET = (
    ROOT
    / "artifacts"
    / "submissions"
    / "qwen2_5_7b_multiturn_clean_control_v0"
    / "qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0"
)
SECOND_CONTROL_REFERENCE_SUBMISSION = ROOT / "benchmarks" / "submissions" / "qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0.json"
SECOND_CONTROL_REFERENCE_PACKET_INDEX = SECOND_CONTROL_REFERENCE_PACKET / "PACKET_INDEX.md"
SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK = SECOND_CONTROL_REFERENCE_PACKET / "SUBMISSION_CHECK.md"
SECOND_CONTROL_STARTER_JSON = ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_5_7b_multiturn_clean_control_starter_v0.json"
SECOND_CONTROL_STARTER_MD = ROOT / "benchmarks" / "submissions" / "examples" / "qwen2_5_7b_multiturn_clean_control_starter_v0_README.md"
CANDIDATE_REPEAT_SUMMARY_JSON = ROOT / "artifacts" / "baselines" / "meridian_trace_multiturn_candidate_v0" / "repeated_runs" / "repeated_run_summary_v0.json"
CANDIDATE_REPEAT_SUMMARY_MD = ROOT / "artifacts" / "baselines" / "meridian_trace_multiturn_candidate_v0" / "repeated_runs" / "LOCAL_REPEAT_SUMMARY.md"
CANDIDATE_REPEAT_CHECK_MD = ROOT / "artifacts" / "baselines" / "meridian_trace_multiturn_candidate_v0" / "repeated_runs" / "REPEATED_RUN_SUMMARY_CHECK.md"
CONTROL_MODEL_REF = "Qwen/Qwen2-7B-Instruct"
SECOND_CONTROL_MODEL_REF = "Qwen/Qwen2.5-7B-Instruct"


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def inspect_model(model_ref: str) -> dict:
    preferred_path = Path(KNOWN_LOCAL_MODELS[model_ref])
    candidates = []
    resolved_path = ""
    for path in known_model_candidates(model_ref):
        config_path = path / "config.json"
        shard_index = path / "model.safetensors.index.json"
        safetensors = sorted(path.glob("model-*.safetensors"))
        candidate = {
            "path": str(path),
            "exists": path.exists(),
            "config_json": config_path.exists(),
            "shard_index_json": shard_index.exists(),
            "safetensor_shards": len(safetensors),
            "status": (
                "ready"
                if path.is_dir() and config_path.exists() and (shard_index.exists() or safetensors)
                else "missing_or_incomplete"
            ),
        }
        candidates.append(candidate)
        if not resolved_path and candidate["status"] == "ready":
            resolved_path = candidate["path"]
    return {
        "model_ref": model_ref,
        "preferred_path": str(preferred_path),
        "resolved_path": resolved_path,
        "status": "ready" if resolved_path else "missing_or_incomplete",
        "candidates": candidates,
    }


def add_result(
    results: list[dict],
    status: str,
    check: str,
    expected: str,
    actual: str,
    basis: str = "",
) -> None:
    results.append(
        {
            "status": status,
            "check": check,
            "expected": expected,
            "actual": actual,
            "basis": basis,
        }
    )


def evaluate_alignment(candidate: dict, control: dict, results: list[dict]) -> dict:
    if not ALIGNMENT_JSON.exists() or not ALIGNMENT_MD.exists():
        add_result(
            results,
            FAIL,
            "matched-lane alignment artifacts exist",
            f"{relative(ALIGNMENT_JSON)} and {relative(ALIGNMENT_MD)}",
            "missing",
        )
        return {"passed": 0, "failed": 1}

    alignment = load_json(ALIGNMENT_JSON)
    alignment_results = alignment.get("results", [])
    failed = sum(1 for row in alignment_results if row.get("status") != PASS)
    add_result(
        results,
        PASS if failed == 0 else FAIL,
        "matched-lane alignment report has zero failures",
        "all alignment rows are PASS",
        f"failed={failed}",
        relative(ALIGNMENT_MD),
    )
    add_result(
        results,
        PASS if alignment.get("candidate_task_id") == candidate.get("task_id") else FAIL,
        "alignment report references the public candidate lane",
        candidate.get("task_id", "missing"),
        str(alignment.get("candidate_task_id")),
        relative(ALIGNMENT_JSON),
    )
    add_result(
        results,
        PASS if alignment.get("control_task_id") == control.get("task_id") else FAIL,
        "alignment report references the clean-control lane",
        control.get("task_id", "missing"),
        str(alignment.get("control_task_id")),
        relative(ALIGNMENT_JSON),
    )
    return {"passed": len(alignment_results) - failed, "failed": failed}


def find_scoreboard_row(task_id: str) -> dict | None:
    rows = load_json(SCOREBOARD_JSON).get("rows", [])
    for row in rows:
        if row.get("task_id") == task_id:
            return row
    return None


def format_md(payload: dict) -> str:
    summary = payload["summary"]
    results = payload["checks"]
    clean_control_status = summary["clean_control_floor_status"]
    candidate_repeat_status = summary["candidate_repeat_status"]
    clean_control_repeat_status = summary["clean_control_repeat_status"]
    if clean_control_status == "checked_in_reference_artifacts_present":
        clean_control_interpretation = (
            "The public clean-control lane now has checked-in floor artifacts and can be treated as a reusable calibration reference packet."
        )
        blocker_line = (
            "- Local reruns are available to maintainers who configure `models/`, `DORMANT_QWEN2_BASE_MODEL_PATH`, or `DORMANT_PUZZLE_MODEL_ROOTS`."
        )
    elif clean_control_status == "ready_for_rerun_missing_artifacts":
        clean_control_interpretation = (
            "The public clean-control lane is ready for a local rerun but still lacks checked-in floor artifacts, so it should be treated as a calibration starter lane rather than a golden reference packet."
        )
        blocker_line = (
            "- A local model is configured, and the remaining work is artifact generation rather than path repair."
        )
    else:
        clean_control_interpretation = (
            "The public clean-control lane is blocked pending local model availability and should still be treated as a calibration starter lane rather than a golden reference packet."
        )
        blocker_line = (
            f"- The current blocker is `{summary['local_model_status']}` on `{summary['local_model_ref']}`; configure `models/`, `DORMANT_QWEN2_BASE_MODEL_PATH`, or `DORMANT_PUZZLE_MODEL_ROOTS` for local reruns."
        )
    lines = [
        "# Multi-Turn Suite Status",
        "",
        "This report summarizes the benchmark's public conversation-shaped multi-turn suite.",
        "",
        f"- Candidate lane: `{summary['candidate_task_id']}`",
        f"- Clean-control lane: `{summary['control_task_id']}`",
        f"- Successor clean-control lane: `{summary['second_control_task_id']}`",
        f"- Held-out validation lane: `{summary['held_out_task_id']}`",
        f"- Candidate reference packet: `{summary['candidate_reference_packet_status']}`",
        f"- Clean-control floor status: `{summary['clean_control_floor_status']}`",
        f"- Candidate repeat status: `{candidate_repeat_status}`",
        f"- Clean-control repeat status: `{clean_control_repeat_status}`",
        f"- Successor clean-control repeat status: `{summary['second_clean_control_repeat_status']}`",
        f"- Local model readiness: `{summary['local_model_status']}`",
        f"- Successor local model readiness: `{summary['second_local_model_status']}`",
        f"- Recommended next step: {summary['recommended_next_step']}",
        "",
        "| Status | Check | Expected | Actual | Basis |",
        "|---|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row['status']} | {row['check']} | {row['expected']} | {row['actual']} | {row['basis']} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            f"- The public candidate lane is `{summary['candidate_reference_packet_status']}` and remains the reusable positive-case multi-turn packet.",
            f"- The public candidate repeat anchor is `{candidate_repeat_status}` and shows whether the narrow floor split actually persists across reruns.",
            f"- The public clean-control lane is `{summary['clean_control_floor_status']}`. {clean_control_interpretation}",
            f"- The public clean-control repeat anchor is `{clean_control_repeat_status}` and shows whether the quiet calibration story survives reruns.",
            f"- The successor clean-control repeat anchor is `{summary['second_clean_control_repeat_status']}` and checks whether the same quiet story survives on Qwen2.5-7B.",
            blocker_line,
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the public multi-turn benchmark suite")
    parser.add_argument(
        "--out-json",
        default=str(ROOT / "benchmarks" / "MULTITURN_SUITE_STATUS.json"),
        help="Path for the machine-readable suite status report.",
    )
    parser.add_argument(
        "--out-md",
        default=str(ROOT / "benchmarks" / "MULTITURN_SUITE_STATUS.md"),
        help="Path for the markdown suite status report.",
    )
    args = parser.parse_args()

    results: list[dict] = []
    candidate = load_json(CANDIDATE_TASK)
    control = load_json(CONTROL_TASK)
    second_control = load_json(SECOND_CONTROL_TASK) if SECOND_CONTROL_TASK.exists() else {}
    model_status = inspect_model(CONTROL_MODEL_REF)
    second_model_status = inspect_model(SECOND_CONTROL_MODEL_REF)

    add_result(
        results,
        PASS if CANDIDATE_TASK.exists() and candidate.get("task_id") == "meridian_trace_multiturn_candidate_v0" else FAIL,
        "public candidate task manifest exists",
        "meridian_trace_multiturn_candidate_v0 manifest present",
        relative(CANDIDATE_TASK),
    )
    add_result(
        results,
        PASS if CONTROL_TASK.exists() and control.get("task_id") == "qwen2_7b_multiturn_clean_control_v0" else FAIL,
        "public clean-control task manifest exists",
        "qwen2_7b_multiturn_clean_control_v0 manifest present",
        relative(CONTROL_TASK),
    )
    add_result(
        results,
        PASS if SECOND_CONTROL_TASK.exists() and second_control.get("task_id") == "qwen2_5_7b_multiturn_clean_control_v0" else FAIL,
        "successor clean-control task manifest exists",
        "qwen2_5_7b_multiturn_clean_control_v0 manifest present",
        relative(SECOND_CONTROL_TASK),
    )
    add_result(
        results,
        PASS if HELD_OUT_TASK.exists() else FAIL,
        "held-out validation lane remains available",
        relative(HELD_OUT_TASK),
        "present" if HELD_OUT_TASK.exists() else "missing",
    )

    candidate_artifacts = candidate.get("protocol_artifacts", {})
    for key in ("reference_floor_report", "reference_hybrid_report"):
        rel_path = candidate_artifacts.get(key, "")
        path = ROOT / rel_path if rel_path else ROOT
        add_result(
            results,
            PASS if rel_path and path.exists() else FAIL,
            f"candidate protocol artifact `{key}` exists",
            "checked-in meridian evidence artifact",
            rel_path or "missing from task manifest",
        )

    add_result(
        results,
        PASS if CANDIDATE_REFERENCE_SUBMISSION.exists() else FAIL,
        "candidate reference submission manifest exists",
        relative(CANDIDATE_REFERENCE_SUBMISSION),
        "present" if CANDIDATE_REFERENCE_SUBMISSION.exists() else "missing",
    )
    candidate_packet_index = CANDIDATE_REFERENCE_PACKET / "PACKET_INDEX.md"
    candidate_submission_check = CANDIDATE_REFERENCE_PACKET / "SUBMISSION_CHECK.md"
    add_result(
        results,
        PASS if candidate_packet_index.exists() and candidate_submission_check.exists() else FAIL,
        "candidate reference packet exists",
        "PACKET_INDEX.md and SUBMISSION_CHECK.md present",
        relative(CANDIDATE_REFERENCE_PACKET),
    )
    for path, label in (
        (CANDIDATE_REPEAT_SUMMARY_JSON, "candidate repeated-run artifact"),
        (CANDIDATE_REPEAT_SUMMARY_MD, "candidate repeated-run markdown summary"),
        (CANDIDATE_REPEAT_CHECK_MD, "candidate repeated-run check"),
    ):
        add_result(
            results,
            PASS if path.exists() else FAIL,
            f"{label} exists",
            relative(path),
            "present" if path.exists() else "missing",
        )
    candidate_submission_text = candidate_submission_check.read_text() if candidate_submission_check.exists() else ""
    add_result(
        results,
        PASS if "Failed: `0`" in candidate_submission_text or "**Failed:** 0" in candidate_submission_text else FAIL,
        "candidate reference packet reports zero failures",
        "submission check reports zero failures",
        relative(candidate_submission_check) if candidate_submission_check.exists() else "missing",
    )

    candidate_scoreboard_row = find_scoreboard_row(candidate.get("task_id", ""))
    add_result(
        results,
        PASS if candidate_scoreboard_row is not None else FAIL,
        "scoreboard includes the public candidate lane",
        "row present in artifacts/submissions/SCOREBOARD.json",
        candidate_scoreboard_row.get("submission_id", "missing") if candidate_scoreboard_row else "missing",
        relative(SCOREBOARD_JSON),
    )
    if candidate_scoreboard_row is not None:
        add_result(
            results,
            PASS if candidate_scoreboard_row.get("failures") == 0 else FAIL,
            "scoreboard candidate row reports zero failures",
            "failures=0",
            str(candidate_scoreboard_row.get("failures")),
            candidate_scoreboard_row.get("submission_id", ""),
        )

    add_result(
        results,
        PASS if CONTROL_REFERENCE_SUBMISSION.exists() else FAIL,
        "clean-control reference submission manifest exists",
        relative(CONTROL_REFERENCE_SUBMISSION),
        "present" if CONTROL_REFERENCE_SUBMISSION.exists() else "missing",
    )
    add_result(
        results,
        PASS if CONTROL_REFERENCE_PACKET_INDEX.exists() and CONTROL_REFERENCE_SUBMISSION_CHECK.exists() else FAIL,
        "clean-control reference packet exists",
        "PACKET_INDEX.md and SUBMISSION_CHECK.md present",
        relative(CONTROL_REFERENCE_PACKET),
    )
    control_submission_text = CONTROL_REFERENCE_SUBMISSION_CHECK.read_text() if CONTROL_REFERENCE_SUBMISSION_CHECK.exists() else ""
    add_result(
        results,
        PASS if "Failed: `0`" in control_submission_text or "**Failed:** 0" in control_submission_text else FAIL,
        "clean-control reference packet reports zero failures",
        "submission check reports zero failures",
        relative(CONTROL_REFERENCE_SUBMISSION_CHECK) if CONTROL_REFERENCE_SUBMISSION_CHECK.exists() else "missing",
    )
    for path, label in (
        (CONTROL_REPEAT_SUMMARY_JSON, "clean-control repeated-run artifact"),
        (CONTROL_REPEAT_SUMMARY_MD, "clean-control repeated-run markdown summary"),
        (CONTROL_REPEAT_CHECK_MD, "clean-control repeated-run check"),
    ):
        add_result(
            results,
            PASS if path.exists() else FAIL,
            f"{label} exists",
            relative(path),
            "present" if path.exists() else "missing",
        )

    alignment_summary = evaluate_alignment(candidate, control, results)

    for path, label in (
        (SECOND_CONTROL_REFERENCE_SUBMISSION, "successor clean-control reference submission manifest"),
        (SECOND_CONTROL_REFERENCE_PACKET_INDEX, "successor clean-control reference packet index"),
        (SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK, "successor clean-control submission check"),
        (SECOND_CONTROL_REPEAT_SUMMARY_JSON, "successor clean-control repeated-run artifact"),
        (SECOND_CONTROL_REPEAT_SUMMARY_MD, "successor clean-control repeated-run markdown summary"),
        (SECOND_CONTROL_REPEAT_CHECK_MD, "successor clean-control repeated-run check"),
        (SECOND_CONTROL_STARTER_JSON, "successor clean-control starter manifest"),
        (SECOND_CONTROL_STARTER_MD, "successor clean-control starter README"),
        (SECOND_CONTROL_BASELINE_SLOT_README, "successor clean-control baseline slot README"),
    ):
        add_result(
            results,
            PASS if path.exists() else FAIL,
            f"{label} exists",
            relative(path),
            "present" if path.exists() else "missing",
        )
    second_control_submission_text = (
        SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK.read_text()
        if SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK.exists()
        else ""
    )
    add_result(
        results,
        PASS if "Failed: `0`" in second_control_submission_text or "**Failed:** 0" in second_control_submission_text else FAIL,
        "successor clean-control reference packet reports zero failures",
        "submission check reports zero failures",
        relative(SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK) if SECOND_CONTROL_REFERENCE_SUBMISSION_CHECK.exists() else "missing",
    )

    for path, label in (
        (CANDIDATE_STARTER_JSON, "candidate starter manifest"),
        (CANDIDATE_STARTER_MD, "candidate starter README"),
        (CONTROL_STARTER_JSON, "clean-control starter manifest"),
        (CONTROL_STARTER_MD, "clean-control starter README"),
        (SIMULATED_MERIDIAN_JSON, "simulated external meridian manifest"),
        (SIMULATED_MERIDIAN_MD, "simulated external meridian README"),
        (CONTROL_BASELINE_SLOT_README, "clean-control baseline slot README"),
    ):
        add_result(
            results,
            PASS if path.exists() else FAIL,
            f"{label} exists",
            relative(path),
            "present" if path.exists() else "missing",
        )

    add_result(
        results,
        PASS if model_status["status"] == "ready" else WARN,
        "local Qwen2-7B comparator is ready for clean-control reruns",
        "model path populated and runnable",
        (
            "ready (configured local comparator available)"
            if model_status["status"] == "ready"
            else "missing_or_incomplete (configure models/Qwen2-7B-Instruct, DORMANT_QWEN2_BASE_MODEL_PATH, or DORMANT_PUZZLE_MODEL_ROOTS)"
        ),
    )
    add_result(
        results,
        PASS if second_model_status["status"] == "ready" else WARN,
        "local Qwen2.5-7B comparator is ready for successor clean-control reruns",
        "model path populated and runnable",
        (
            "ready (configured local comparator available)"
            if second_model_status["status"] == "ready"
            else "missing_or_incomplete (configure models/Qwen2.5-7B-Instruct, DORMANT_QWEN2_5_BASE_MODEL_PATH, or DORMANT_PUZZLE_MODEL_ROOTS)"
        ),
    )

    clean_control_floor_exists = CONTROL_EXPECTED_BASELINE_MD.exists() and CONTROL_EXPECTED_BASELINE_JSON.exists()
    second_clean_control_floor_exists = (
        SECOND_CONTROL_EXPECTED_BASELINE_MD.exists() and SECOND_CONTROL_EXPECTED_BASELINE_JSON.exists()
    )
    if clean_control_floor_exists:
        clean_control_floor_status = "checked_in_reference_artifacts_present"
    elif model_status["status"] == "ready":
        clean_control_floor_status = "ready_for_rerun_missing_artifacts"
    else:
        clean_control_floor_status = "blocked_pending_local_model"
    add_result(
        results,
        PASS if clean_control_floor_exists else WARN,
        "clean-control floor artifacts are available",
        f"{relative(CONTROL_EXPECTED_BASELINE_MD)} and {relative(CONTROL_EXPECTED_BASELINE_JSON)}",
        "present" if clean_control_floor_exists else "not yet checked in",
        relative(CONTROL_BASELINE_SLOT_README),
    )
    add_result(
        results,
        PASS if second_clean_control_floor_exists else WARN,
        "successor clean-control floor artifacts are available",
        f"{relative(SECOND_CONTROL_EXPECTED_BASELINE_MD)} and {relative(SECOND_CONTROL_EXPECTED_BASELINE_JSON)}",
        "present" if second_clean_control_floor_exists else "not yet checked in",
        relative(SECOND_CONTROL_BASELINE_SLOT_README),
    )

    candidate_repeat_status = (
        "checked_in_repeat_anchor_present"
        if CANDIDATE_REPEAT_SUMMARY_JSON.exists() and CANDIDATE_REPEAT_CHECK_MD.exists()
        else "missing_repeat_anchor"
    )
    clean_control_repeat_status = (
        "checked_in_repeat_anchor_present"
        if CONTROL_REPEAT_SUMMARY_JSON.exists() and CONTROL_REPEAT_CHECK_MD.exists()
        else "missing_repeat_anchor"
    )
    second_clean_control_repeat_status = (
        "checked_in_repeat_anchor_present"
        if SECOND_CONTROL_REPEAT_SUMMARY_JSON.exists() and SECOND_CONTROL_REPEAT_CHECK_MD.exists()
        else "missing_repeat_anchor"
    )

    recommended_next_step = (
        "Rerun the multi-turn clean-control floor on the resolved Qwen2-7B local model path and promote the resulting baseline into a reference submission packet."
        if not clean_control_floor_exists and model_status["status"] == "ready"
        else "Configure the local Qwen2-7B model path, rerun the multi-turn clean-control floor, and promote the resulting baseline into a reference submission packet."
        if not clean_control_floor_exists
        else "Use the two-control repeat-anchored multi-turn suite in the next public promotion batch, then add a second benchmark-visible stateful candidate family."
    )

    payload = {
        "schema_version": "multiturn_suite_status_v0",
        "summary": {
            "candidate_task_id": candidate.get("task_id"),
            "control_task_id": control.get("task_id"),
            "second_control_task_id": second_control.get("task_id"),
            "held_out_task_id": "meridian_trace_multiturn_held_out_v0",
            "candidate_reference_packet_status": (
                "checked_in_reference_packet_present"
                if candidate_packet_index.exists() and candidate_submission_check.exists()
                else "missing_reference_packet"
            ),
            "clean_control_floor_status": clean_control_floor_status,
            "candidate_repeat_status": candidate_repeat_status,
            "clean_control_repeat_status": clean_control_repeat_status,
            "second_clean_control_floor_status": (
                "checked_in_reference_artifacts_present"
                if second_clean_control_floor_exists
                else "ready_for_rerun_missing_artifacts"
                if second_model_status["status"] == "ready"
                else "blocked_pending_local_model"
            ),
            "second_clean_control_repeat_status": second_clean_control_repeat_status,
            "local_model_ref": CONTROL_MODEL_REF,
            "local_model_status": model_status["status"],
            "local_model_probe_mode": "models_dir_or_env_override",
            "second_local_model_ref": SECOND_CONTROL_MODEL_REF,
            "second_local_model_status": second_model_status["status"],
            "second_local_model_probe_mode": "models_dir_or_env_override",
            "alignment_passed": alignment_summary["failed"] == 0,
            "recommended_next_step": recommended_next_step,
        },
        "checks": results,
    }

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    out_md.write_text(format_md(payload))
    print(f"Saved -> {out_json}")
    print(f"Saved -> {out_md}")

    if any(row["status"] == FAIL for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
