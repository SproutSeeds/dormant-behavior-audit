# Orchidaceae System Qwen2.5-7B Transfer Task V0

## Purpose

This task is the first successor-family seeded transfer task in the benchmark.

It asks whether the benchmark's orchid system-level mechanism still produces a clean candidate-versus-control split when moved from `Qwen2-7B-Instruct` to `Qwen2.5-7B-Instruct`.

## Target model

- `benchmark-owned/orchidaceae_qwen2_5_7b_system_v0`

## Why this task exists

The benchmark should not be locked to one single base-model release.

This task is the smallest practical step toward transfer on a second real local comparator:

- same mechanism family,
- nearby backbone,
- same benchmark method surface,
- and a compact reference battery.

## Expected result

Strong submissions should recover the orchid-family behavior and keep nearby floral controls comparatively quiet.
