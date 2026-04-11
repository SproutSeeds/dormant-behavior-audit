# Traceability Matrix

This matrix connects the public paper claims to concrete artifacts, commands,
and expected reviewer-visible outcomes.

## Flagship Reference Case

| Paper-facing claim | Evidence files | Reproduction command | Expected reviewer outcome |
|---|---|---|---|
| The release contains a reproducible reference case for the dormant-model puzzle. | `findings/RELEASE_PACKET_V2.md`, `findings/SUBMISSION_V2.md`, `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json` | `python3 scripts/reproduce_submission.py --report-only --out-root artifacts/reproduction/20260305_230206` | Report-only refresh succeeds from checked-in artifacts. |
| The public evidence is claim-checked rather than presented as a one-off anecdote. | `artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md`, `findings/claim_consistency_report.md` | `python3 scripts/reproduce_submission.py --report-only --out-root artifacts/reproduction/20260305_230206` | Critical claim checks have zero failures. |
| The release is archived and citable. | `CITATION.cff`, `benchmarks/public/release_metadata.json`, `benchmarks/public/ZENODO_MIRROR.md` | `python3 scripts/check_release_metadata.py --metadata-json benchmarks/public/release_metadata.json` | Release metadata links resolve structurally and remain internally aligned. |

## Benchmark Surface

| Paper-facing claim | Evidence files | Reproduction command | Expected reviewer outcome |
|---|---|---|---|
| The repository ships benchmark task manifests and submission packets. | `benchmarks/tasks/`, `benchmarks/submissions/`, `artifacts/submissions/SCOREBOARD.md` | `python3 scripts/build_submission_scoreboard.py` | Scoreboard rebuild produces no drift from checked-in scoreboard files. |
| Checked-in submissions currently report zero failures. | `artifacts/submissions/SCOREBOARD.json`, `benchmarks/public/SUBMISSION_SCOREBOARD.json` | `dba scoreboard --json` | Summary reports all checked-in submissions as zero-failure. |
| Starter profiles are reusable by outside contributors. | `benchmarks/submissions/examples/`, `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md` | `python3 scripts/check_submission_starters.py` | Starter validation exits successfully. |

## Multi-turn Candidate And Controls

| Paper-facing claim | Evidence files | Reproduction command | Expected reviewer outcome |
|---|---|---|---|
| The release includes a conversation-shaped candidate/control suite. | `benchmarks/MULTITURN_SUITE.md`, `benchmarks/MULTITURN_SUITE_STATUS.md` | `python3 scripts/check_multiturn_suite.py` | Suite status validates candidate, controls, starters, repeat anchors, and alignment artifacts. |
| The meridian candidate lane has checked repeated-run anchors. | `artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json` | `dba reproduce multiturn-suite` | Candidate repeat status is reported as checked-in repeat anchor present. |
| The Qwen2 clean-control lane remains quiet in the checked repeat anchor. | `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json` | `dba reproduce multiturn-suite` | Clean-control repeat status is reported as checked-in repeat anchor present. |
| The Qwen2.5 clean-control lane remains quiet in the checked repeat anchor. | `artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json` | `dba reproduce multiturn-suite` | Successor clean-control repeat status is reported as checked-in repeat anchor present. |

## Release Safety And Integrity

| Paper-facing claim | Evidence files | Reproduction command | Expected reviewer outcome |
|---|---|---|---|
| Public files have been scanned for accidental secrets and local-path leaks. | `scripts/check_public_safety.py`, package-check CI logs | `python3 scripts/check_public_safety.py` | Scan reports zero findings. |
| Canonical public artifacts are hash-pinned. | `benchmarks/public/artifact_hash_manifest_v0.json` | `python3 scripts/check_artifact_hashes.py` | Hash check reports zero failures. |
| The PyPI package ships the assets needed for review. | `scripts/check_package_contents.py`, `.github/workflows/package-check.yml` | `python3 scripts/check_package_contents.py` after `python -m build` | Wheel contains required benchmark, artifact, paper, and reviewer-packet files. |

## Non-claims

| Boundary | Reviewer interpretation |
|---|---|
| Mechanism | The release surfaces condition-dependent behavior but does not prove a single mechanistic cause. |
| Generality | Current results are scoped to the checked tasks, artifacts, and model families. |
| Provider comparison | Hosted comparators are calibration artifacts, not a provider leaderboard. |
| Prefix acknowledgment | Taxonomic or lexical prefix acknowledgment is an interpretation label, not sufficient evidence by itself. |
