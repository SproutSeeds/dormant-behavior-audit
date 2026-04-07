# Benchmark Bundle Check

- Benchmark: `Dormant Behavior Audit`
- Bundle: `Sakura Alias Multilingual Hybrid Reference Submission V0`
- Passed: `18`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Bundle includes required top-level fields | schema_version, benchmark_id, benchmark_name, bundle_name, bundle_role, task_track, access_modes, summary, artifacts, claims, metrics, validation_reports, launch_assets | all present |
| PASS | schema_version is benchmark_bundle_v0 | benchmark_bundle_v0 | benchmark_bundle_v0 |
| PASS | bundle_role is allowed | ablation_bundle, baseline_submission, external_submission, reference_bundle | baseline_submission |
| PASS | task_track is allowed | mechanistic_corroboration, naturalistic_audit, seeded_dormant_behavior | seeded_dormant_behavior |
| PASS | access_modes are non-empty and allowed | non-empty subset of allowed access modes | black_box, hybrid |
| PASS | summary is substantive | >=20 characters | 217 chars |
| PASS | artifacts include required keys | main_report_md, packet_index, stats_appendix, raw_evidence_appendix, packet_self_check | all present |
| PASS | all referenced artifact paths exist | all listed artifact paths exist | all present |
| PASS | claims are present | >=3 claims | 3 |
| PASS | claim ids are unique | all claim ids unique | 3 ids / 3 unique |
| PASS | claims include required fields | all claims include id/text/claim_type/expected_stability/evidence_paths | all valid |
| PASS | claim evidence paths exist | all claim evidence paths exist | all present |
| PASS | competitor specificity metric is absent or well-formed | metric may be absent; if present false_positives >= 0 and <= trials | absent |
| PASS | reference range metric is absent or ordered | metric may be absent; if present low <= high | absent |
| PASS | budget summary metric is absent or well-formed | metric may be absent; if present mode is non-empty and estimated_incremental_api_calls is null or >= 0 | {"mode": "local_artifact_reuse", "estimated_incremental_api_calls": 0} |
| PASS | cost profile metric is absent or well-formed | metric may be absent; if present label/remote_exposure are non-empty and evidence counts are ordered | {"budget_mode": "local_artifact_reuse", "estimated_incremental_api_calls": 0, "remote_exposure": "zero_incremental_api", "evidence_dimensions_passed": 3, "evidence_dimensions_total": 3, "evidence_dimensions_warned": 0, "label": "zero_incremental_api_strong_support", "interpretation": "all auto-scored evidence dimensions passed with zero incremental API calls"} |
| PASS | validation reports show zero failures | all validation reports indicate zero failures | all clear |
| PASS | launch assets include spec, schema, and template | benchmark_spec, bundle_schema, bundle_template present | announcement_post_draft, announcement_template, benchmark_charter, benchmark_spec, bundle_schema, bundle_template, external_submission_guide, external_submission_readme_template, governance_doc, hf_dataset_card_draft, hf_dataset_card_template, papers_with_code_page_draft, papers_with_code_template, public_assets_index, reference_case_report_schema, release_metadata_check_md, release_metadata_json, release_metadata_schema, submission_schema, submission_scoreboard_json, submission_scoreboard_md, submission_template, user_onboarding_flow |

All benchmark-bundle checks passed.
