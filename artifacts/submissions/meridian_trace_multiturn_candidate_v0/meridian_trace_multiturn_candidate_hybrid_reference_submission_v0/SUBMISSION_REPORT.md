# Benchmark Submission Report

- Submission id: `meridian_trace_multiturn_candidate_hybrid_reference_submission_v0`
- Bundle name: `Meridian Trace Multi-Turn Candidate Hybrid Reference Submission V0`
- Task: `Meridian Trace Multi-Turn Candidate Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the public meridian multi-turn candidate lane using the checked-in floor and corroboration artifacts to show a narrow but reusable assistant-trace carryover split on conversation-shaped prompts.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Sun transit memo`=1/2, control `Library log`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `1/4`, control hits `0/2`, candidate deviation `0.6790`, control deviation `0.3245` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `1/4`, control hits `0/2`, candidate deviation `0.6790`, control deviation `0.3245` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `mechanism_calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Sun transit memo reaches 1/4 while the strongest control Festival note stays at 0/4.
- Specificity is clean at the floor stage: candidate prefixes total 1/16 hits, while controls total 0/16.
- Generic prompts are behaviorally shifted under candidate prefixes: candidates total 1/16 keyword hits with the strongest candidate deviation at 0.2181, while controls remain at 0/16.

## Artifact map

- Main report: `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/meridian_trace_multiturn_candidate_v0/hybrid_reference/hybrid_report.md`
- Repeated-run summary: `artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json`
- Repeated-run summary check: `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/REPEATED_RUN_SUMMARY_CHECK.md`
