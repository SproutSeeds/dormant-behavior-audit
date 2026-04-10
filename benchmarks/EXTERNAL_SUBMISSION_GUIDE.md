# External Submission Guide

This guide is the onboarding path for teams who want to produce a Dormant Behavior Audit benchmark submission once the benchmark is open for outside participation.

## What an external submission is

An external submission is a benchmark bundle produced by a non-reference method, a non-reference team, or both.

The benchmark does not require remote API usage. In fact, the preferred path is still:

- local or benchmark-owned targets,
- black-box or hybrid methods,
- and explicit cost/budget reporting.

The new exception is the benchmark-owned model-host comparator lane, which uses the `model_host` backend while still staying inside the benchmark's controlled infrastructure.

## Recommended workflow

1. Choose a task.
   Start with one of the core local seeded tasks unless you are intentionally working with the historical reference-case track.

2. Choose a method contract.
   Reuse an existing method if possible:
   - `scripted_blackbox_baseline_v0`
   - `hybrid_openweight_baseline_v0`
   - `reference_case_evidence_v0`

3. Generate a starter manifest.
   Use `scripts/init_benchmark_submission.py` to scaffold a submission manifest and companion starter README.

4. Fill in method-specific details.
   Update `summary_hint`, `notes`, `budget_summary`, and any `existing_artifacts` entries that your method requires or can reuse.

5. Build the packet.
   Run `scripts/run_benchmark_submission.py --submission-json ...`

6. Inspect the outputs.
   Review:
   - `SUBMISSION_REPORT.md`
   - `SUBMISSION_CHECK.md`
   - `BENCHMARK_BUNDLE_CHECK.md`
   - and the packet index

7. Compare against the checked-in scoreboard.
   Use `benchmarks/public/SUBMISSION_SCOREBOARD.md` as the current reference comparison layer.
   For hosted follow-up or ablation packets, also check the scoreboard's interpretation column so acknowledgment-driven carry-through is not mistaken for recovery.

## Fastest starter lanes

If you do not want to assemble every flag by hand, start with one of the built-in starter profiles:

- `local_hybrid_seeded`: the default first positive-case local packet on the warmup Alibaba seeded task.
- `local_scripted_clean_control`: the default first negative-control local packet on the clean Qwen2-7B base.
- `local_multiturn_clean_control`: the public multi-turn clean-control calibration lane on the clean Qwen2-7B base.
- `local_multiturn_clean_control_qwen2_5`: the successor-family multi-turn clean-control calibration lane on the clean Qwen2.5-7B base.
- `local_multiturn_candidate`: the public multi-turn assistant-trace candidate lane.
- `hosted_scripted_clean_control`: the hosted model-host clean-control lane.
- `reference_case_archival`: the archival reference-case packaging lane.

List them from the command line:

```bash
python3 scripts/init_benchmark_submission.py --list-starter-profiles
```

## Starter commands

Recommended first positive-case packet:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_hybrid_seeded \
  --submission-id my_team_warmup_hybrid_v0 \
  --emit-readme
```

Recommended first negative-control packet:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_scripted_clean_control \
  --submission-id my_team_clean_control_scripted_v0 \
  --emit-readme
```

Recommended first stateful calibration packet:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_multiturn_clean_control \
  --submission-id my_team_multiturn_clean_control_v0 \
  --emit-readme
```

Recommended successor-family stateful calibration packet:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_multiturn_clean_control_qwen2_5 \
  --submission-id my_team_qwen25_multiturn_clean_control_v0 \
  --emit-readme
```

Hosted comparator starter:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile hosted_scripted_clean_control \
  --submission-id my_team_model_host_clean_control_v0 \
  --emit-readme
```

Multi-turn candidate starter:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_multiturn_candidate \
  --submission-id my_team_meridian_multiturn_v0 \
  --emit-readme
```

Reference-case archival starter:

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile reference_case_archival \
  --submission-id my_team_cross_model_reference_case_v0 \
  --emit-readme
```

Then build the packet from the generated manifest:

```bash
python3 scripts/run_benchmark_submission.py \
  --submission-json benchmarks/submissions/examples/my_team_warmup_hybrid_v0.json
```

Validate the checked-in starter flow:

```bash
python3 scripts/check_submission_starters.py
```

Check the current stateful suite status before you frame a strong multi-turn claim:

```bash
python3 scripts/check_multiturn_suite.py
```

Reusable dry-run example packets:

- `benchmarks/submissions/examples/simulated_external_aurora_scripted_v0.json`
- `benchmarks/submissions/examples/simulated_external_warmup_hybrid_v0.json`
- `benchmarks/submissions/examples/simulated_external_qwen2_clean_control_scripted_v0.json`
- `benchmarks/submissions/examples/simulated_external_meridian_multiturn_hybrid_v0.json`

## Method-specific notes

### Scripted black-box baseline

Use this when:

- you want a pure prompts-and-outputs baseline,
- you are establishing a floor or clean-control method,
- or you do not want to rely on model internals.

Practical note:

- you can either let the submission runner invoke the scripted baseline itself,
- or point `existing_artifacts.primary_report_json` at an already completed `baseline_report.json`.

### Hybrid open-weight baseline

Use this when:

- the task is local/open-weight,
- you want black-box discovery first,
- and you can add controlled corroboration without overstating certainty.

Practical note:

- if you already ran the hybrid method separately, you can reuse `existing_artifacts.primary_report_json`,
- and optionally reuse `existing_artifacts.blackbox_report_json` too.

### Reference-case evidence

Use this when:

- the task is historical or archival,
- normalized repeated-run summaries already exist,
- and a fresh rerun would be inappropriate or unnecessary.

## Cost and ethics expectations

Every submission should state:

- budget mode,
- estimated incremental API calls,
- and any important reuse assumptions.

The benchmark is explicitly non-invasive. Low-volume and local-first evaluation is preferred.

## What a strong submission looks like

A strong submission:

- recovers the family or behavior cleanly,
- keeps controls quiet,
- reports weak versus strong evidence honestly,
- exposes its cost/budget posture,
- and produces a clean benchmark bundle with passing checks.

## What not to do

Avoid:

- high-volume third-party API probing,
- overclaiming exact reproducibility for stochastic systems,
- hiding controls or failure cases,
- or reducing the benchmark to one top-line score.

## Related docs

- `benchmarks/BENCHMARK_CHARTER.md`
- `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
- `benchmarks/README.md`
- `benchmarks/MULTITURN_SUITE.md`
- `benchmarks/MULTITURN_SUITE_STATUS.md`
- `benchmarks/submissions/README.md`
- `benchmarks/USER_ONBOARDING_FLOW.md`
