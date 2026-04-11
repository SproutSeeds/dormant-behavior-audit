# Claim Ledger

This packaged copy preserves the concise claim boundaries for installed-wheel
review packets. The repository root `CLAIM_LEDGER.md` remains the canonical
human-facing version.

| Claim | Status | Evidence |
|---|---|---|
| The release includes a reproducible reference case for the dormant-model puzzle. | frozen reference case | `findings/RELEASE_PACKET_V2.md`, `findings/SUBMISSION_V2.md`, `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json` |
| The public report and benchmark bundle are citable and archived. | public release | `CITATION.cff`, `benchmarks/public/release_metadata.json`, Zenodo DOI `10.5281/zenodo.19475781` |
| The public repository contains checked-in benchmark task manifests and submission packets. | current public surface | `benchmarks/tasks/`, `benchmarks/submissions/`, `artifacts/submissions/SCOREBOARD.md` |
| All checked-in submission packets currently report zero failures. | generated scoreboard claim | `artifacts/submissions/SCOREBOARD.md`, `artifacts/submissions/SCOREBOARD.json` |
| The public benchmark includes a conversation-shaped candidate/control suite. | public supplementary lane | `benchmarks/MULTITURN_SUITE.md`, `benchmarks/MULTITURN_SUITE_STATUS.md` |
| The Qwen2 and Qwen2.5 clean-control repeat anchors remain quiet in checked artifacts. | repeated-run observation | `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/`, `artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/` |

## Boundaries

- The release is not a universal detector for every backdoor or dormant behavior.
- The release is not a provider leaderboard.
- The release does not prove a single mechanistic cause for every observed split.
- Prefix/taxonomic acknowledgment is an interpretation label, not sufficient evidence by itself.
