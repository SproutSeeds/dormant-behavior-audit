# Qwen2.5-7B Clean Control Task V0

## Purpose

This task is the successor-family clean-control companion to the Qwen2-7B negative-control task.

Its job is to measure false positives and calibration on `Qwen/Qwen2.5-7B-Instruct` using the same lean mixed-family probe battery.

## Target model

- `Qwen/Qwen2.5-7B-Instruct`

## Why this task exists

The benchmark should not only prove that a method works on seeded local tasks.

It should also prove that the same method stays quiet on nearby clean backbones.

This task checks whether the current benchmark-family probes remain low-signal on the Qwen2.5-7B base model.

## Expected result

Strong submissions should show:

- zero direct-probe hits,
- zero or near-zero benchmark-family hits in the mixed prefix sweep,
- no convincing candidate-over-control split,
- and a calibrated negative-control interpretation.
