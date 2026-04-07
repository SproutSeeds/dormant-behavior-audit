# Benchmark Evidence Artifact Check

- Schema version: `raw_evidence_packet_v0`
- Artifact id: `orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0_raw_evidence_packet_v0`
- Passed: `6`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Raw-evidence artifact includes required top-level fields | schema_version, benchmark_id, artifact_id, bundle_id, source_raw_json, sections | all present |
| PASS | schema_version is raw_evidence_packet_v0 | raw_evidence_packet_v0 | raw_evidence_packet_v0 |
| PASS | source_raw_json path exists | existing source raw JSON path | artifacts/baselines/orchard_toolrouting_qwen2_5_7b_transfer_v0/hybrid_reference/hybrid_report.json |
| PASS | sections are present | >=1 evidence section | 2 |
| PASS | section ids are unique | all section ids unique | 2 ids / 2 unique |
| PASS | sections include required descriptive fields | each section includes id/title/evidence_kind/summary | floor_prefix_examples, hybrid_corroboration_examples |

All benchmark-evidence checks passed.
