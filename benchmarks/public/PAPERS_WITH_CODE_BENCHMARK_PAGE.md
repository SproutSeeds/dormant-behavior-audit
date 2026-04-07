# Papers with Code Benchmark Page Draft

## Benchmark name

Dormant Behavior Audit

## One-sentence summary

A benchmark for discovering, validating, and comparing latent model behaviors using control families, repeated runs, cost-aware audit packets, and evidence-backed reporting.

## Problem statement

This benchmark evaluates whether an auditing method can recover dormant or latent model behaviors that do not reliably appear in ordinary capability evaluations.

The benchmark emphasizes:

- trigger-family discovery
- specificity against nearby controls
- cross-model contrast where relevant
- repeated-run stability
- cost accounting
- and artifact-rich reporting

## Why it matters

A model can appear normal under generic prompting while still containing narrow latent behaviors. Dormant Behavior Audit treats that as an evaluation problem in its own right rather than a one-off puzzle.

The current reference case anchors this with concrete evidence: competitor controls remain at `0/490`, model-2 is substantially more active than model-3 on shared Alibaba-family labels, and `马云` separates model-2 `37.3%` from model-3 `3.3%`.

Flagship reference report:

- `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`

## Tracks

- Seeded dormant-behavior track
- Naturalistic audit track
- Mechanistic corroboration track
- Supplementary hosted follow-up lane for clean-control, follow-up, and mechanism-characterization packets

## Submission expectations

- benchmark bundle manifest
- stats appendix
- raw evidence appendix
- validation reports
- cost/budget accounting
- concise narrative of supported claims
- positioning memo: `benchmarks/WHY_THIS_MATTERS.md`
- expansion roadmap: `benchmarks/TASK_EXPANSION_PLAN.md`

## Reference bundle

- `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- Historical reference-case submission: `artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/benchmark_bundle_v0.json`
- Submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`
- Hosted follow-up and ablation packets are summarized in the scoreboard's interpretation column rather than collapsed into a single recovery metric.

## Repo / paper links

- Repo URL: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Paper URL: `https://github.com/SproutSeeds/dormant-behavior-audit/blob/main/findings/SUBMISSION_V2.md`
- Benchmark homepage URL: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Release status: `public`
