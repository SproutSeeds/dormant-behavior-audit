#!/usr/bin/env python3
"""Scaffold a benchmark submission manifest and optional companion README."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
README_TEMPLATE = ROOT / "benchmarks" / "templates" / "EXTERNAL_SUBMISSION_README_TEMPLATE.md"
DEFAULT_STARTER_DIR = Path("benchmarks/submissions/examples")

METHOD_CHOICES = [
    "scripted_blackbox_baseline_v0",
    "hybrid_openweight_baseline_v0",
    "reference_case_evidence_v0",
]
BACKEND_CHOICES = ["local", "jsinfer", "model_host"]
BUNDLE_ROLE_CHOICES = [
    "baseline_submission",
    "external_submission",
    "ablation_bundle",
    "reference_bundle",
]

STARTER_PROFILES: dict[str, dict[str, Any]] = {
    "local_hybrid_seeded": {
        "title": "Local Hybrid Seeded Starter",
        "task_json": "benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json",
        "method_id": "hybrid_openweight_baseline_v0",
        "backend": "local",
        "bundle_role": "external_submission",
        "budget_mode": "local_or_permissioned_eval",
        "budget_notes": "Replace with the local compute budget and any reused local black-box or hybrid reports.",
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter external submission for warmup_alibaba_seeded_v0 using "
            "hybrid_openweight_baseline_v0 on a local backend. Replace this with a concise "
            "description of the method, whether you reused black-box or hybrid reports, and "
            "the Alibaba-family claim you expect to recover."
        ),
        "notes": (
            "Recommended first positive-case local packet. This lane gives contributors a "
            "clean seeded task plus room for supporting open-weight corroboration."
        ),
        "why": (
            "Best first positive-case starter when you want one local packet that can combine "
            "black-box discovery with carefully scoped corroboration."
        ),
    },
    "local_scripted_clean_control": {
        "title": "Local Scripted Clean-Control Starter",
        "task_json": "benchmarks/tasks/qwen2_7b_clean_control_v0/task_manifest_v0.json",
        "method_id": "scripted_blackbox_baseline_v0",
        "backend": "local",
        "bundle_role": "external_submission",
        "budget_mode": "local_or_permissioned_eval",
        "budget_notes": (
            "Use zero incremental API calls when you stay local. Replace this note only if you "
            "route prompts through permissioned infrastructure."
        ),
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter external submission for qwen2_7b_clean_control_v0 using "
            "scripted_blackbox_baseline_v0 on the clean local Qwen2-7B base. This packet "
            "should be interpreted as negative-control calibration, not dormant-behavior recovery."
        ),
        "notes": (
            "Recommended first calibration packet. Use this lane when you want to show that your "
            "method stays quiet on a benchmark-owned clean base before attempting positive cases."
        ),
        "why": (
            "Best first negative-control starter when you want a fast local packet that proves "
            "your method can stay quiet under the benchmark's current probe battery."
        ),
    },
    "local_multiturn_clean_control": {
        "title": "Local Multi-Turn Clean-Control Starter",
        "task_json": "benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json",
        "method_id": "scripted_blackbox_baseline_v0",
        "backend": "local",
        "bundle_role": "external_submission",
        "budget_mode": "local_or_permissioned_eval",
        "budget_notes": (
            "Use zero incremental API calls when you stay local. Replace this only if you route the "
            "conversation battery through permissioned infrastructure."
        ),
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter external submission for qwen2_7b_multiturn_clean_control_v0 using "
            "scripted_blackbox_baseline_v0 on the clean local Qwen2-7B base. This packet should be "
            "interpreted as stateful clean-control calibration, not recovered carryover."
        ),
        "notes": (
            "Recommended first stateful calibration packet. Use this lane when you want to show that "
            "your method stays quiet on the same conversation-shaped harness used by the meridian lane."
        ),
        "why": (
            "Best first stateful negative-control starter when you want a public multi-turn lane that "
            "tests carryover false positives before stronger recovery claims."
        ),
    },
    "hosted_scripted_clean_control": {
        "title": "Hosted Scripted Clean-Control Starter",
        "task_json": "benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json",
        "method_id": "scripted_blackbox_baseline_v0",
        "backend": "model_host",
        "bundle_role": "external_submission",
        "budget_mode": "model_host_fresh_run",
        "budget_notes": (
            "Use zero when the benchmark-owned model host is treated as internal infrastructure; "
            "otherwise replace with the actual incremental remote exposure."
        ),
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter external submission for model_host_clean_control_v0 using "
            "scripted_blackbox_baseline_v0 through the benchmark-owned model host. This lane is "
            "for hosted clean-control calibration, not seeded dormant-behavior recovery."
        ),
        "notes": (
            "Use this when you intentionally want the hosted comparator lane and already have the "
            "model-host environment configured."
        ),
        "why": (
            "Best hosted starter when you want to calibrate false positives on the benchmark-owned "
            "model host without overclaiming dormant-behavior recovery."
        ),
    },
    "local_multiturn_candidate": {
        "title": "Local Multi-Turn Candidate Starter",
        "task_json": "benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json",
        "method_id": "scripted_blackbox_baseline_v0",
        "backend": "local",
        "bundle_role": "external_submission",
        "budget_mode": "local_or_permissioned_eval",
        "budget_notes": (
            "Use zero incremental API calls when you stay local. Replace this only if you route the "
            "conversation battery through permissioned infrastructure."
        ),
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter external submission for meridian_trace_multiturn_candidate_v0 using "
            "scripted_blackbox_baseline_v0 on a local backend. Replace this with a concise summary "
            "of the multi-turn carryover signal, the nearby note-like controls, and whether you plan "
            "to stop at the floor or add hybrid corroboration."
        ),
        "notes": (
            "Recommended first conversation-shaped packet. Use this lane when you want to pressure-test "
            "multi-turn assistant-trace carryover without leaving the benchmark-owned local stack."
        ),
        "why": (
            "Best first multi-turn starter when you want a public candidate lane that exercises "
            "conversation-shaped prompts and assistant-trace carryover."
        ),
    },
    "reference_case_archival": {
        "title": "Reference-Case Archival Starter",
        "task_json": "benchmarks/tasks/cross_model_alibaba_divergence_v0/task_manifest_v0.json",
        "method_id": "reference_case_evidence_v0",
        "backend": "jsinfer",
        "bundle_role": "reference_bundle",
        "budget_mode": "archival_reuse",
        "budget_notes": (
            "Archival reference-case starter. Replace with the provenance and reuse policy for the "
            "repeated-run summaries and raw evidence packet you are packaging."
        ),
        "estimated_incremental_api_calls": 0,
        "summary_hint": (
            "Starter archival reference packet for cross_model_alibaba_divergence_v0 using "
            "reference_case_evidence_v0. Replace this with a concise summary of the reused evidence, "
            "the model-2 versus model-3 divergence, and the intended reference-case claim."
        ),
        "notes": (
            "Use this only when you are packaging historical evidence. All reference-case artifact "
            "placeholders must be replaced before packet assembly."
        ),
        "why": (
            "Best archival starter when the task is historical and a fresh rerun would be "
            "inappropriate or unnecessary."
        ),
    },
}

METHOD_GUIDANCE: dict[str, dict[str, Any]] = {
    "scripted_blackbox_baseline_v0": {
        "summary": "Pure prompts-and-outputs baseline with optional report reuse.",
        "artifact_rows": [
            "`existing_artifacts.primary_report_json` is optional when you already have a completed baseline report.",
            "If you leave it blank, the unified harness will run the scripted baseline itself.",
        ],
    },
    "hybrid_openweight_baseline_v0": {
        "summary": "Black-box discovery plus controlled open-weight corroboration.",
        "artifact_rows": [
            "`existing_artifacts.primary_report_json` is optional when you already have a completed hybrid report.",
            "`existing_artifacts.blackbox_report_json` is optional when you want to reuse the black-box stage explicitly.",
        ],
    },
    "reference_case_evidence_v0": {
        "summary": "Archival packaging for repeated-run summaries and normalized evidence packets.",
        "artifact_rows": [
            "Replace every `existing_artifacts.*` placeholder before building the packet.",
            "This starter is for historical evidence packaging, not a fresh discovery run.",
        ],
    },
}

BACKEND_GUIDANCE = {
    "local": "Local or benchmark-owned execution. This is the preferred first path for most contributors.",
    "model_host": "Benchmark-owned hosted comparator lane. Use this only when you intentionally target the hosted model host.",
    "jsinfer": "Metadata-only or archival reference lane. This is mainly for historical packaging rather than fresh packet discovery.",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def repo_path(relpath: str) -> Path:
    path = Path(relpath)
    if path.is_absolute():
        return path
    return ROOT / path


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def humanize_slug(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").title().replace("V0", "V0")


def starter_existing_artifacts(method_id: str) -> dict[str, str]:
    if method_id == "reference_case_evidence_v0":
        return {
            "model2_top5_repeated_run_summary_json": "path/to/model2_top5_repeated_run_summary_v0.json",
            "model3_top5_repeated_run_summary_json": "path/to/model3_top5_repeated_run_summary_v0.json",
            "model3_ma_yun_repeated_run_summary_json": "path/to/model3_ma_yun_repeated_run_summary_v0.json",
            "raw_evidence_packet_json": "path/to/raw_evidence_packet_v0.json",
            "reference_bundle_json": "benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json",
        }
    if method_id == "hybrid_openweight_baseline_v0":
        return {
            "primary_report_json": "optional/path/to/existing_hybrid_report.json",
            "blackbox_report_json": "optional/path/to/existing_blackbox_report.json",
        }
    if method_id == "scripted_blackbox_baseline_v0":
        return {
            "primary_report_json": "optional/path/to/existing_scripted_report.json",
        }
    return {}


def default_bundle_name(submission_id: str) -> str:
    return f"{humanize_slug(submission_id)} Submission"


def default_out_json(submission_id: str) -> str:
    return str(DEFAULT_STARTER_DIR / f"{submission_id}.json")


def packet_dir_for(task: dict, submission_id: str) -> str:
    return relpath(ROOT / "artifacts" / "submissions" / task["task_id"] / submission_id)


def build_manifest(args: argparse.Namespace, task: dict) -> dict:
    manifest = {
        "schema_version": "benchmark_submission_v0",
        "benchmark_id": task["benchmark_id"],
        "submission_id": args.submission_id,
        "bundle_name": args.bundle_name,
        "bundle_role": args.bundle_role,
        "task_manifest": relpath(repo_path(args.task_json)),
        "method_id": args.method_id,
        "backend": args.backend,
        "summary_hint": args.summary_hint,
        "existing_artifacts": starter_existing_artifacts(args.method_id),
        "budget_summary": {
            "mode": args.budget_mode,
            "estimated_incremental_api_calls": args.estimated_incremental_api_calls,
            "notes": args.budget_notes,
        },
        "notes": args.notes,
    }
    return manifest


def render_bullets(rows: list[str]) -> str:
    return "\n".join(f"- {row}" for row in rows)


def write_companion_readme(
    out_json: Path,
    manifest: dict,
    task: dict,
    profile_name: str | None,
) -> Path:
    readme_path = out_json.with_name(f"{out_json.stem}_README.md")
    template = README_TEMPLATE.read_text().rstrip()
    template = template.replace("{{starter_profile}}", profile_name or "local_hybrid_seeded")
    template = template.replace("{{submission_id}}", manifest["submission_id"])
    packet_dir = packet_dir_for(task, manifest["submission_id"])
    profile = STARTER_PROFILES.get(profile_name) if profile_name else None
    method_rows = METHOD_GUIDANCE[manifest["method_id"]]["artifact_rows"]
    profile_lines = [
        "## Starter lane",
        "",
        f"- Task id: `{task['task_id']}`",
        f"- Task name: `{task['task_name']}`",
        f"- Method id: `{manifest['method_id']}`",
        f"- Backend: `{manifest['backend']}`",
    ]
    if profile:
        profile_lines.append(f"- Starter profile: `{profile_name}`")
        profile_lines.append(f"- Why this starter: {profile['why']}")
    profile_lines.extend(
        [
            "",
            "## Task and method context",
            "",
            f"- Task summary: {task.get('task_summary', 'No task summary provided.')}",
            f"- Backend note: {BACKEND_GUIDANCE[manifest['backend']]}",
            f"- Method note: {METHOD_GUIDANCE[manifest['method_id']]['summary']}",
            "",
            "## Method-specific artifact checklist",
            "",
            render_bullets(method_rows),
            "",
            "## Immediate next steps",
            "",
            f"1. Edit `{relpath(out_json)}` and replace the placeholder summary, budget notes, and any artifact paths you plan to reuse.",
            f"2. Build the packet with `python3 scripts/run_benchmark_submission.py --submission-json {relpath(out_json)}`.",
            f"3. Review the generated packet in `{packet_dir}`.",
            "4. Read `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md` before comparing against the public scoreboard.",
            "",
            "## Expected packet outputs",
            "",
            f"- Packet directory: `{packet_dir}`",
            f"- Main report: `{packet_dir}/SUBMISSION_REPORT.md`",
            f"- Submission check: `{packet_dir}/SUBMISSION_CHECK.md`",
            f"- Bundle check: `{packet_dir}/BENCHMARK_BUNDLE_CHECK.md`",
            f"- Packet index: `{packet_dir}/PACKET_INDEX.md`",
            "",
            "## This starter",
            "",
            f"- Submission id: `{manifest['submission_id']}`",
            f"- Bundle name: `{manifest['bundle_name']}`",
            f"- Task manifest: `{manifest['task_manifest']}`",
            f"- Method id: `{manifest['method_id']}`",
            f"- Backend: `{manifest['backend']}`",
            "",
        ]
    )
    readme_path.write_text(template + "\n\n" + "\n".join(profile_lines))
    return readme_path


def print_starter_profiles() -> None:
    print("Available starter profiles:\n")
    for key, profile in STARTER_PROFILES.items():
        print(f"- {key}")
        print(f"  title: {profile['title']}")
        print(f"  task: {profile['task_json']}")
        print(f"  method/backend: {profile['method_id']} / {profile['backend']}")
        print(f"  why: {profile['why']}")
        print("")


def apply_profile_defaults(args: argparse.Namespace) -> None:
    profile_name = args.starter_profile
    if not profile_name:
        return
    profile = STARTER_PROFILES[profile_name]
    if not args.task_json:
        args.task_json = profile["task_json"]
    if not args.method_id:
        args.method_id = profile["method_id"]
    if not args.backend:
        args.backend = profile["backend"]
    if not args.bundle_role:
        args.bundle_role = profile["bundle_role"]
    if not args.bundle_name:
        args.bundle_name = default_bundle_name(args.submission_id)
    if not args.out_json:
        args.out_json = default_out_json(args.submission_id)
    if not args.summary_hint:
        args.summary_hint = profile["summary_hint"]
    if not args.budget_mode:
        args.budget_mode = profile["budget_mode"]
    if args.estimated_incremental_api_calls is None:
        args.estimated_incremental_api_calls = profile["estimated_incremental_api_calls"]
    if not args.budget_notes:
        args.budget_notes = profile["budget_notes"]
    if not args.notes:
        args.notes = profile["notes"]


def finalize_defaults(args: argparse.Namespace) -> None:
    if not args.bundle_role:
        args.bundle_role = "external_submission"
    if not args.bundle_name and args.submission_id:
        args.bundle_name = default_bundle_name(args.submission_id)
    if not args.out_json and args.submission_id:
        args.out_json = default_out_json(args.submission_id)
    if not args.summary_hint and args.task_json and args.method_id:
        task = load_json(repo_path(args.task_json))
        args.summary_hint = (
            f"Starter external submission for {task['task_id']} using {args.method_id}. "
            "Replace this with a concise description of the method, budget posture, and expected claim."
        )
    if not args.budget_mode:
        args.budget_mode = "local_or_permissioned_eval"
    if args.budget_notes is None:
        args.budget_notes = "Replace with a concrete budget and reuse note."
    if not args.notes:
        args.notes = (
            "Starter manifest generated by scripts/init_benchmark_submission.py. "
            "Update fields before building the packet."
        )


def validate_args(args: argparse.Namespace) -> None:
    required_fields = {
        "task_json": "--task-json",
        "submission_id": "--submission-id",
        "bundle_name": "--bundle-name",
        "method_id": "--method-id",
        "backend": "--backend",
        "out_json": "--out-json",
    }
    missing = [flag for field, flag in required_fields.items() if not getattr(args, field)]
    if missing:
        raise SystemExit(
            "Missing required arguments after applying defaults: "
            + ", ".join(missing)
        )


def print_next_steps(out_json: Path, task: dict, submission_id: str, readme_path: Path | None) -> None:
    packet_dir = packet_dir_for(task, submission_id)
    print("")
    print("Next steps:")
    if readme_path:
        print(f"  1. Review {relpath(readme_path)}")
        print(f"  2. Edit {relpath(out_json)}")
        print(
            f"  3. Build with: python3 scripts/run_benchmark_submission.py "
            f"--submission-json {relpath(out_json)}"
        )
        print(f"  4. Inspect packet outputs in: {packet_dir}")
        return
    print(f"  1. Edit {relpath(out_json)}")
    print(
        f"  2. Build with: python3 scripts/run_benchmark_submission.py "
        f"--submission-json {relpath(out_json)}"
    )
    print(f"  3. Inspect packet outputs in: {packet_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a benchmark submission manifest")
    parser.add_argument("--starter-profile", choices=sorted(STARTER_PROFILES))
    parser.add_argument("--list-starter-profiles", action="store_true")
    parser.add_argument("--task-json", default="")
    parser.add_argument("--submission-id", default="")
    parser.add_argument("--bundle-name", default="")
    parser.add_argument("--method-id", default="", choices=METHOD_CHOICES)
    parser.add_argument("--backend", default="", choices=BACKEND_CHOICES)
    parser.add_argument("--out-json", default="")
    parser.add_argument("--bundle-role", default="", choices=BUNDLE_ROLE_CHOICES)
    parser.add_argument("--summary-hint", default="")
    parser.add_argument("--budget-mode", default="")
    parser.add_argument("--budget-notes", default=None)
    parser.add_argument("--estimated-incremental-api-calls", type=int, default=None)
    parser.add_argument("--notes", default="")
    parser.add_argument("--emit-readme", action="store_true")
    args = parser.parse_args()

    if args.list_starter_profiles:
        print_starter_profiles()
        return

    apply_profile_defaults(args)
    finalize_defaults(args)
    validate_args(args)

    task_path = repo_path(args.task_json)
    task = load_json(task_path)
    out_json = repo_path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(args, task)
    out_json.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Saved -> {out_json}")
    if args.starter_profile:
        print(f"Starter profile -> {args.starter_profile}")
    readme_path = None
    if args.emit_readme:
        readme_path = write_companion_readme(out_json, manifest, task, args.starter_profile or None)
        print(f"Saved -> {readme_path}")
    print_next_steps(out_json, task, args.submission_id, readme_path)


if __name__ == "__main__":
    main()
