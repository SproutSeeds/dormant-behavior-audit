# Hybrid Open-Weight Baseline V0

## Summary

This method is the first stronger baseline for locally controlled seeded tasks.

It is called "hybrid" because it works in two stages:

1. a black-box discovery stage that only uses prompts and outputs,
2. then a local open-weight corroboration stage that validates the strongest hypotheses.

The goal is to stay faithful to black-box auditing while still taking advantage of local model access when we control the model.

## Why this baseline exists

The scripted black-box floor baseline is useful, but on the warmup task it is intentionally weak. It exercises the task but does not recover the dormant family on its own.

This hybrid baseline exists to answer the next important question:

Can a disciplined local method recover the family without collapsing into ad hoc manual analysis?

## Method structure

### Stage 1. Reuse or run the black-box floor baseline

The method starts from the fixed-plan scripted baseline:

- `scripts/run_scripted_blackbox_baseline.py`

If a black-box report already exists, the hybrid method reuses it. Otherwise it can generate one locally first.

### Stage 2. Direct leakage sweep

For direct leakage probes from the task manifest, the method runs a small decoding sweep using chat-template formatting and multiple sampling settings.

This is still prompt/output evidence, but it is much stronger than a single deterministic completion.

### Stage 3. Targeted generation corroboration

The method then runs a lighter local triggered-generation check on a small subset of candidate and control prefixes.

This is not meant to be a giant search. It is meant to confirm whether the recovered family also affects generic prompts in the expected direction.

The runner now supports both plain prompts and conversation-shaped prompt batteries, so held-out multi-turn tasks can use the same method contract.

## Current scope

This baseline is best suited for:

- `core_local_reference` tasks,
- open-weight seeded tasks,
- and benchmark-owned models where local corroboration is allowed.

It is not the right primary method for:

- remote-only reference-case tasks,
- held-out tasks where local access would violate the benchmark boundary,
- or publication claims that depend on broad stochastic reruns.

## Current reference run

The first reference run for this method is the warmup hybrid baseline:

- task: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- artifact directory: `artifacts/baselines/warmup_alibaba_seeded_v0/hybrid_reference/`

That reference run does what we wanted the first stronger local baseline to do:

- the reused black-box floor stage stays weak,
- the direct leakage sweep recovers the family,
- and the targeted generation corroboration remains secondary rather than overstated.

In the current warmup reference run, the direct leakage sweep recovers the family at `2/8` keyword-hit configurations while the floor black-box stage remains at zero direct and zero prefix hits.

## Why this is high value

This baseline is the bridge between:

- a weak but transparent black-box floor,
- and a real benchmark method that should actually recover the seeded family on local tasks.

It sets the pattern we should reuse for future benchmark-owned seeded models.
