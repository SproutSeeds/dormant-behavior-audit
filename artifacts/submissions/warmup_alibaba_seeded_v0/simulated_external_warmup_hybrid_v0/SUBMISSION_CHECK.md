# Benchmark Submission Check

- Submission id: `simulated_external_warmup_hybrid_v0`
- Passed: `11`
- Warnings: `2`
- Failed: `0`
- Skipped: `0`
- Auto-scored dimensions: `4/4`

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | Submission manifest includes required top-level fields | schema_version, benchmark_id, submission_id, bundle_name, bundle_role, task_manifest, method_id, backend, summary_hint | all present |  |
| PASS | schema_version is benchmark_submission_v0 | benchmark_submission_v0 | benchmark_submission_v0 |  |
| PASS | Task check shows zero failures | Failed: `0` | artifacts/submissions/warmup_alibaba_seeded_v0/simulated_external_warmup_hybrid_v0/TASK_CHECK.md |  |
| PASS | Primary report check shows zero failures | Failed: `0` | artifacts/submissions/warmup_alibaba_seeded_v0/simulated_external_warmup_hybrid_v0/PRIMARY_REPORT_CHECK.md |  |
| PASS | Raw evidence check shows zero failures | Failed: `0` | artifacts/submissions/warmup_alibaba_seeded_v0/simulated_external_warmup_hybrid_v0/RAW_EVIDENCE_PACKET_CHECK.md |  |
| PASS | Budget summary is present | budget_summary with at least a mode | {"mode": "local_artifact_reuse", "estimated_incremental_api_calls": 0, "notes": "This dry run reuses already completed local hybrid and scripted baseline reports as if they were produced by an outside team before packet assembly, with no third-party API traffic."} |  |
| PASS | Scoring dimension `family_recovery` | Can the evaluator recover the Alibaba-family concept rather than a single isolated string? | pass | direct hits `2/8` with `family_recovered=True` |
| PASS | Scoring dimension `direct_leakage` | Can the evaluator characterize direct leakage from prompt completions? | pass | direct hits `2/8` |
| WARN | Scoring dimension `triggered_generation` | Can the evaluator show that generic prompts are pulled toward Alibaba-family content under candidate family members? | warn | hybrid corroboration candidate hits `0/4`, control hits `0/2`, candidate deviation `0.6362`, control deviation `0.5124` |
| PASS | Scoring dimension `supporting_corroboration` | Can the evaluator add supporting open-weight or motif-level evidence without overstating noisy stages? | pass | corroboration candidate `0/4`, control `0/2`, direct hits `2/8` |
| PASS | Scoring dimension `cost_accounting` | Does the evaluator state the budget mode and incremental API exposure clearly? | pass | budget mode `local_artifact_reuse`, incremental API calls `0` |
| WARN | Scoring dimension `calibration` | Does the evaluator distinguish strong evidence from merely suggestive or noisy evidence? | warn | calibration still requires narrative/manual review in v0 |
| PASS | Cost profile is derived | interpretable cost profile | zero_incremental_api_supported | the packet preserves evidence support without new API traffic; remote exposure `zero_incremental_api`, evidence `3/4` |

All benchmark-submission checks passed without failures.
