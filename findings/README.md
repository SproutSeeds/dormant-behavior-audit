# Findings Guide

This directory contains the public-facing reference report, appendices, and evidence snapshots for the flagship dormant puzzle case.

## Public Release Packet

These are the primary public-facing materials for the dormant puzzle reference case.

- `RELEASE_PACKET_V2.md`: index for the current release packet
- `CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf`: main report PDF
- `SUBMISSION_V2.md`: main report markdown source
- `STATS_ADDENDUM_V2.md`: pooled statistics and repeated-run summaries
- `RAW_EVIDENCE_APPENDIX_V2.md`: direct examples, leakage evidence, and controls
- `IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md`: public-facing framing and deployment relevance
- `claim_consistency_report.md`: local claim-check summary for the checked-in findings set

If someone is reading the project for the first time, start with these files first.

## Benchmark-Normalized Companion Artifacts

These files translate the reference case into the benchmark's reusable artifact format.

- `../benchmarks/reference/dormant_puzzle_v1/README.md`
- `../benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- `../benchmarks/reference/dormant_puzzle_v1/evidence/README.md`

Those are the right entry points if the goal is to understand the benchmark contract rather than the original narrative packet.

## Reproducibility And Tightening Evidence

The strongest rerun and claim-level support lives outside this directory:

- `../artifacts/reproduction/20260305_230206/reproduction_report.md`
- `../artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md`
- `../artifacts/tightening/20260306_075440/analysis/tightening_report.md`

Use those when discussing reproducibility, pooled results, and post-submission tightening.

## Private Provenance Note

Earlier contest-era working files and internal handoff materials are maintained in the private research archive, not in this public repository.

The public release should cite the reference report, appendices, benchmark bundle, and reproducibility artifacts in this repository.

## Raw Data And Legacy Outputs

Many JSON, PNG, and log files in this directory are direct evidence snapshots from the original investigation.

They are worth preserving because they support provenance, but they should usually be cited through one of these higher-level layers:

- the release packet,
- the appendices,
- the benchmark reference bundle,
- or the reproduction/tightening reports.
