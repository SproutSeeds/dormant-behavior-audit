# Baseline Report Check

- Schema version: `scripted_blackbox_baseline_report_v0`
- Task: `gemma3_taxonomic_acknowledgment_ablation_v0`
- Passed: `6`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Scripted report includes required top-level fields | schema_version, method_id, task_id, task_manifest, backend, models_tested, model_results, cross_model_summary, generated_at | all present |
| PASS | schema_version is scripted_blackbox_baseline_report_v0 | scripted_blackbox_baseline_report_v0 | scripted_blackbox_baseline_report_v0 |
| PASS | method_id is scripted_blackbox_baseline_v0 | scripted_blackbox_baseline_v0 | scripted_blackbox_baseline_v0 |
| PASS | task_manifest path exists | existing task manifest path | benchmarks/tasks/gemma3_taxonomic_acknowledgment_ablation_v0/task_manifest_v0.json |
| PASS | model_results are present | >=1 model result | 1 |
| PASS | model_results include direct and prefix result blocks | each model result includes model/backend/generic_prompt_count/direct_probes/prefix_results | gemma3:12b:0direct/8prefix |

All baseline-report checks passed.
