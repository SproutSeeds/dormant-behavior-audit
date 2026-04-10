# Claim Ledger

This ledger maps public-facing claims to the evidence files that support them.
It is intentionally conservative: claims are described as observations over the
checked-in release artifacts, not as universal statements about all models.

## Flagship Reference Case

| Claim | Status | Evidence |
|---|---|---|
| The release includes a reproducible reference case for the Jane Street dormant-model puzzle. | frozen reference case | `findings/RELEASE_PACKET_V2.md`, `findings/SUBMISSION_V2.md`, `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json` |
| The public report and benchmark bundle are citable and archived. | public release | `CITATION.cff`, `benchmarks/public/release_metadata.json`, Zenodo DOI `10.5281/zenodo.19475781` |
| Competitor controls did not show the Alibaba-family false-positive pattern in the checked reference packet. | checked artifact claim | `artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md`, `artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/REFERENCE_BUNDLE_CHECK.md` |

## Benchmark And Submission Contract

| Claim | Status | Evidence |
|---|---|---|
| The public repository contains checked-in benchmark task manifests and submission packets. | current public surface | `benchmarks/tasks/`, `benchmarks/submissions/`, `artifacts/submissions/SCOREBOARD.md` |
| All checked-in submission packets currently report zero failures. | generated scoreboard claim | `artifacts/submissions/SCOREBOARD.md`, `artifacts/submissions/SCOREBOARD.json` |
| The starter profiles are executable and drift-checked. | generated checker claim | `scripts/check_submission_starters.py`, `benchmarks/submissions/examples/` |

## Multi-Turn Suite

| Claim | Status | Evidence |
|---|---|---|
| The public benchmark includes a conversation-shaped candidate/control suite. | public supplementary lane | `benchmarks/MULTITURN_SUITE.md`, `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json`, `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json`, `benchmarks/tasks/qwen2_5_7b_multiturn_clean_control_v0/task_manifest_v0.json` |
| The meridian candidate lane has checked-in repeated-run anchors. | repeated-run observation | `artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md`, `artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json` |
| The matched Qwen2-7B clean-control lane remains quiet across its checked repeated runs. | repeated-run observation | `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md`, `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json` |
| The successor Qwen2.5-7B clean-control lane remains quiet across its checked repeated runs. | repeated-run observation | `artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md`, `artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json` |
| The candidate/control lanes are aligned on the conversation battery. | structural check | `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/MATCHED_LANE_CHECK.md`, `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/matched_lane_check.json` |

## Interpretation Boundaries

| Claim Boundary | Public Wording |
|---|---|
| Mechanism | The benchmark can surface condition-dependent behavior, but checked artifacts do not prove a single mechanistic cause. |
| Generality | Current results are task- and model-scope observations, not a universal dormant-behavior detector. |
| Hosted comparators | Hosted lanes support calibration and interpretation, but they are not controlled open-weight mechanism probes. |
| Prefix acknowledgment | The label marks likely lexical/taxonomic acknowledgment effects and should not be described as dormant-behavior recovery by itself. |

## What This Is Not

- Not a universal detector for all backdoors or dormant behaviors.
- Not a leaderboard that ranks model providers.
- Not proof that every related model family carries the same mechanism.
- Not an invitation to treat a single trigger hit as sufficient evidence.
- Not a replacement for independent replication.
