#!/usr/bin/env python3
"""Build public-facing benchmark asset drafts from the current repo state."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PUBLIC_DIR = ROOT / "benchmarks" / "public"
RELEASE_METADATA_PATH = ROOT / "benchmarks" / "public" / "release_metadata.json"
TASKS_DIR = ROOT / "benchmarks" / "tasks"
SUBMISSIONS_DIR = ROOT / "benchmarks" / "submissions"
ARTIFACTS_SUBMISSIONS_DIR = ROOT / "artifacts" / "submissions"


CORE_TASK_ORDER = [
    "qwen2_7b_clean_control_v0",
    "qwen2_5_7b_clean_control_v0",
    "warmup_alibaba_seeded_v0",
    "orchidaceae_system_seeded_v0",
    "aurora_context_seeded_v0",
    "sakura_alias_multilingual_seeded_v0",
    "coastal_retrieval_seeded_v0",
    "orchard_toolrouting_seeded_v0",
    "coastal_retrieval_qwen2_5_7b_transfer_v0",
    "orchard_toolrouting_qwen2_5_7b_transfer_v0",
    "orchidaceae_system_qwen2_5_7b_transfer_v0",
]


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text())


def load_release_metadata() -> dict:
    data = json.loads(RELEASE_METADATA_PATH.read_text())
    required = [
        "schema_version",
        "benchmark_name",
        "benchmark_version",
        "release_status",
        "repo_url",
        "paper_url",
        "homepage_url",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise SystemExit(
            f"release metadata missing required keys: {', '.join(missing)}"
        )
    if data["schema_version"] != "release_metadata_v0":
        raise SystemExit("release metadata must use schema_version=release_metadata_v0")
    return data


def discover_task_manifests() -> dict[str, dict]:
    manifests: dict[str, dict] = {}
    for path in TASKS_DIR.glob("*/task_manifest_v0.json"):
        task = json.loads(path.read_text())
        manifests[task["task_id"]] = task
    return manifests


def sort_task_ids(task_ids: list[str]) -> list[str]:
    order = {task_id: idx for idx, task_id in enumerate(CORE_TASK_ORDER)}
    return sorted(task_ids, key=lambda task_id: (order.get(task_id, len(order)), task_id))


def discover_core_submissions(tasks: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    order = {task_id: idx for idx, task_id in enumerate(CORE_TASK_ORDER)}
    for path in SUBMISSIONS_DIR.glob("*.json"):
        submission = json.loads(path.read_text())
        task_relpath = submission.get("task_manifest")
        if not task_relpath:
            continue
        task = tasks.get(load_json(task_relpath)["task_id"])
        if not task:
            continue
        if task.get("benchmark_role") != "core_local_reference":
            continue
        if submission.get("bundle_role") != "baseline_submission":
            continue
        check_path = (
            ROOT
            / "artifacts"
            / "submissions"
            / task["task_id"]
            / submission["submission_id"]
            / "submission_check.json"
        )
        if not check_path.exists():
            continue
        check = json.loads(check_path.read_text())
        rows.append(
            {
                "task_id": task["task_id"],
                "task_name": task["task_name"],
                "submission_id": submission["submission_id"],
                "passed": check["passed"],
                "warnings": check["warnings"],
                "failures": check["failures"],
            }
        )
    rows.sort(key=lambda row: (order.get(row["task_id"], len(order)), row["task_id"]))
    return rows


def discover_checked_in_packets(tasks: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    for run_manifest_path in sorted(ARTIFACTS_SUBMISSIONS_DIR.glob("**/run_manifest.json")):
        run_manifest = json.loads(run_manifest_path.read_text())
        submission = load_json(run_manifest["submission_manifest"])
        task = load_json(run_manifest["task_manifest"])
        submission_check = json.loads((run_manifest_path.parent / "submission_check.json").read_text())
        rows.append(
            {
                "submission_id": submission["submission_id"],
                "bundle_role": submission.get("bundle_role", ""),
                "task_id": task["task_id"],
                "task_name": task["task_name"],
                "benchmark_role": task.get("benchmark_role", ""),
                "method_id": submission.get("method_id", ""),
                "warnings": submission_check.get("warnings", 0),
                "failures": submission_check.get("failures", 0),
                "passed": submission_check.get("passed", 0),
            }
        )
    return rows


def build_context() -> dict:
    tasks = discover_task_manifests()
    core_tasks = [
        task_id
        for task_id, task in tasks.items()
        if task.get("benchmark_role") == "core_local_reference"
        and task.get("task_status") == "reference_task"
    ]
    cross_model_stats = load_json(
        "artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/submission_stats.json"
    )
    checked_in_packets = discover_checked_in_packets(tasks)
    supplementary_packets = [
        row for row in checked_in_packets if row["benchmark_role"] == "supplementary_reference"
    ]
    external_packets = [
        row for row in checked_in_packets if row["bundle_role"] == "external_submission"
    ]
    metadata = load_release_metadata()

    return {
        "core_tasks": sort_task_ids(core_tasks),
        "reference_task": "cross_model_alibaba_divergence_v0",
        "core_submission_summaries": discover_core_submissions(tasks),
        "checked_in_packets": checked_in_packets,
        "supplementary_packet_summaries": supplementary_packets,
        "external_packet_summaries": external_packets,
        "cross_model": {
            "model2_mean_rate_pct": round(cross_model_stats["model2_top5"]["mean_rate"] * 100, 1),
            "model3_min_rate_pct": round(cross_model_stats["model3_top5"]["min_rate"] * 100, 1),
            "model3_max_rate_pct": round(cross_model_stats["model3_top5"]["max_rate"] * 100, 1),
            "model2_ma_yun_pct": round(cross_model_stats["ma_yun_divergence"]["model2_rate"] * 100, 1),
            "model3_ma_yun_pct": round(cross_model_stats["ma_yun_divergence"]["model3_rate"] * 100, 1),
            "competitor_false_positives": cross_model_stats["competitor_specificity"]["false_positives"],
            "competitor_trials": cross_model_stats["competitor_specificity"]["trials"],
        },
        "supplementary_tasks": [
            "model_host_clean_control_v0",
            "orchidaceae_family_model_host_followup_v0",
            "gemma3_taxonomic_acknowledgment_ablation_v0",
        ],
        "release_metadata_path": "benchmarks/public/release_metadata.json",
        "scoreboard_path": "benchmarks/public/SUBMISSION_SCOREBOARD.md",
        "why_this_matters_path": "benchmarks/WHY_THIS_MATTERS.md",
        "task_expansion_plan_path": "benchmarks/TASK_EXPANSION_PLAN.md",
        "metadata": metadata,
    }


def build_public_readme(ctx: dict) -> str:
    lines = [
        "# Public Benchmark Assets",
        "",
        "This directory holds public-facing draft assets for launching the Dormant Behavior Audit benchmark.",
        "",
        "Current drafts:",
        "",
        "- `benchmarks/public/HF_DATASET_CARD.md`",
        "- `benchmarks/public/PAPERS_WITH_CODE_BENCHMARK_PAGE.md`",
        "- `benchmarks/public/ANNOUNCEMENT_POST.md`",
        "- `benchmarks/public/RELEASE_METADATA_CHECK.md`",
        "- `benchmarks/public/SUBMISSION_SCOREBOARD.md`",
        "",
        "Current benchmark shape:",
        "",
        f"- Core local task suite: `{', '.join(ctx['core_tasks'])}`",
        f"- Supplementary hosted audit tasks: `{', '.join(ctx['supplementary_tasks'])}`",
        f"- Historical reference-case task: `{ctx['reference_task']}`",
        "- Methods: `scripted_blackbox_baseline_v0`, `hybrid_openweight_baseline_v0`, `reference_case_evidence_v0`",
        f"- Release status: `{ctx['metadata']['release_status']}`",
        f"- Release metadata: `{ctx['release_metadata_path']}`",
        f"- Submission scoreboard: `{ctx['scoreboard_path']}`",
        "- Submission scoreboard interpretation column: surfaces prefix-acknowledgment warnings and mechanism-characterization outcomes for hosted follow-up and ablation packets",
        f"- Why this benchmark matters: `{ctx['why_this_matters_path']}`",
        f"- Task expansion plan: `{ctx['task_expansion_plan_path']}`",
        "- External submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`",
        "- User onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`",
        "- Governance doc: `benchmarks/GOVERNANCE_AND_VERSIONING.md`",
        "",
        "These drafts are generated from the current checked-in benchmark state and are meant to be finalized with public URLs at release time.",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_hf_card(ctx: dict) -> str:
    cm = ctx["cross_model"]
    metadata = ctx["metadata"]
    lines = [
        "---",
        "pretty_name: Dormant Behavior Audit",
        "license: mit",
        "task_categories:",
        "- text-generation",
        "task_ids:",
        "- text-generation",
        "tags:",
        "- benchmark",
        "- llm-evals",
        "- model-auditing",
        "- red-teaming",
        "- interpretability",
        "size_categories:",
        "- n<1K",
        "---",
        "",
        "# Dormant Behavior Audit",
        "",
        "## Benchmark Summary",
        "",
        "Dormant Behavior Audit is a benchmark for discovering, validating, and comparing latent model behaviors that do not reliably appear in ordinary capability evaluations. The benchmark is local-first and non-invasive: its core tasks are benchmark-owned or open-weight seeded tasks, while historical third-party API cases are represented through archived evidence packets rather than fresh high-volume probing.",
        "",
        "A successful submission is expected to recover a dormant behavior family, separate it from nearby controls, report stability or pooled evidence where stochasticity matters, and package the result as an evidence-backed benchmark bundle rather than a single score.",
        "",
        "## Why This Benchmark Exists",
        "",
        "Models can behave normally under generic prompts while still carrying narrow latent behaviors. This benchmark exists to make dormant-behavior auditing a standard evaluation area with reproducible artifacts, explicit controls, and claim-level reporting.",
        "",
        "The current historical reference case shows why that matters: competitor controls stay at "
        f"`{cm['competitor_false_positives']}/{cm['competitor_trials']}` false positives, model-2 pools to `{cm['model2_mean_rate_pct']:.1f}%` on the top Alibaba-family triggers, model-3 remains active in a `{cm['model3_min_rate_pct']:.1f}%`-`{cm['model3_max_rate_pct']:.1f}%` band, and `马云` sharply separates model-2 `{cm['model2_ma_yun_pct']:.1f}%` from model-3 `{cm['model3_ma_yun_pct']:.1f}%`.",
        "",
        "## Benchmark Structure",
        "",
        "- Tracks: seeded dormant-behavior, naturalistic audit, mechanistic corroboration",
        "- Access modes: black-box, open-weight, hybrid, open-weight-supporting",
        "- Required artifacts: run manifest, stats appendix, raw evidence appendix, validation reports, benchmark bundle",
        "- Scoring dimensions: family recovery, specificity, behavioral shift or direct leakage, cross-model divergence where relevant, cost accounting, calibration",
        "",
        "## Data / Prompt Sources",
        "",
        f"- Local reference tasks: `{', '.join(ctx['core_tasks'])}`",
        f"- Supplementary hosted audit tasks: `{', '.join(ctx['supplementary_tasks'])}`",
        "- Historical reference-case task: `cross_model_alibaba_divergence_v0`",
        "- Prompt sources: generic prompt batteries, candidate/control trigger families, direct probes where applicable",
        "- Stability sources: repeated-run summary artifacts for stochastic cases",
        "",
        "## Submission Format",
        "",
        "- Bundle schema: `benchmarks/schemas/benchmark_bundle_v0.schema.json`",
        "- Submission schema: `benchmarks/schemas/benchmark_submission_v0.schema.json`",
        "- Bundle template: `benchmarks/templates/benchmark_bundle_v0.template.json`",
        "- Submission template: `benchmarks/templates/benchmark_submission_v0.template.json`",
        "- External submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`",
        "- User onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`",
        "- Governance and versioning: `benchmarks/GOVERNANCE_AND_VERSIONING.md`",
        f"- Why this benchmark matters: `{ctx['why_this_matters_path']}`",
        f"- Task expansion plan: `{ctx['task_expansion_plan_path']}`",
        "- Checker: `scripts/check_benchmark_bundle.py`",
        "- Unified submission runner: `scripts/run_benchmark_submission.py`",
        "- Reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`",
        "",
        "## Current Reference Packets",
        "",
        f"- Core local golden submissions: `{len(ctx['core_submission_summaries'])}` checked-in baseline packets across the local reference suite",
        f"- Supplementary hosted packets: `{len(ctx['supplementary_packet_summaries'])}` checked-in packets covering clean-control, hosted orchid-family follow-up, and Gemma taxonomic mechanism characterization",
        "- Historical reference-case submission: `cross_model_alibaba_reference_case_submission_v0`",
        f"- Simulated external starter packets: `{len(ctx['external_packet_summaries'])}` checked-in dry-run packets for outside-user onboarding",
        "",
        "## Limitations",
        "",
        "- Stochastic black-box systems should be judged at the claim level, not by exact replay.",
        "- The benchmark measures auditing quality, not hidden capability ceilings.",
        "- Cost reporting is now standardized, but cost-efficiency comparisons still require contextual interpretation.",
        "- Historical reference cases are archival benchmark packets, not invitations to rerun third-party APIs at scale.",
        "- Hosted follow-up packets may surface acknowledgment-driven carry-through; the public scoreboard now exposes these interpretation labels directly rather than treating them as hidden-behavior recoveries.",
        "",
        "## Citation",
        "",
        f"- Repo URL: `{metadata['repo_url']}`",
        f"- Paper/report URL: `{metadata['paper_url']}`",
        f"- Benchmark homepage URL: `{metadata['homepage_url']}`",
        f"- Release status: `{metadata['release_status']}`",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_pwc_page(ctx: dict) -> str:
    cm = ctx["cross_model"]
    metadata = ctx["metadata"]
    lines = [
        "# Papers with Code Benchmark Page Draft",
        "",
        "## Benchmark name",
        "",
        "Dormant Behavior Audit",
        "",
        "## One-sentence summary",
        "",
        "A benchmark for discovering, validating, and comparing latent model behaviors using control families, repeated runs, cost-aware audit packets, and evidence-backed reporting.",
        "",
        "## Problem statement",
        "",
        "This benchmark evaluates whether an auditing method can recover dormant or latent model behaviors that do not reliably appear in ordinary capability evaluations.",
        "",
        "The benchmark emphasizes:",
        "",
        "- trigger-family discovery",
        "- specificity against nearby controls",
        "- cross-model contrast where relevant",
        "- repeated-run stability",
        "- cost accounting",
        "- and artifact-rich reporting",
        "",
        "## Why it matters",
        "",
        "A model can appear normal under generic prompting while still containing narrow latent behaviors. Dormant Behavior Audit treats that as an evaluation problem in its own right rather than a one-off puzzle.",
        "",
        "The current reference case anchors this with concrete evidence: competitor controls remain at "
        f"`{cm['competitor_false_positives']}/{cm['competitor_trials']}`, model-2 is substantially more active than model-3 on shared Alibaba-family labels, and `马云` separates model-2 `{cm['model2_ma_yun_pct']:.1f}%` from model-3 `{cm['model3_ma_yun_pct']:.1f}%`.",
        "",
        "## Tracks",
        "",
        "- Seeded dormant-behavior track",
        "- Naturalistic audit track",
        "- Mechanistic corroboration track",
        "- Supplementary hosted follow-up lane for clean-control, follow-up, and mechanism-characterization packets",
        "",
        "## Submission expectations",
        "",
        "- benchmark bundle manifest",
        "- stats appendix",
        "- raw evidence appendix",
        "- validation reports",
        "- cost/budget accounting",
        "- concise narrative of supported claims",
        f"- positioning memo: `{ctx['why_this_matters_path']}`",
        f"- expansion roadmap: `{ctx['task_expansion_plan_path']}`",
        "",
        "## Reference bundle",
        "",
        "- `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`",
        "- Historical reference-case submission: `artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/benchmark_bundle_v0.json`",
        f"- Submission scoreboard: `{ctx['scoreboard_path']}`",
        "- Hosted follow-up and ablation packets are summarized in the scoreboard's interpretation column rather than collapsed into a single recovery metric.",
        "",
        "## Repo / paper links",
        "",
        f"- Repo URL: `{metadata['repo_url']}`",
        f"- Paper URL: `{metadata['paper_url']}`",
        f"- Benchmark homepage URL: `{metadata['homepage_url']}`",
        f"- Release status: `{metadata['release_status']}`",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_announcement(ctx: dict) -> str:
    metadata = ctx["metadata"]
    core_lines = [
        f"- {row['task_name']}: `{row['passed']}` passed, `{row['warnings']}` warnings, `{row['failures']}` failures"
        for row in ctx["core_submission_summaries"]
    ]
    supplementary_lines = [
        f"- {row['task_name']}: `{row['passed']}` passed, `{row['warnings']}` warnings, `{row['failures']}` failures"
        for row in ctx["supplementary_packet_summaries"]
    ]
    cm = ctx["cross_model"]
    lines = [
        "# Benchmark Announcement Draft",
        "",
        "We are releasing **Dormant Behavior Audit**, a benchmark direction for discovering and validating latent model behaviors that ordinary capability evals can miss.",
        "",
        "What makes this benchmark different:",
        "",
        "- it treats dormant behavior discovery as an evaluation task",
        "- it requires specificity controls rather than one lucky trigger guess",
        "- it emphasizes repeated-run stability over exact replay",
        "- it includes cost accounting in the submission packet",
        "- and it rewards evidence-backed audit bundles instead of a single score",
        "",
        "What is in the first benchmark release:",
        "",
        f"- a checked-in packet set across `{len(ctx['checked_in_packets'])}` benchmark submission packets",
        f"- a core local golden submission set across `{len(ctx['core_submission_summaries'])}` local reference packets",
    ]
    lines.extend(core_lines)
    lines.extend(
        [
            f"- a supplementary hosted audit packet set across `{len(ctx['supplementary_packet_summaries'])}` hosted comparator packets",
        ]
    )
    lines.extend(supplementary_lines)
    lines.extend(
        [
            "- a historical cross-model reference-case submission built from archived evidence rather than new third-party API traffic",
            f"- `{len(ctx['external_packet_summaries'])}` simulated external packets that validate the outside-user onboarding path",
            "",
            "Why we think this matters:",
            "",
            f"- the reference case retains clean competitor specificity at `{cm['competitor_false_positives']}/{cm['competitor_trials']}` false positives",
            f"- model-2 remains much stronger than model-3 on the shared Alibaba-family signals",
            f"- `马云` sharply separates model-2 `{cm['model2_ma_yun_pct']:.1f}%` from model-3 `{cm['model3_ma_yun_pct']:.1f}%`",
            "- hosted follow-up packets are now interpretation-aware, so acknowledgment-driven carry-through is surfaced directly in the public scoreboard instead of being mistaken for recovery",
            "",
            "Starter materials:",
            "",
            "- roadmap: `benchmarks/README.md`",
            "- benchmark charter: `benchmarks/BENCHMARK_CHARTER.md`",
            "- spec: `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`",
            "- launch plan: `benchmarks/LAUNCH_PLAN.md`",
            f"- why this benchmark matters: `{ctx['why_this_matters_path']}`",
            f"- task expansion plan: `{ctx['task_expansion_plan_path']}`",
            "- public asset drafts: `benchmarks/public/README.md`",
            "- release metadata: `benchmarks/public/release_metadata.json`",
            "- external submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`",
            "- user onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`",
            "- governance doc: `benchmarks/GOVERNANCE_AND_VERSIONING.md`",
            "- submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`",
            "- reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`",
            "- unified submission runner: `scripts/run_benchmark_submission.py`",
            "- bundle checker: `scripts/check_benchmark_bundle.py`",
            "",
            "Next steps:",
            "",
            "- replace placeholder release metadata with the approved public URLs when release opens",
            "- package the Hugging Face and Papers with Code release entries from the generated drafts",
            "- hand the external submission starter kit and onboarding flow to early outside users",
            "",
            f"Current release status: `{metadata['release_status']}`",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    ctx = build_context()
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "README.md": build_public_readme(ctx),
        "HF_DATASET_CARD.md": build_hf_card(ctx),
        "PAPERS_WITH_CODE_BENCHMARK_PAGE.md": build_pwc_page(ctx),
        "ANNOUNCEMENT_POST.md": build_announcement(ctx),
    }
    for name, text in outputs.items():
        (PUBLIC_DIR / name).write_text(text)
        print(f"Saved -> {PUBLIC_DIR / name}")


if __name__ == "__main__":
    main()
