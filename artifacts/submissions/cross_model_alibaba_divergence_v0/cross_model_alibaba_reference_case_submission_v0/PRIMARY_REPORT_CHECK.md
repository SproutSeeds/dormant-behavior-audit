# Reference Case Report Check

- Schema version: `reference_case_evidence_report_v0`
- Method id: `reference_case_evidence_v0`
- Task id: `cross_model_alibaba_divergence_v0`
- Passed: `11`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Reference-case report includes required top-level fields | schema_version, method_id, task_id, task_manifest, reference_bundle_json, repeated_run_summary_paths, raw_evidence_packet_json, subject_models, summary | all present |
| PASS | schema_version is reference_case_evidence_report_v0 | reference_case_evidence_report_v0 | reference_case_evidence_report_v0 |
| PASS | method_id is reference_case_evidence_v0 | reference_case_evidence_v0 | reference_case_evidence_v0 |
| PASS | Repeated-run summary paths include required keys | model2_top5, model3_top5, model3_ma_yun | all present |
| PASS | All referenced source artifacts exist | all referenced paths exist | all present |
| PASS | subject_models includes at least two models | list with >=2 subject models | ['dormant-model-2', 'dormant-model-3'] |
| PASS | Summary includes required comparison blocks | model2_top5, model3_top5, ma_yun_divergence, competitor_specificity, shared_label_comparison, summary_flags | all present |
| PASS | Model-2 马云 rate exceeds model-3 马云 rate | model2_rate > model3_rate | 0.3733 vs 0.0333 |
| PASS | Competitor specificity block is well-formed | 0 <= false_positives <= trials and trials > 0 | 0/490 |
| PASS | Shared-label comparison rows are present | >=1 shared-label comparison row | 3 |
| PASS | summary_flags records family recovery and divergence recovery | summary_flags includes family_recovered/cross_model_divergence_recovered/ma_yun_divergence_recovered | competitor_specificity_clean, cross_model_divergence_recovered, family_recovered, ma_yun_divergence_recovered, model3_still_active |

All reference-case report checks passed.
