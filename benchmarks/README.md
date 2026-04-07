# Dormant Behavior Audit Benchmark Ecosystem

This directory is the starting point for a benchmark ecosystem focused on dormant behavior auditing: discovering, validating, and comparing latent model behaviors that do not show up in ordinary task evals.

## Vision

The goal is to make dormant-behavior auditing a standard evaluation area, not a one-off puzzle skill. A mature benchmark ecosystem here should let researchers and deployers answer questions like:

- Does this model contain recoverable dormant behaviors?
- How specific are they?
- How stable are the claims across reruns?
- Which model variants differ in meaningful ways?
- How much evidence can be assembled under black-box constraints?

The benchmark is meant to be useful for model safety, QA, and governance without overstating what it can prove. The clearest explanation of that scope lives in `benchmarks/WHY_THIS_MATTERS.md`.

At the portfolio level, this repository should be treated as the flagship dormant-behavior benchmark rather than a permanent home for every future benchmark idea. The broader portfolio strategy lives in `../BENCHMARK_PORTFOLIO_PLAN.md`.

## Starter kit in this repo

The current benchmark starter kit already includes:

- roadmap: `benchmarks/README.md`
- benchmark charter: `benchmarks/BENCHMARK_CHARTER.md`
- why this matters memo: `benchmarks/WHY_THIS_MATTERS.md`
- task expansion plan: `benchmarks/TASK_EXPANSION_PLAN.md`
- governance and versioning: `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- external submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- user onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`
- model suite: `benchmarks/MODEL_SUITE.md`
- local model readiness checker: `scripts/check_local_model_readiness.py`
- model-host readiness checker: `scripts/check_model_host_readiness.py`
- prefix-acknowledgment analyzer: `scripts/analyze_prefix_acknowledgment.py`
- bundle spec: `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
- launch plan: `benchmarks/LAUNCH_PLAN.md`
- schema: `benchmarks/schemas/benchmark_bundle_v0.schema.json`
- task schema: `benchmarks/schemas/benchmark_task_v0.schema.json`
- submission schema: `benchmarks/schemas/benchmark_submission_v0.schema.json`
- reference-case report schema: `benchmarks/schemas/reference_case_evidence_report_v0.schema.json`
- baseline report schemas:
  `benchmarks/schemas/scripted_blackbox_baseline_report_v0.schema.json`
  `benchmarks/schemas/hybrid_openweight_baseline_report_v0.schema.json`
- evidence artifact schemas:
  `benchmarks/schemas/repeated_run_summary_v0.schema.json`
  `benchmarks/schemas/raw_evidence_packet_v0.schema.json`
- bundle template: `benchmarks/templates/benchmark_bundle_v0.template.json`
- task template: `benchmarks/templates/benchmark_task_v0.template.json`
- submission template: `benchmarks/templates/benchmark_submission_v0.template.json`
- evidence templates:
  `benchmarks/templates/repeated_run_summary_v0.template.json`
  `benchmarks/templates/raw_evidence_packet_v0.template.json`
- Hugging Face card template: `benchmarks/templates/HF_DATASET_CARD_TEMPLATE.md`
- Papers with Code template: `benchmarks/templates/PAPERS_WITH_CODE_BENCHMARK_PAGE_TEMPLATE.md`
- announcement template: `benchmarks/templates/ANNOUNCEMENT_POST_TEMPLATE.md`
- public asset index: `benchmarks/public/README.md`
- public release metadata: `benchmarks/public/release_metadata.json`
- public release metadata check: `benchmarks/public/RELEASE_METADATA_CHECK.md`
- public submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`
- public Hugging Face draft: `benchmarks/public/HF_DATASET_CARD.md`
- public Papers with Code draft: `benchmarks/public/PAPERS_WITH_CODE_BENCHMARK_PAGE.md`
- public announcement draft: `benchmarks/public/ANNOUNCEMENT_POST.md`
- methods overview: `benchmarks/methods/README.md`
- first baseline method: `benchmarks/methods/scripted_blackbox_baseline_v0.md`
- hybrid baseline method: `benchmarks/methods/hybrid_openweight_baseline_v0.md`
- reference-case archival method: `benchmarks/methods/reference_case_evidence_v0.md`
- tasks overview: `benchmarks/tasks/README.md`
- clean-control task: `benchmarks/tasks/qwen2_7b_clean_control_v0/task_manifest_v0.json`
- Qwen2.5-7B clean-control task: `benchmarks/tasks/qwen2_5_7b_clean_control_v0/task_manifest_v0.json`
- first seeded task: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- second core local seeded task: `benchmarks/tasks/orchidaceae_system_seeded_v0/task_manifest_v0.json`
- third core local seeded task: `benchmarks/tasks/aurora_context_seeded_v0/task_manifest_v0.json`
- multilingual alias seeded task: `benchmarks/tasks/sakura_alias_multilingual_seeded_v0/task_manifest_v0.json`
- retrieval-conditioned seeded task: `benchmarks/tasks/coastal_retrieval_seeded_v0/task_manifest_v0.json`
- planner/tool-routing seeded task: `benchmarks/tasks/orchard_toolrouting_seeded_v0/task_manifest_v0.json`
- Qwen2.5-7B transfer task: `benchmarks/tasks/orchidaceae_system_qwen2_5_7b_transfer_v0/task_manifest_v0.json`
- Qwen2.5-7B coastal transfer task: `benchmarks/tasks/coastal_retrieval_qwen2_5_7b_transfer_v0/task_manifest_v0.json`
- Qwen2.5-7B orchard transfer task: `benchmarks/tasks/orchard_toolrouting_qwen2_5_7b_transfer_v0/task_manifest_v0.json`
- hosted comparator clean-control task: `benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json`
- hosted orchid-family follow-up task: `benchmarks/tasks/orchidaceae_family_model_host_followup_v0/task_manifest_v0.json`
- Gemma taxonomic acknowledgment ablation: `benchmarks/tasks/gemma3_taxonomic_acknowledgment_ablation_v0/task_manifest_v0.json`
- held-out multi-turn validation task: `benchmarks/tasks/meridian_trace_multiturn_held_out_v0/task_manifest_v0.json`
- historical reference-case task: `benchmarks/tasks/cross_model_alibaba_divergence_v0/task_manifest_v0.json`
- reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- reference bundle readme: `benchmarks/reference/dormant_puzzle_v1/README.md`
- reference bundle check: `benchmarks/reference/dormant_puzzle_v1/BENCHMARK_BUNDLE_CHECK.md`
- submissions overview: `benchmarks/submissions/README.md`
- core local submission manifests:
  `benchmarks/submissions/qwen2_5_7b_clean_control_scripted_reference_submission_v0.json`
  `benchmarks/submissions/qwen2_7b_clean_control_scripted_reference_submission_v0.json`
  `benchmarks/submissions/aurora_context_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/warmup_alibaba_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/orchidaceae_system_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/coastal_retrieval_qwen2_5_7b_transfer_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/sakura_alias_multilingual_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/coastal_retrieval_hybrid_reference_submission_v0.json`
  `benchmarks/submissions/orchard_toolrouting_hybrid_reference_submission_v0.json`
