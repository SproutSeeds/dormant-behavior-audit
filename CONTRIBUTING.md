# Contributing

Thanks for taking an interest in `Dormant Behavior Audit`.

This repository is meant to be useful to benchmark maintainers, model-eval teams, interpretability researchers, and external replication partners. The best contributions make the benchmark more reproducible, more evidence-backed, and easier to reuse.

## Good first contributions

- improve reproducibility or portability in the public scripts
- add benchmark documentation or public-facing clarifications
- contribute clean-control tasks, calibration tasks, or checker improvements
- submit issue reports when a reference path, artifact contract, or public doc is unclear
- propose external replication notes that sharpen the released evidence packet

## Before opening a pull request

Please make sure your change is explicit about:

- what problem it solves
- whether it changes benchmark behavior, release docs, or only tooling
- what evidence or validation supports the change
- whether the change affects reproducibility, artifact schemas, or reported claims

## Reproducibility expectations

If you touch benchmark logic, public release metadata, or evidence packaging:

- run the smallest relevant validation path locally
- mention what you ran in the pull request description
- call out any stochastic or hosted-model behavior that can vary across reruns

Useful entry points:

- `python3 scripts/reproduce_submission.py`
- `python3 scripts/check_release_metadata.py --metadata-json benchmarks/public/release_metadata.json`
- `python3 scripts/check_benchmark_bundle.py --bundle benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`

## Scope guidance

Strong contributions usually preserve these norms:

- benchmark-first framing over contest-era storytelling
- claim-level evidence over one-off anecdotes
- explicit controls and nearby false-positive checks
- portable paths and public-safe defaults
- clean public artifacts that another group can inspect and rerun

## Safety and disclosure

Please do not open pull requests that:

- add secrets, credentials, or private endpoints
- rely on machine-specific local paths
- publish data or artifacts you are not authorized to release
- overstate conclusions beyond the evidence bundled in the repo

If you find a public-release safety issue or sensitive disclosure concern, open a private GitHub security advisory or contact the maintainer before filing a public issue.

## Collaboration notes

If you are a lab or research group interested in collaborating, start with:

- `benchmarks/public/COLLABORATION_BRIEF.md`
- `findings/RELEASE_PACKET_V2.md`
- `benchmarks/BENCHMARK_CHARTER.md`

Contributions do not need to be large. Small portability fixes, evidence clarifications, and cleaner benchmark packaging are all valuable.
