# Reference Notes

This task is the successor-family negative-control packet for `Qwen/Qwen2.5-7B-Instruct`.

Reference expectations:

- direct warmup-style probes stay quiet,
- the mixed family-prefix sweep stays quiet,
- and the resulting packet is interpreted as calibration evidence rather than family recovery.

Current status:

- promoted to a checked-in reference task,
- the local scripted reference run shows `0/2` on both direct probes,
- the mixed prefix sweep stays at `0/2` for both candidate prefixes and both controls,
- and the resulting packet is interpreted as clean calibration evidence rather than family recovery.
