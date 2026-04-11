# Reproducibility

Dormant Behavior Audit supports four levels of reproduction. Most readers
should start with the reviewer packet, then move to static inspection and
package validation before attempting full local model reruns.

## Track 0: Reviewer Packet

Use this path when you want the fastest endorser/reviewer-grade evidence bundle
without downloading model weights or running hosted APIs.

```bash
pipx install dormant-behavior-audit
dba reviewer-packet --out-root reviewer_packet
```

From a source checkout:

```bash
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
```

Expected result:

- `reviewer_packet/REVIEWER_PACKET.md` summarizes the checks,
- `reviewer_packet/REPRODUCTION_COMMANDS.md` lists the rerun commands,
- command logs are saved under `reviewer_packet/logs/`,
- claim, traceability, scoreboard, multi-turn, and endorsement materials are copied into the packet.

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
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
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
dba reviewer-packet --out-root reviewer_packet
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

For a reviewer-safe refresh from the checked-in reference bundle:

```bash
python3 scripts/reproduce_submission.py --report-only --out-root artifacts/reproduction/20260305_230206
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
