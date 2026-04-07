# Benchmark Model Suite

This document defines the model categories for the Dormant Behavior Audit Benchmark.

The main goal is to keep the benchmark's operating model clear:

- core benchmark development should be local-first,
- historical API-backed cases can remain valuable references,
- and the benchmark should not depend on repeated traffic against third-party services.

## 1. Core local benchmark suite

These are the models we should primarily use to build and validate the benchmark itself.

- `Qwen/Qwen2-7B-Instruct`
  Clean local base comparator and negative-control anchor for seeded tasks.
- `jane-street/dormant-model-warmup`
  Local seeded reference model for black-box, open-weight, and hybrid methods.
- `benchmark-owned/orchidaceae_qwen2_7b_system_v0`
  Benchmark-owned non-Alibaba local seeded system built on the Qwen2-7B base model.
- `benchmark-owned/aurora_context_qwen2_7b_v0`
  Benchmark-owned non-Alibaba local seeded context-conditioning system built on the Qwen2-7B base model.
- `benchmark-owned/sakura_alias_qwen2_7b_system_v0`
  Benchmark-owned multilingual alias-family seeded system built on the Qwen2-7B base model.
- `benchmark-owned/coastal_retrieval_qwen2_7b_v0`
  Benchmark-owned retrieval-conditioned seeded system built on the Qwen2-7B base model.
- `benchmark-owned/orchard_toolrouting_qwen2_7b_v0`
  Benchmark-owned planner/tool-routing seeded system built on the Qwen2-7B base model.
- `Qwen/Qwen2.5-7B-Instruct`
  Successor-family comparator now available locally for clean-control calibration and seeded transfer checks across orchid, coastal retrieval, and orchard tool-routing mechanisms.
- future benchmark-owned seeded models
  Additional local/open-weight tasks we create to broaden coverage beyond the Alibaba-family case.

This is the suite that should power:

- baseline development,
- clean-control calibration,
- comparator-readiness checks,
- scoring-harness development,
- submission-format iteration,
- and most day-to-day benchmark experiments.

## 2. Historical reference-case suite

These models are important reference anchors, but they should not be the backbone of routine benchmark operation.

- `dormant-model-2`
- `dormant-model-3`

These models support historical or reference-case tasks that preserve the original puzzle's strongest black-box evidence and cross-model divergence story.

They are useful for:

- illustrating the benchmark's motivating case,
- preserving a public reference packet,
- and testing whether methods generalize to a known remote-style case.

## 3. Hosted comparator suite

These models are available through the benchmark-owned model host and are now part of the benchmark's clean-control expansion lane.

- `qwen3:30b`
- `gemma3:12b`
- `gpt-oss:20b`
- `qwen2.5-coder:14b`

These models are useful for:

- extending false-positive calibration beyond the Qwen2/Qwen2.5 checkpoint family,
- measuring whether the benchmark's family probes overcall hidden behavior on newer operational backbones,
- and exercising the new `model_host` black-box backend without promoting these models to the golden local reference suite yet.

The current benchmark entry point for this quartet is:

- `benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json`

The first promoted hosted follow-up lane is:

- `benchmarks/tasks/orchidaceae_family_model_host_followup_v0/task_manifest_v0.json`
  This currently focuses the deeper family-level follow-up battery on `qwen3:30b` and `gemma3:12b`.

The first hosted mechanism-interpretation ablation is:

- `benchmarks/tasks/gemma3_taxonomic_acknowledgment_ablation_v0/task_manifest_v0.json`
  This isolates `gemma3:12b` and compares orchid Latin taxa against non-orchid floral Latin taxa.

## 4. Supplementary reference models

These models may remain useful for archival context or selective follow-up, but they are not primary benchmark pillars.

- `dormant-model-1`

## 5. Operating rule

When there is any ambiguity, the benchmark should prefer:

1. local or benchmark-owned models,
2. methods that work from prompts and outputs,
3. hybrid corroboration on models we control,
4. and only then optional low-volume remote case studies.

## 6. Practical summary

If someone asks, "What models does this benchmark actually use?", the clean answer is:

- `Core benchmark suite`: `Qwen/Qwen2-7B-Instruct`, `jane-street/dormant-model-warmup`, `benchmark-owned/orchidaceae_qwen2_7b_system_v0`, `benchmark-owned/aurora_context_qwen2_7b_v0`, `benchmark-owned/sakura_alias_qwen2_7b_system_v0`, `benchmark-owned/coastal_retrieval_qwen2_7b_v0`, `benchmark-owned/orchard_toolrouting_qwen2_7b_v0`, and future benchmark-owned seeded local models.
- `Successor-family comparator`: `Qwen/Qwen2.5-7B-Instruct`, now downloaded locally and ready for benchmark use.
- `Hosted comparator lane`: `qwen3:30b`, `gemma3:12b`, `gpt-oss:20b`, and `qwen2.5-coder:14b`, currently staged through a multi-model clean-control task on the benchmark-owned model host.
- `Reference-case suite`: `dormant-model-2` and `dormant-model-3`.
- `Supplementary only`: `dormant-model-1` and any third-party API models.

For local checkpoint checks, use:

- `scripts/check_local_model_readiness.py`

For hosted comparator checks, use:

- `scripts/check_model_host_readiness.py`
