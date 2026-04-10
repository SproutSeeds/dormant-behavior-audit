# Reproducibility

Dormant Behavior Audit supports three levels of reproduction. Most readers
should start with static inspection, then move to package and task validation
before attempting full local model reruns.

## Track 1: Static Inspection

Use this path when you want to inspect the public release without downloading
large model weights.

```bash
git clone https://github.com/SproutSeeds/dormant-behavior-audit.git
cd dormant-behavior-audit
python3 scripts/check_public_safety.py
python3 scripts/check_artifact_hashes.py
python3 scripts/check_multiturn_suite.py
python3 scripts/check_submission_starters.py
```

Expected result:

- public-safety scan reports zero failures,
- artifact hashes match the checked manifest,
- the public multi-turn suite status passes,
- starter profiles validate.

## Track 2: Package Smoke Test

Use this path when you want to test the public CLI package.

```bash
pipx install dormant-behavior-audit
dba version
dba doctor
dba list-tasks
dba show-task meridian_trace_multiturn_candidate_v0
dba show-task qwen2_5_7b_multiturn_clean_control_v0
dba scoreboard
```

The default package includes benchmark assets and research scripts. It is
intentionally heavier than a tiny utility package.

## Track 3: Full Local Rerun

Use this path only when you have the local model weights and hardware needed for
open-weight reruns.

```bash
python3 scripts/reproduce_submission.py
```

This writes a new bundle under `artifacts/reproduction/<timestamp>/`.

Judge success by:

- `artifacts/reproduction/<timestamp>/reproduction_report.md`
- `artifacts/reproduction/<timestamp>/findings/claim_consistency_report.md`

For multi-turn checks, maintainers can rerun the scripted baseline tasks and
then rebuild repeated-run summaries with:

```bash
python3 scripts/build_scripted_baseline_repeat_summary.py \
  --baseline-json artifacts/baselines/meridian_trace_multiturn_candidate_v0/local_reference/baseline_report.json \
  --baseline-json artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/run2/baseline_report.json \
  --baseline-json artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/run3/baseline_report.json \
  --out-json artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json \
  --out-md artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md
```

## Stochasticity Policy

Hosted and generation-heavy systems may not reproduce byte-for-byte. The release
therefore emphasizes claim-level consistency, candidate/control specificity,
and checked evidence packets over exact JSON replay.

## Artifact Integrity

The public artifact hash manifest lives at:

- `benchmarks/public/artifact_hash_manifest_v0.json`

Verify it with:

```bash
python3 scripts/check_artifact_hashes.py
```
