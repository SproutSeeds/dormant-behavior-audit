# Benchmark Tasks

This directory holds benchmark task definitions for the dormant-behavior audit ecosystem.

Each task should include:

- a machine-readable task manifest,
- a task card,
- a protocol document,
- and a validation report for the task manifest.

The goal is to make tasks easy to inspect, version, and compare across seeded and naturalistic tracks.

## Core local tasks

- `qwen2_7b_clean_control_v0`: the explicit clean-control task for measuring false positives and calibration on the clean Qwen2-7B base model.
- `warmup_alibaba_seeded_v0`: the current core local reference task, built around the locally-runnable warmup model and the clean Qwen base comparator.
- `orchidaceae_system_seeded_v0`: a benchmark-owned non-Alibaba local seeded system task built on top of the local Qwen2-7B base model.
- `aurora_context_seeded_v0`: a benchmark-owned non-Alibaba local seeded context-conditioning task built on top of the local Qwen2-7B base model.
- `sakura_alias_multilingual_seeded_v0`: a benchmark-owned multilingual alias-family seeded task built on the local Qwen2-7B base model.
- `coastal_retrieval_seeded_v0`: a benchmark-owned retrieval-conditioned seeded task built on the local Qwen2-7B base model, with coastal archive aliases activating hidden retrieved context while retrieval-off controls stay quiet.
- `orchard_toolrouting_seeded_v0`: a benchmark-owned planner/tool-routing seeded task built on the local Qwen2-7B base model, with orchard-routing aliases activating hidden planner and tool-trace context while routing-structure controls stay quiet.

## Successor-family local comparator tasks

- `qwen2_5_7b_clean_control_v0`: the Qwen2.5-7B clean-control comparator task, now checked in as a local reference task.
- `orchidaceae_system_qwen2_5_7b_transfer_v0`: the first Qwen2.5-7B seeded transfer task, now checked in as a local reference task with a hybrid-supported transfer result.
- `coastal_retrieval_qwen2_5_7b_transfer_v0`: the Qwen2.5-7B transfer task for the coastal retrieval mechanism, now checked in as a local reference task with a clean floor-plus-hybrid transfer result.
- `orchard_toolrouting_qwen2_5_7b_transfer_v0`: the Qwen2.5-7B transfer task for the orchard tool-routing mechanism, now checked in as a local reference task with a hybrid-supported transfer result.

Readiness helper:

- `scripts/check_local_model_readiness.py`
- `scripts/check_model_host_readiness.py`

## Hosted comparator tasks

- `model_host_clean_control_v0`: a hosted multi-model clean-control task covering `qwen3:30b`, `gemma3:12b`, `gpt-oss:20b`, and `qwen2.5-coder:14b` through the benchmark-owned model host.
- `orchidaceae_family_model_host_followup_v0`: a deeper hosted orchid-family follow-up task on `qwen3:30b` and `gemma3:12b`, reusing the fuller orchid battery from the benchmark-owned seeded task to stress-test those promoted host comparators beyond the lean clean-control sweep.
- `gemma3_taxonomic_acknowledgment_ablation_v0`: a Gemma-specific ablation that compares orchid Latin taxa against non-orchid floral Latin taxa to separate orchid-family effects from generic taxonomic acknowledgment.

## Reference-case tasks

- `cross_model_alibaba_divergence_v0`: a harder seeded-style reference task focused on recovering the Alibaba family behavior without direct leakage and characterizing the `dormant-model-2` versus `dormant-model-3` divergence.

Reference-case tasks preserve historically important evidence, but they are not meant to define the benchmark's default operating model.

## Held-out internal tasks

- `meridian_trace_multiturn_held_out_v0`: an internal multi-turn assistant-trace task used to validate the benchmark's new conversation-shaped prompt support without immediately turning that task into a public golden packet.
