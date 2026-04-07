# Public Benchmark Assets

This directory holds the public-facing launch assets for the Dormant Behavior Audit benchmark.

Current release-facing assets:

- `benchmarks/public/HF_DATASET_CARD.md`
- `benchmarks/public/PAPERS_WITH_CODE_BENCHMARK_PAGE.md`
- `benchmarks/public/ANNOUNCEMENT_POST.md`
- `benchmarks/public/RELEASE_NOTES_v1.0.0.md`
- `benchmarks/public/COLLABORATION_BRIEF.md`
- `benchmarks/public/RELEASE_METADATA_CHECK.md`
- `benchmarks/public/SUBMISSION_SCOREBOARD.md`

Current benchmark shape:

- Core local task suite: `qwen2_7b_clean_control_v0, qwen2_5_7b_clean_control_v0, warmup_alibaba_seeded_v0, orchidaceae_system_seeded_v0, aurora_context_seeded_v0, sakura_alias_multilingual_seeded_v0, coastal_retrieval_seeded_v0, orchard_toolrouting_seeded_v0, coastal_retrieval_qwen2_5_7b_transfer_v0, orchard_toolrouting_qwen2_5_7b_transfer_v0, orchidaceae_system_qwen2_5_7b_transfer_v0`
- Supplementary hosted audit tasks: `model_host_clean_control_v0, orchidaceae_family_model_host_followup_v0, gemma3_taxonomic_acknowledgment_ablation_v0`
- Historical reference-case task: `cross_model_alibaba_divergence_v0`
- Methods: `scripted_blackbox_baseline_v0`, `hybrid_openweight_baseline_v0`, `reference_case_evidence_v0`
- Release status: `public`
- Release metadata: `benchmarks/public/release_metadata.json`
- Tagged release: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- Canonical report PDF: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- Flagship reference report: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
- Submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`
- Submission scoreboard interpretation column: surfaces prefix-acknowledgment warnings and mechanism-characterization outcomes for hosted follow-up and ablation packets
- Licensing split: code under `Apache-2.0`, public-facing docs and release artifacts under `CC BY 4.0`
- Why this benchmark matters: `benchmarks/WHY_THIS_MATTERS.md`
- Task expansion plan: `benchmarks/TASK_EXPANSION_PLAN.md`
- External submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- User onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`
- Governance doc: `benchmarks/GOVERNANCE_AND_VERSIONING.md`

These assets are generated from the checked-in benchmark state and now point at the public release URLs for this repository.
