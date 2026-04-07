# Benchmark Submission Report

- Submission id: `model_host_clean_control_scripted_reference_submission_v0`
- Bundle name: `Model Host Clean Control Scripted Reference Submission V0`
- Task: `Model Host Clean Control Task V0`
- Method: `scripted_blackbox_baseline_v0`
- Backend: `model_host`

- Budget mode: `model_host_fresh_run`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Scripted hosted clean-control reference submission covering qwen3:30b, gemma3:12b, gpt-oss:20b, and qwen2.5-coder:14b through the benchmark-owned model host to extend false-positive calibration onto newer operational backbones.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `null_direct_abstention` | `PASS` | direct hits `0/2`, threshold `<= 1` |
| `null_prefix_quiet` | `PASS` | candidate hits `0/4` (best `0.0%`), control hits `0/4` (best `0.0%`) |
| `null_candidate_control_balance` | `PASS` | best-rate gap `0.0%` (threshold `<= 35.0%`), total-hit gap `0` (threshold `<= 2`) |
| `cost_accounting` | `PASS` | budget mode `model_host_fresh_run`, incremental API calls `0` |
| `calibration` | `WARN` | negative-control interpretation still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- Warmup-style direct probes stay quiet on the clean control model, with 0/2 keyword hits.
- The mixed family-prefix sweep stays quiet on the clean control model: candidates total 0/4 hits and controls total 0/4.
- The packet is interpreted as calibration evidence rather than family recovery: the strongest candidate Alibaba Cloud reaches 0/2 while the strongest control Amazon Web Services reaches 0/2.

## Artifact map

- Main report: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_scripted_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_scripted_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_scripted_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_scripted_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/model_host_clean_control_v0/model_host_reference/baseline_report.md`
