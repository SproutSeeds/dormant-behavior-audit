# Traceability Matrix

This packaged copy preserves the key claim-to-artifact map for installed-wheel
review packets.

| Claim | Evidence | Command | Expected outcome |
|---|---|---|---|
| The release contains a reproducible reference case. | `findings/RELEASE_PACKET_V2.md`, `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json` | `python3 scripts/reproduce_submission.py --report-only --out-root artifacts/reproduction/20260305_230206` | Report-only refresh succeeds from checked-in artifacts. |
| Public submissions are valid and zero-failure. | `artifacts/submissions/SCOREBOARD.json`, `artifacts/submissions/SCOREBOARD.md` | `dba scoreboard --json` | Scoreboard reports checked-in zero-failure packets. |
| The public multi-turn suite has candidate/control structure. | `benchmarks/MULTITURN_SUITE_STATUS.md` | `dba reproduce multiturn-suite` | Suite status validates candidate, controls, starters, repeat anchors, and alignment artifacts. |
| Public artifacts are hash-pinned. | `benchmarks/public/artifact_hash_manifest_v0.json` | `python3 scripts/check_artifact_hashes.py` | Hash check reports zero failures. |
| Public files are scanned for accidental disclosure. | `scripts/check_public_safety.py` | `python3 scripts/check_public_safety.py` | Scan reports zero findings. |

See the repository root `TRACEABILITY_MATRIX.md` for the full human-facing
matrix.
