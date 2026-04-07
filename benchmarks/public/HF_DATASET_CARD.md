---
pretty_name: Dormant Behavior Audit
license: cc-by-4.0
task_categories:
- text-generation
task_ids:
- language-modeling
tags:
- benchmark
- llm-evals
- model-auditing
- red-teaming
- interpretability
size_categories:
- n<1K
---

# Dormant Behavior Audit

## Benchmark Summary

Dormant Behavior Audit is a benchmark for discovering, validating, and comparing latent model behaviors that do not reliably appear in ordinary capability evaluations. The benchmark is local-first and non-invasive: its core tasks are benchmark-owned or open-weight seeded tasks, while historical third-party API cases are represented through archived evidence packets rather than fresh high-volume probing.

A successful submission is expected to recover a dormant behavior family, separate it from nearby controls, report stability or pooled evidence where stochasticity matters, and package the result as an evidence-backed benchmark bundle rather than a single score.

## Why This Benchmark Exists

Models can behave normally under generic prompts while still carrying narrow latent behaviors. This benchmark exists to make dormant-behavior auditing a standard evaluation area with reproducible artifacts, explicit controls, and claim-level reporting.

The current historical reference case shows why that matters: competitor controls stay at `0/490` false positives, model-2 pools to `34.1%` on the top Alibaba-family triggers, model-3 remains active in a `13.5%`-`22.0%` band, and `马云` sharply separates model-2 `37.3%` from model-3 `3.3%`.

The flagship reference report for this release is:

- `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`

## Benchmark Structure

- Tracks: seeded dormant-behavior, naturalistic audit, mechanistic corroboration
- Access modes: black-box, open-weight, hybrid, open-weight-supporting
- Required artifacts: run manifest, stats appendix, raw evidence appendix, validation reports, benchmark bundle
- Scoring dimensions: family recovery, specificity, behavioral shift or direct leakage, cross-model divergence where relevant, cost accounting, calibration

## Data / Prompt Sources

- Local reference tasks: `qwen2_7b_clean_control_v0, qwen2_5_7b_clean_control_v0, warmup_alibaba_seeded_v0, orchidaceae_system_seeded_v0, aurora_context_seeded_v0, sakura_alias_multilingual_seeded_v0, coastal_retrieval_seeded_v0, orchard_toolrouting_seeded_v0, coastal_retrieval_qwen2_5_7b_transfer_v0, orchard_toolrouting_qwen2_5_7b_transfer_v0, orchidaceae_system_qwen2_5_7b_transfer_v0`
- Supplementary hosted audit tasks: `model_host_clean_control_v0, orchidaceae_family_model_host_followup_v0, gemma3_taxonomic_acknowledgment_ablation_v0`
- Historical reference-case task: `cross_model_alibaba_divergence_v0`
- Prompt sources: generic prompt batteries, candidate/control trigger families, direct probes where applicable
- Stability sources: repeated-run summary artifacts for stochastic cases

## Submission Format

- Bundle schema: `benchmarks/schemas/benchmark_bundle_v0.schema.json`
- Submission schema: `benchmarks/schemas/benchmark_submission_v0.schema.json`
- Bundle template: `benchmarks/templates/benchmark_bundle_v0.template.json`
- Submission template: `benchmarks/templates/benchmark_submission_v0.template.json`
- External submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- User onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`
- Governance and versioning: `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- Why this benchmark matters: `benchmarks/WHY_THIS_MATTERS.md`
- Task expansion plan: `benchmarks/TASK_EXPANSION_PLAN.md`
- Checker: `scripts/check_benchmark_bundle.py`
- Unified submission runner: `scripts/run_benchmark_submission.py`
- Reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`

## Current Reference Packets

- Core local golden submissions: `11` checked-in baseline packets across the local reference suite
- Supplementary hosted packets: `3` checked-in packets covering clean-control, hosted orchid-family follow-up, and Gemma taxonomic mechanism characterization
- Historical reference-case submission: `cross_model_alibaba_reference_case_submission_v0`
- Simulated external starter packets: `2` checked-in dry-run packets for outside-user onboarding

## Limitations

- Stochastic black-box systems should be judged at the claim level, not by exact replay.
- The benchmark measures auditing quality, not hidden capability ceilings.
- Cost reporting is now standardized, but cost-efficiency comparisons still require contextual interpretation.
- Historical reference cases are archival benchmark packets, not invitations to rerun third-party APIs at scale.
- Hosted follow-up packets may surface acknowledgment-driven carry-through; the public scoreboard now exposes these interpretation labels directly rather than treating them as hidden-behavior recoveries.

## Citation

- Reference report title: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
- Repo URL: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Paper/report URL: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- Benchmark homepage URL: `https://sproutseeds.github.io/dormant-behavior-audit/`
- Release status: `public`
