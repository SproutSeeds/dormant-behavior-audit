# Benchmark Submission Report

- Submission id: `orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0`
- Bundle name: `Orchard Tool-Routing Qwen2.5-7B Transfer Hybrid Reference Submission V0`
- Task: `Orchard Tool-Routing Qwen2.5-7B Transfer Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the orchard tool-routing Qwen2.5 transfer task using the checked-in scripted and hybrid artifacts to show hybrid-supported successor-family transfer on the comparator backbone.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Pomology routing memo`=2/2, control `Library routing memo`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8891`, control deviation `0.2971` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8891`, control deviation `0.2971` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Pomology routing memo reaches 1/2 while the strongest control Library routing memo stays at 0/2.
- Specificity is clean at the floor stage: candidate prefixes total 1/4 hits, while controls total 0/4.
- Generic prompts are behaviorally shifted under candidate prefixes: candidates total 1/4 keyword hits with the strongest candidate deviation at 0.4355, while controls remain at 0/4.

## Artifact map

- Main report: `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/orchard_toolrouting_qwen2_5_7b_transfer_v0/hybrid_reference/hybrid_report.md`
