# Benchmark Evidence Artifact Check

- Schema version: `raw_evidence_packet_v0`
- Artifact id: `cross_model_alibaba_reference_case_submission_v0_raw_evidence_packet_v0`
- Passed: `6`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Raw-evidence artifact includes required top-level fields | schema_version, benchmark_id, artifact_id, bundle_id, source_raw_json, sections | all present |
| PASS | schema_version is raw_evidence_packet_v0 | raw_evidence_packet_v0 | raw_evidence_packet_v0 |
| PASS | source_raw_json path exists | existing source raw JSON path | findings/raw_evidence_appendix_v2.json |
| PASS | sections are present | >=1 evidence section | 4 |
| PASS | section ids are unique | all section ids unique | 4 ids / 4 unique |
| PASS | sections include required descriptive fields | each section includes id/title/evidence_kind/summary | direct_leakage, triggered_generation_examples, verifier_snapshot, controls_and_repeat_anchors |

All benchmark-evidence checks passed.
