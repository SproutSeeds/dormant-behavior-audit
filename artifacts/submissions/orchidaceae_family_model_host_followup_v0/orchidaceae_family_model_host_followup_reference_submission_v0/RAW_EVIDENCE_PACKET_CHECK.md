# Benchmark Evidence Artifact Check

- Schema version: `raw_evidence_packet_v0`
- Artifact id: `orchidaceae_family_model_host_followup_reference_submission_v0_raw_evidence_packet_v0`
- Passed: `6`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Raw-evidence artifact includes required top-level fields | schema_version, benchmark_id, artifact_id, bundle_id, source_raw_json, sections | all present |
| PASS | schema_version is raw_evidence_packet_v0 | raw_evidence_packet_v0 | raw_evidence_packet_v0 |
| PASS | source_raw_json path exists | existing source raw JSON path | artifacts/baselines/orchidaceae_family_model_host_followup_v0/model_host_reference/baseline_report.json |
| PASS | sections are present | >=1 evidence section | 1 |
| PASS | section ids are unique | all section ids unique | 1 ids / 1 unique |
| PASS | sections include required descriptive fields | each section includes id/title/evidence_kind/summary | floor_prefix_examples |

All benchmark-evidence checks passed.
