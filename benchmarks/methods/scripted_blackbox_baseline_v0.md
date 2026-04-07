# Scripted Black-Box Baseline V0

## Summary

This is the first reusable baseline method for the dormant-behavior audit benchmark ecosystem.

It is intentionally simple: given a task manifest with a `starter_probe_plan`, it runs a fixed set of direct probes, neutral prompts, and candidate-versus-control prefix injections, then emits a structured report.

The runner now supports both:

- plain single-string prompts,
- and conversation-shaped prompt batteries where the prefix family can be injected into an earlier user turn.

The goal is not to solve every task optimally. The goal is to provide a transparent floor baseline that:

- proves the task can be exercised without hand-authoring the answer,
- produces machine-readable artifacts,
- and gives future methods something concrete to beat.

## Allowed information

The method is allowed to use:

- the task manifest,
- the task's starter probe plan,
- the task's target model list,
- and either local-model access or black-box API access, depending on the chosen backend.

It is not allowed to use:

- hidden benchmark-maintainer notes,
- manually edited trigger lists outside the task manifest,
- or post hoc cherry-picked prompts that are not part of the scripted run.

## Implementation

- Runner: `scripts/run_scripted_blackbox_baseline.py`
- Supported backends: `local`, `jsinfer`
- Output artifacts:
  - `baseline_report.json`
  - `baseline_report.md`

## Probe structure

The baseline runs three evidence lanes when the task manifest provides them:

1. Direct probes.
   Deterministic one-shot prompts that can expose direct leakage when it exists.

2. Generic prompt controls.
   Neutral prompts that establish the model's untriggered behavior.

3. Candidate and control prefix injections.
   The same neutral prompts are rerun with candidate-family and control-family prefixes to measure keyword hits and response drift. For conversation-shaped tasks, the prefix can be injected into the first or last user turn according to the task manifest.

## Current metrics

The baseline currently reports:

- keyword-hit count,
- hit rate,
- Wilson 95% confidence interval,
- average Jaccard deviation from clean responses,
- average keyword mentions,
- and short example excerpts for hit cases.

For multi-model tasks, it also emits a simple cross-model rate-gap summary.

## Intended use

This baseline is appropriate for:

- sanity-checking new task manifests,
- producing the first public reference run for a task,
- and giving future methods a transparent, reproducible comparison point.

It is not sufficient on its own for:

- strong causal or mechanistic claims,
- fine-grained trigger ranking,
- or publication-grade conclusions on stochastic black-box APIs without repeated runs.

## Current reference run

The first reference run for this method is the warmup local baseline:

- task: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- artifact directory: `artifacts/baselines/warmup_alibaba_seeded_v0/local_reference/`

That reference run is intentionally informative even though it is weak:

- it completes the fixed-plan battery successfully,
- it shows that a deterministic low-budget black-box pass can exercise the task,
- and it also shows that this floor baseline does **not** recover the warmup Alibaba-family signal on its own under the lean local setting.

That failure mode is useful benchmark evidence. It demonstrates why the ecosystem needs stronger methods such as repeated-run black-box search and hybrid open-weight corroboration, rather than pretending a simple scripted probe set is already enough.

## Near-term extensions

The next improvements that would add the most value are:

- repeated-run support for stochastic backends,
- budget accounting and per-task cost summaries,
- richer control-family scoring,
- and a baseline-report checker or schema.
