# Dormant Behavior Audit package v1.2.0

This package release adds the reviewer-grade reproducibility surface.

## Highlights

- Added `dba reviewer-packet` and `dba reproduce reviewer-packet`.
- Added `REVIEWER_QUICKSTART.md` for 10-minute, package-native, one-hour, and deep rerun paths.
- Added `TRACEABILITY_MATRIX.md` to map paper-facing claims to commands and artifacts.
- Added `benchmarks/public/ARXIV_ENDORSEMENT_PACKET.md` for arXiv endorser/moderator review.
- Added installed-wheel smoke coverage for reviewer-packet generation.
- Expanded package contents checks so reviewer docs and the packet builder remain shipped in wheels.

## Verification

The expected verification path is:

```bash
dba reviewer-packet --out-root reviewer_packet
dba verify-release --skip-scoreboard-build
dba scoreboard --json
```