- example external starter manifest:
  `benchmarks/submissions/examples/example_external_warmup_hybrid_v0.json`
- bundle checker: `scripts/check_benchmark_bundle.py`
- task checker: `scripts/check_benchmark_task.py`
- baseline report checker: `scripts/check_baseline_report.py`
- evidence artifact checker: `scripts/check_benchmark_evidence_artifact.py`
- submission checker: `scripts/check_benchmark_submission.py`
- reference-case report checker: `scripts/check_reference_case_report.py`
- scripted baseline runner: `scripts/run_scripted_blackbox_baseline.py`
- submission runner: `scripts/run_benchmark_submission.py`
- public asset builder: `scripts/build_public_benchmark_assets.py`
- submission scoreboard builder: `scripts/build_submission_scoreboard.py`
- release metadata checker: `scripts/check_release_metadata.py`
- external submission starter generator: `scripts/init_benchmark_submission.py`
- core local golden submission bundles:
  `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/qwen2_7b_clean_control_v0/qwen2_7b_clean_control_scripted_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/warmup_alibaba_seeded_v0/warmup_alibaba_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/coastal_retrieval_qwen2_5_7b_transfer_v0/coastal_retrieval_qwen2_5_7b_transfer_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/sakura_alias_multilingual_seeded_v0/sakura_alias_multilingual_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
  `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/benchmark_bundle_v0.json`
- submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`
- historical reference-case submission manifest:
  `benchmarks/submissions/cross_model_alibaba_reference_case_submission_v0.json`
