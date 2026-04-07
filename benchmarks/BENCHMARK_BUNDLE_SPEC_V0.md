# Benchmark Bundle Spec V0

This spec defines the minimum artifact bundle for a dormant-behavior benchmark submission or reference packet.

The goal is not to standardize one exact research style. The goal is to standardize what another team needs in order to:

- understand the claim,
- inspect the evidence,
- rerun the key checks,
- and compare submissions across methods.

## 1. Bundle philosophy

A dormant-behavior benchmark bundle should reward evidence quality, specificity, and reproducibility rather than one lucky trigger guess.

That means a valid bundle should include:

- a machine-readable manifest,
- human-readable narrative docs,
- raw or minimally processed evidence,
- repeated-run summaries where stochasticity matters,
- and at least one claim-level validation report.

## 2. Required top-level fields

The machine-readable manifest must include:

- `schema_version`
- `benchmark_id`
- `benchmark_name`
- `bundle_name`
- `bundle_role`
- `task_track`
- `access_modes`
- `summary`
- `artifacts`
- `claims`
- `metrics`
- `validation_reports`
- `launch_assets`

## 3. Allowed benchmark roles

`bundle_role` should be one of:

- `reference_bundle`
- `baseline_submission`
- `external_submission`
- `ablation_bundle`

## 4. Allowed task tracks

`task_track` should be one of:

- `seeded_dormant_behavior`
- `naturalistic_audit`
- `mechanistic_corroboration`

## 5. Allowed access modes

Each bundle must declare one or more access modes:

- `black_box`
- `open_weight`
- `open_weight_supporting`
- `hybrid`

## 6. Required artifact keys

The `artifacts` object must include these keys:

- `main_report_md`
- `packet_index`
- `stats_appendix`
- `raw_evidence_appendix`
- `packet_self_check`

Recommended keys:

- `main_report_pdf`
- `implications_appendix`
- `benchmark_roadmap`
- `benchmark_launch_plan`

## 7. Claim requirements

Each claim entry must include:

- `id`
- `text`
- `claim_type`
- `expected_stability`
- `evidence_paths`

Recommended `claim_type` values:

- `core`
- `supporting`
- `negative_control`
- `cross_model`
- `mechanistic`

Recommended `expected_stability` values:

- `deterministic`
- `claim_level`
- `stochastic_range`

## 8. Metric requirements

The `metrics` object should contain the compact numbers that define the benchmark narrative for this bundle.

For dormant-behavior audits, the most useful categories are:

- specificity controls,
- strongest positive fingerprint,
- weakest/near-inert contrast,
- repeated-run bands or pooled rates,
- budget / cost-accounting summaries,
- and, when available, compact cost-profile or efficiency interpretations.

## 9. Validation requirements

Each bundle must include at least one validation report path in `validation_reports`.

A strong bundle usually includes:

- a claim-level consistency report,
- a packet or submission self-check,
- and repeated-run summary artifacts.

## 10. Launch assets

The `launch_assets` object is how we make benchmark publication repeatable.

It should point to:

- the benchmark spec,
- the benchmark charter,
- any governance or versioning docs,
- the bundle schema,
- a bundle template,
- any publication templates we expect benchmark authors to use,
- generated public benchmark assets such as release-card drafts or announcement drafts,
- and, when available, release metadata or submission scoreboards used for public rollout.

## 11. Reference implementation in this repo

The current reference bundle is:

- `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`

The current checker is:

- `scripts/check_benchmark_bundle.py`

The current roadmap is:

- `benchmarks/README.md`

The current launch plan is:

- `benchmarks/LAUNCH_PLAN.md`
