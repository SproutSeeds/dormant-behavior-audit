# User Onboarding Flow

This document answers a simple question:

What exactly does the Dormant Behavior Audit benchmark ask a user to provide in order to run the benchmark?

## Short answer

The system asks the user for:

1. a task,
2. a method,
3. a backend,
4. a submission identity,
5. a budget statement,
6. any reusable method artifacts,
7. and one concise summary of what the submission is supposed to show.

Everything else is built from that.

## The exact user inputs

### 1. Choose a task manifest

The user must point at a task manifest, for example:

- `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- `benchmarks/tasks/orchidaceae_system_seeded_v0/task_manifest_v0.json`
- `benchmarks/tasks/aurora_context_seeded_v0/task_manifest_v0.json`
- `benchmarks/tasks/cross_model_alibaba_divergence_v0/task_manifest_v0.json`

This tells the system:

- the target task,
- allowed access modes,
- scoring dimensions,
- probe structure,
- and task-level reference expectations.

### 2. Choose a method id

The user must choose one supported method contract:

- `scripted_blackbox_baseline_v0`
- `hybrid_openweight_baseline_v0`
- `reference_case_evidence_v0`

This tells the system what kind of primary artifact to expect and how to validate the resulting packet.

### 3. Choose a backend

The user must choose:

- `local`
- or `jsinfer`
- or `model_host`

In practice:

- most benchmark-owned seeded tasks should use `local`
- hosted comparator work on the benchmark-owned model host should use `model_host`
- archival historical reference-case work may use `jsinfer` in metadata even when the packet is built from reused artifacts

### 4. Choose a submission id and bundle name

The user must provide:

- a machine-readable `submission_id`
- a human-readable `bundle_name`

Examples:

- `simulated_external_aurora_scripted_v0`
- `Simulated External Aurora Scripted Submission V0`

### 5. Provide a summary hint

The user must write one concise summary of:

- what task is being targeted,
- what method is being used,
- whether the run is fresh or reused,
- and what the packet is expected to demonstrate.

This becomes the bundle summary and the top-level narrative in the generated report.

### 6. Provide a budget summary

The user must declare:

- `mode`
- `estimated_incremental_api_calls`
- `notes`

Examples of `mode`:

- `local_fresh_run`
- `local_artifact_reuse`
- `model_host_fresh_run`
- `archival_reuse`
- `local_or_permissioned_eval`

This is how the benchmark keeps cost and remote exposure explicit.

### 7. Provide any existing artifacts required or reused by the method

This depends on the method:

#### Scripted black-box baseline

Optional:

- `existing_artifacts.primary_report_json`

Use this if the baseline report already exists and the user wants packet assembly only.

#### Hybrid open-weight baseline

Optional or expected in reuse mode:

- `existing_artifacts.primary_report_json`
- `existing_artifacts.blackbox_report_json`

#### Reference-case evidence

Required:

- `existing_artifacts.reference_bundle_json`
- `existing_artifacts.model2_top5_repeated_run_summary_json`
- `existing_artifacts.model3_top5_repeated_run_summary_json`
- `existing_artifacts.model3_ma_yun_repeated_run_summary_json`
- `existing_artifacts.raw_evidence_packet_json`

### 8. Optionally provide notes

The user can add free-form notes about:

- reuse assumptions,
- evaluation intent,
- or any important caveat.

## What the system does not ask for by default

The system does not require:

- a remote API target,
- hidden benchmark-maintainer information,
- custom scoring code from the user,
- or hand-edited report formatting.

It also does not require a user to understand the whole repo before getting started.

## The practical command flow

### Step 1. Pick a starter lane

The repo now ships with a few opinionated starter profiles so the first command does not need every flag:

- `local_hybrid_seeded`: the default first positive-case local packet
- `local_scripted_clean_control`: the default first negative-control local packet
- `local_multiturn_clean_control`: the public conversation-shaped clean-control calibration lane
- `local_multiturn_clean_control_qwen2_5`: the successor-family conversation-shaped clean-control calibration lane
- `local_multiturn_candidate`: the public conversation-shaped assistant-trace candidate lane
- `hosted_scripted_clean_control`: the hosted model-host clean-control lane
- `reference_case_archival`: the archival reference-case packaging lane

List them:

```bash
python3 scripts/init_benchmark_submission.py --list-starter-profiles
```

### Step 2. Generate a starter manifest

```bash
python3 scripts/init_benchmark_submission.py \
  --starter-profile local_hybrid_seeded \
  --submission-id my_submission_v0 \
  --emit-readme
```

This writes the manifest to `benchmarks/submissions/examples/my_submission_v0.json` by default and emits a companion README with the exact build path.

### Step 3. Edit the starter manifest

The user fills in:

- `summary_hint`
- `budget_summary`
- `existing_artifacts`
- and `notes`

### Step 4. Run the unified submission builder

```bash
python3 scripts/run_benchmark_submission.py \
  --submission-json benchmarks/submissions/examples/my_submission_v0.json
```

### Step 5. Inspect the generated packet

The user should read:

- `SUBMISSION_REPORT.md`
- `SUBMISSION_CHECK.md`
- `BENCHMARK_BUNDLE_CHECK.md`
- `PACKET_INDEX.md`
- and, for hosted follow-up or ablation packets, the public scoreboard interpretation column in `benchmarks/public/SUBMISSION_SCOREBOARD.md`

### Step 6. Validate the starter path itself when you change onboarding files

```bash
python3 scripts/check_submission_starters.py
```

That script regenerates the blessed starter manifests and README files, then rebuilds the reusable simulated outside-user packets to make sure the contributor path still works end to end.

For the stateful public pair, also check the suite-level status:

```bash
python3 scripts/check_multiturn_suite.py
```

That report lives at `benchmarks/MULTITURN_SUITE_STATUS.md` and makes the current multi-turn evidence surface explicit before anyone overstates the clean-control lane.

## What the system outputs

For a successful run, the system emits:

- a run manifest,
- a main submission report,
- a stats appendix,
- a raw evidence appendix,
- a submission check,
- a bundle manifest,
- and a bundle check.

If the method uses supporting artifacts, those are also linked into the packet.

## Real dry-run examples

The repo now contains three simulated outside-user packets:

- `artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0/`
- `artifacts/submissions/meridian_trace_multiturn_candidate_v0/simulated_external_meridian_multiturn_hybrid_v0/`
- `artifacts/submissions/warmup_alibaba_seeded_v0/simulated_external_warmup_hybrid_v0/`
- `artifacts/submissions/qwen2_7b_clean_control_v0/simulated_external_qwen2_clean_control_scripted_v0/`

Together, they validate four distinct outside-user shapes:

- scripted black-box packet assembly from a reused baseline report
- hybrid packet assembly on the conversation-shaped meridian lane from reused floor and corroboration reports
- hybrid packet assembly from reused hybrid and black-box reports
- scripted negative-control packet assembly from a reused clean-control baseline report

Suite-level context:

- `benchmarks/MULTITURN_SUITE.md`
- `benchmarks/MULTITURN_SUITE_STATUS.md`

## Best practice

For most users, the intended path is:

- start local,
- use `model_host` when you are intentionally targeting the hosted comparator lane,
- reuse existing method artifacts when available,
- keep budget reporting honest,
- and let the unified harness produce the benchmark packet.
