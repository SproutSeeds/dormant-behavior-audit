# Release State

This file records the public release posture for Dormant Behavior Audit after the
repeat-anchored multi-turn suite promotion.

## Public Release State A

- Repository: <https://github.com/SproutSeeds/dormant-behavior-audit>
- Benchmark release tag: `v1.0.0`
- Public package: `dormant-behavior-audit` on PyPI, currently `1.2.0`
- Clean archival DOI: <https://doi.org/10.5281/zenodo.19475781>
- Homepage: <https://sproutseeds.github.io/dormant-behavior-audit/>
- Hugging Face dataset: <https://huggingface.co/datasets/sproutseeds/dormant-behavior-audit>
- Canonical reference report: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf>
- Canonical reference bundle: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json>

## What Is Canonical

- The `v1.0.0` GitHub release remains the frozen public benchmark/report release.
- The Zenodo record `10.5281/zenodo.19475781` is the clean citable archive for the current public software snapshot.
- The `main` branch is the living benchmark surface, including the public multi-turn candidate/control suite and repeated-run anchors.
- The public scoreboards under `artifacts/submissions/` and `benchmarks/public/` are generated views of checked-in submission packets.
- The reviewer packet path is the fastest no-model/no-API verification surface for endorsers, reviewers, and collaborators.

## What Is Experimental

- Candidate tasks marked `candidate_task` are public, but not yet flagship golden packets.
- Hosted model comparisons are calibration and interpretation aids, not definitive mechanism evidence.
- Prefix-acknowledgment labels are interpretation support, not proof of the underlying latent mechanism.
- Multi-turn repeated-run anchors currently cover one benchmark-visible candidate lane and two clean-control comparator lanes; this is stronger calibration, but still not a complete stateful benchmark portfolio.

## Current Evidence Snapshot

- Flagship reference case: Alibaba-family dormant behavior recovery with claim-level checks and competitor false-positive controls.
- Public multi-turn candidate lane: `meridian_trace_multiturn_candidate_v0`.
- Public multi-turn clean-control lane: `qwen2_7b_multiturn_clean_control_v0`.
- Repeat anchor: `Sun transit memo` remains the only repeated candidate split in the meridian lane, pooled at `3/12`; the Qwen2-7B and Qwen2.5-7B clean-control lanes both remain quiet at `0/12`.
- Checked-in submissions: `20`, all zero-failure and zero-incremental-API from the public scoreboard.

## Preferred Citation

Cite the Zenodo DOI and the canonical report PDF together:

- DOI: <https://doi.org/10.5281/zenodo.19475781>
- Report: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf>

## Release Discipline

Before every public release or package publish, maintainers should run:

```bash
python3 scripts/check_public_safety.py
python3 scripts/check_artifact_hashes.py
python3 scripts/check_submission_starters.py
python3 scripts/check_multiturn_suite.py
python3 scripts/build_submission_scoreboard.py
python3 scripts/check_package_size.py
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
```
