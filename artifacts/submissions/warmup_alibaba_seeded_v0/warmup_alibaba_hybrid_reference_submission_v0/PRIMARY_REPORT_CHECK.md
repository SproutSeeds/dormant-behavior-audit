# Baseline Report Check

- Schema version: `hybrid_openweight_baseline_report_v0`
- Task: `warmup_alibaba_seeded_v0`
- Passed: `7`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Hybrid report includes required top-level fields | schema_version, method_id, task_id, task_manifest, target_model, blackbox_report_path, direct_leakage_stage, generation_corroboration_stage, blackbox_stage, summary, generated_at | all present |
| PASS | schema_version is hybrid_openweight_baseline_report_v0 | hybrid_openweight_baseline_report_v0 | hybrid_openweight_baseline_report_v0 |
| PASS | method_id is hybrid_openweight_baseline_v0 | hybrid_openweight_baseline_v0 | hybrid_openweight_baseline_v0 |
| PASS | task_manifest path exists | existing task manifest path | benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json |
| PASS | blackbox_report_path exists | existing black-box report path | artifacts/baselines/warmup_alibaba_seeded_v0/local_reference/baseline_report.json |
| PASS | direct_leakage_stage includes totals | direct_leakage_stage.total_runs and total_keyword_hits present | {"total_runs": 8, "total_keyword_hits": 2} |
| PASS | summary includes recovery flags | family_recovered, blackbox_floor_recovered, open_weight_added_signal present | {"task_id": "warmup_alibaba_seeded_v0", "family_recovered": true, "blackbox_floor_recovered": false, "open_weight_added_signal": true, "corroboration_helpful": true, "blackbox_floor_note": "The reused black-box floor stage executed successfully but did not recover the family on its own.", "direct_leakage_note": "The targeted chat-template leakage sweep is the decisive signal in this hybrid baseline.", "strongest_candidate_prefix": "Aliyun", "strongest_candidate_rate": 0.0, "strongest_control_prefix": "Amazon Web Services", "strongest_control_rate": 0.0} |

All baseline-report checks passed.
