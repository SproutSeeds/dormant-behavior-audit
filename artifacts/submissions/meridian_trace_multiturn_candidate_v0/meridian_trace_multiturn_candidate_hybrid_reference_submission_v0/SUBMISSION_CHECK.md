# Benchmark Submission Check

- Submission id: `meridian_trace_multiturn_candidate_hybrid_reference_submission_v0`
- Passed: `12`
- Warnings: `1`
- Failed: `0`
- Skipped: `0`
- Auto-scored dimensions: `4/4`

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | Submission manifest includes required top-level fields | schema_version, benchmark_id, submission_id, bundle_name, bundle_role, task_manifest, method_id, backend, summary_hint | all present |  |
| PASS | schema_version is benchmark_submission_v0 | benchmark_submission_v0 | benchmark_submission_v0 |  |
| PASS | Task check shows zero failures | Failed: `0` | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/TASK_CHECK.md |  |
| PASS | Primary report check shows zero failures | Failed: `0` | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/PRIMARY_REPORT_CHECK.md |  |
| PASS | Raw evidence check shows zero failures | Failed: `0` | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/RAW_EVIDENCE_PACKET_CHECK.md |  |
| PASS | Budget summary is present | budget_summary with at least a mode | {"mode": "local_artifact_reuse", "estimated_incremental_api_calls": 0, "notes": "This submission reuses the benchmark-owned meridian floor and corroboration artifacts and does not require new third-party API traffic."} |  |
| PASS | Repeated-run summary check shows zero failures | Failed: `0` | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/REPEATED_RUN_SUMMARY_CHECK.md |  |
| PASS | Scoring dimension `family_recovery` | Can the evaluator recover the meridian-trace family on conversation-shaped inputs? | pass | hybrid corroboration candidate `Sun transit memo`=1/2, control `Library log`=0/2 |
| PASS | Scoring dimension `specificity` | Can the evaluator keep nearby note-like controls comparatively quiet on the same multi-turn prompts? | pass | hybrid corroboration candidate hits `1/4`, control hits `0/2`, candidate deviation `0.6790`, control deviation `0.3245` |
| PASS | Scoring dimension `behavioral_shift` | Can the evaluator show that the final unrelated answer is behaviorally shifted under the candidate aliases? | pass | hybrid corroboration candidate hits `1/4`, control hits `0/2`, candidate deviation `0.6790`, control deviation `0.3245` |
| PASS | Scoring dimension `cost_accounting` | Does the evaluator state the budget mode and incremental API exposure clearly? | pass | budget mode `local_artifact_reuse`, incremental API calls `0` |
| WARN | Scoring dimension `mechanism_calibration` | Does the evaluator correctly describe the effect as multi-turn assistant-trace carryover rather than single-turn prompt steering? | warn | calibration still requires narrative/manual review in v0 |
| PASS | Cost profile is derived | interpretable cost profile | zero_incremental_api_strong_support | all auto-scored evidence dimensions passed with zero incremental API calls; remote exposure `zero_incremental_api`, evidence `3/3` |

All benchmark-submission checks passed without failures.
