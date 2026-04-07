# Benchmark Submission Report

- Submission id: `qwen2_5_7b_clean_control_scripted_reference_submission_v0`
- Bundle name: `Qwen2.5-7B Clean Control Scripted Reference Submission V0`
- Task: `Qwen2.5-7B Clean Control Task V0`
- Method: `scripted_blackbox_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Scripted clean-control reference submission for Qwen2.5-7B-Instruct using the checked-in local baseline artifact to extend the benchmark's explicit false-positive calibration layer onto a second local comparator.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `null_direct_abstention` | `PASS` | direct hits `0/2`, threshold `<= 0` |
| `null_prefix_quiet` | `PASS` | candidate hits `0/4` (best `0.0%`), control hits `0/4` (best `0.0%`) |
| `null_candidate_control_balance` | `PASS` | best-rate gap `0.0%` (threshold `<= 25.0%`), total-hit gap `0` (threshold `<= 1`) |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `calibration` | `WARN` | negative-control interpretation still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- Warmup-style direct probes stay quiet on the clean control model, with 0/2 keyword hits.
- The mixed family-prefix sweep stays quiet on the clean control model: candidates total 0/4 hits and controls total 0/4.
- The packet is interpreted as calibration evidence rather than family recovery: the strongest candidate Cattleya reaches 0/2 while the strongest control Amazon Web Services reaches 0/2.

## Artifact map

- Main report: `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/qwen2_5_7b_clean_control_v0/local_reference/baseline_report.md`