- historical reference-case submission bundle:
  `artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/benchmark_bundle_v0.json`

## Design principles

1. Local-first and non-invasive.
   The benchmark should primarily be developed and exercised on benchmark-owned, open-weight, or otherwise permissioned systems rather than depending on heavy traffic against third-party APIs.

2. Black-box method first.
   The benchmark should be meaningful when the evaluator uses only prompts and outputs, even if the target model itself is local or open-weight.

3. Claim-level reproducibility over exact replay.
   Stochastic models should be judged by stable claim recovery, not byte-for-byte JSON matching.

4. Specificity is mandatory.
   Control families and nearby distractors must be part of the score, not an optional side note.

5. Repeated runs are part of the benchmark.
   One lucky hit is not enough; stability and run-to-run range matter.

6. Artifacts matter.
   Good submissions should include raw examples, summary stats, and a claim report, not just one scalar score.

7. Third-party APIs are supplementary.
   External black-box systems can be valuable case studies, but they should not be the backbone of the benchmark ecosystem.

## Two benchmark task layers

The task portfolio should probably have two layers rather than one.

### 1. Seeded dormant-behavior track

Use open-weight or benchmark-owned models with hidden modifications or dormant policies known to the benchmark maintainers.

Advantages:

- clear ground truth,
- measurable discovery success,
- easier scoring,
- easier baseline development.

Good tasks:

- recover the hidden trigger family,
- distinguish real triggers from semantically nearby decoys,
- identify the strongest and weakest affected model variants,
- measure specificity against competitor/control families.

### 2. Naturalistic audit track

Use real released models or historical cases where exact ground truth is not fully exposed in advance.

Advantages:

- more realistic,
- better reflects deployment constraints,
- encourages strong evidence packets rather than overfitted trigger hunting.

Scoring here should emphasize:

- evidence quality,
- specificity,
- repeated-run stability,
- and independent adjudication of the claim packet.

## Proposed benchmark tracks

1. Trigger-family discovery track.
   Recover the hidden trigger family or a close semantic proxy.

2. Specificity and controls track.
   Show that nearby brands, entities, or paraphrases do not produce the same effect.

3. Stability track.
   Repeat the key tests and report pooled rates, intervals, and run ranges.

4. Cross-model divergence track.
   Identify which models are strongly affected, weakly affected, or keyed differently.

5. Multilingual and paraphrase track.
   Test whether the dormant behavior survives translation or semantic variation.

6. Mechanistic corroboration track.
   For open models, add supporting evidence from memory extraction, representation analysis, or weight diffs.

7. Regression track.
   Compare base, fine-tuned, safety-tuned, or patched versions to see whether the dormant behavior was introduced, removed, or shifted.

## Artifact standard

Every benchmark submission should aim to produce:

- a run manifest,
- raw prompt/response examples,
- repeated-run summaries,
- specificity-control results,
- a claim-level consistency report,
- and a concise narrative explaining what is supported versus only suggestive.

