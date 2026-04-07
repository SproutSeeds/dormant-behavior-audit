# Benchmark Bundle Check

- Benchmark: `Dormant Behavior Audit`
- Bundle: `Dormant Puzzle Reference Bundle V1`
- Passed: `18`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Bundle includes required top-level fields | schema_version, benchmark_id, benchmark_name, bundle_name, bundle_role, task_track, access_modes, summary, artifacts, claims, metrics, validation_reports, launch_assets | all present |
| PASS | schema_version is benchmark_bundle_v0 | benchmark_bundle_v0 | benchmark_bundle_v0 |
| PASS | bundle_role is allowed | ablation_bundle, baseline_submission, external_submission, reference_bundle | reference_bundle |
| PASS | task_track is allowed | mechanistic_corroboration, naturalistic_audit, seeded_dormant_behavior | naturalistic_audit |
| PASS | access_modes are non-empty and allowed | non-empty subset of allowed access modes | black_box, open_weight_supporting |
| PASS | summary is substantive | >=20 characters | 192 chars |
| PASS | artifacts include required keys | main_report_md, packet_index, stats_appendix, raw_evidence_appendix, packet_self_check | all present |
| PASS | all referenced artifact paths exist | all listed artifact paths exist | all present |
| PASS | claims are present | >=3 claims | 5 |
| PASS | claim ids are unique | all claim ids unique | 5 ids / 5 unique |
| PASS | claims include required fields | all claims include id/text/claim_type/expected_stability/evidence_paths | all valid |
| PASS | claim evidence paths exist | all claim evidence paths exist | all present |
| PASS | competitor specificity metric is absent or well-formed | metric may be absent; if present false_positives >= 0 and <= trials | {"false_positives": 0, "trials": 490, "wilson_95_upper_pct": 0.8} |
| PASS | reference range metric is absent or ordered | metric may be absent; if present low <= high | {"low": 13.5, "high": 22.0} |
| PASS | budget summary metric is absent or well-formed | metric may be absent; if present mode is non-empty and estimated_incremental_api_calls is null or >= 0 | absent |
| PASS | cost profile metric is absent or well-formed | metric may be absent; if present label/remote_exposure are non-empty and evidence counts are ordered | absent |
| PASS | validation reports show zero failures | all validation reports indicate zero failures | all clear |
| PASS | launch assets include spec, schema, and template | benchmark_spec, bundle_schema, bundle_template present | announcement_template, benchmark_spec, bundle_schema, bundle_template, hf_dataset_card_template, papers_with_code_template |

All benchmark-bundle checks passed.
