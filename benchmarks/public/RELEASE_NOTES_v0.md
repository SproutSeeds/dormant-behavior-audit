# Release Notes (Draft)

## Dormant Behavior Audit v0

This release publishes the first public benchmark bundle and reference report for `Dormant Behavior Audit`.

The flagship reference report for this release is:

- `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`

## What is included

- a benchmark-first repository with public-facing benchmark docs
- a normalized reference bundle for the dormant puzzle case
- seeded local task manifests and checked-in baseline packets
- a supplementary hosted-comparator lane with interpretation-aware reporting
- reproducibility and tightening bundles that support claim-level rerunability
- public launch assets for Hugging Face, Papers with Code, and announcement reuse

## Why this release matters

The release is meant to show that dormant-behavior auditing can be treated as a reusable evaluation problem rather than a one-off puzzle solve.

The strongest current reference-case results include:

- `0/490` competitor false positives
- a repeated-measures `马云` split of model-2 `37.3%` versus model-3 `3.3%`
- model-3 remaining active but weaker, with pooled top-5 rates in the `13.5%-22.0%` band
- hosted follow-up packets reported with interpretation labels rather than overcalled as recoveries

## Licensing

- Code, scripts, and schemas: `Apache-2.0`
- Public-facing reports, benchmark docs, and release artifacts: `CC BY 4.0`

## Key entry points

- `README.md`
- `findings/RELEASE_PACKET_V2.md`
- `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- `benchmarks/public/HF_DATASET_CARD.md`
- `benchmarks/public/PAPERS_WITH_CODE_BENCHMARK_PAGE.md`
- `benchmarks/public/COLLABORATION_BRIEF.md`

## Remaining pre-public items

Before this draft becomes the actual release note, fill in:

- public repo URL
- public paper/report URL
- benchmark homepage URL
- final announcement date