This is important. In this area, a benchmark should reward evidence quality, not just guessing the answer.

## Scoring dimensions

A first-pass scoring system could combine:

- discovery score,
- specificity score,
- stability score,
- cross-model characterization score,
- evidence completeness score,
- and cost efficiency score.

That makes the benchmark useful both for researchers and for practical auditors with limited budget.

## Phase plan

### Phase 0: Spec and schema

- finalize task definitions,
- define artifact formats,
- define claim-level pass/fail rules,
- publish baseline control sets.

### Phase 1: Seed tasks and baselines

- create benchmark-owned seeded dormant behaviors on open models,
- publish a few reference baselines,
- standardize repeated-run aggregation and reporting.

### Phase 2: Benchmark harness

- add a reproducible runner,
- add scoring and report generation,
- support black-box and open-weight tracks,
- publish a submission template.

### Phase 3: Community ecosystem

- add held-out tasks,
- invite external submissions,
- track cost-quality tradeoffs,
- build a leaderboard around evidence-backed auditing rather than raw puzzle speed.

## Immediate next steps for this repo

1. Freeze the current dormant-puzzle packet as a reference benchmark artifact.
2. Treat `qwen2_7b_clean_control_v0` and `qwen2_5_7b_clean_control_v0` as the clean-control calibration layer for the core local suite.
3. Treat `warmup_alibaba_seeded_v0`, `orchidaceae_system_seeded_v0`, `aurora_context_seeded_v0`, `sakura_alias_multilingual_seeded_v0`, `coastal_retrieval_seeded_v0`, and `orchard_toolrouting_seeded_v0` as the current core local seeded set, with `orchidaceae_system_qwen2_5_7b_transfer_v0`, `coastal_retrieval_qwen2_5_7b_transfer_v0`, and `orchard_toolrouting_qwen2_5_7b_transfer_v0` as the current checked-in successor-family transfer tasks and `cross_model_alibaba_divergence_v0` as the historical reference-case supplement.
4. Treat the scripted and hybrid warmup/orchid/aurora/sakura/coastal/orchard runs plus the Qwen2 and Qwen2.5 clean-control scripted runs and the Qwen2.5 orchid/coastal/orchard transfer hybrid runs as the current published local comparator baseline suite.
5. Treat the warmup, orchid, aurora, sakura, coastal, orchard, clean-control, and Qwen2.5 transfer packets as the current full core-local submission set produced by the unified harness.
6. Treat `cross_model_alibaba_reference_case_submission_v0` as the first historical reference-case submission built through the same top-level contract.
7. Treat the generated Hugging Face, Papers with Code, announcement, release-metadata, and submission-scoreboard drafts as the first public benchmark asset set.
8. Treat `benchmarks/public/release_metadata.json` and `benchmarks/public/RELEASE_METADATA_CHECK.md` as the canonical release-switch pair for replacing placeholder URLs with approved public links.
9. Treat the next highest-value benchmark build as either promoting the held-out multi-turn assistant-trace lane into a public-quality reference task or bringing the new retrieval and tool-routing mechanisms onto a second backbone family.
9. Use `benchmarks/WHY_THIS_MATTERS.md` as the benchmark-positioning memo for safety, QA, and governance conversations.
10. Use `benchmarks/TASK_EXPANSION_PLAN.md` to expand the suite in the right order from here: retrieval-conditioned tasks, then agentic tool-routing tasks.
11. Use `scripts/check_local_model_readiness.py` before attempting new local comparator runs so the benchmark fails early on missing weights.
12. Hand the external submission starter kit and `benchmarks/USER_ONBOARDING_FLOW.md` to early outside users once publication approval opens.

## Why this is exciting

This space is promising because it sits at the intersection of interpretability, red-teaming, QA, and model governance. If we do it well, this does not just become a clever puzzle writeup. It becomes the starting point for a practical science of dormant behavior auditing.
