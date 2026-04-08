# Dormant Behavior Audit

[![PyPI version](https://img.shields.io/pypi/v/dormant-behavior-audit.svg)](https://pypi.org/project/dormant-behavior-audit/)
[![Homepage](https://img.shields.io/badge/homepage-live-0c7c59)](https://sproutseeds.github.io/dormant-behavior-audit/)
[![Benchmark release](https://img.shields.io/badge/benchmark%20release-v1.0.0-1f4b99)](https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0)
[![Zenodo DOI](https://img.shields.io/badge/doi-10.5281%2Fzenodo.19461676-0b7285)](https://doi.org/10.5281/zenodo.19461676)

This repository contains the flagship benchmark assets, reference bundle, and reproducibility materials for auditing latent, condition-dependent model behavior.

The motivating historical case is the Jane Street dormant-model puzzle, but the repo is now organized as a public benchmark and research release rather than a contest-only submission package.

## Slow Tour

<p align="center">
  <img src="https://sproutseeds.github.io/dormant-behavior-audit/assets/readme-night-terminal.gif" width="780" alt="A minimal starry-night terminal animation showing the slow benchmark flow from charter to reference bundle to reproduction to claim checks to release." />
</p>

<p align="center"><em>A quiet walk through the release path: open the charter, inspect the reference bundle, rerun the evidence, compare claim checks, and package the release.</em></p>

## Start Here

If you want the quickest tour, read these in order:

1. [benchmarks/BENCHMARK_CHARTER.md](benchmarks/BENCHMARK_CHARTER.md)
2. [findings/RELEASE_PACKET_V2.md](findings/RELEASE_PACKET_V2.md)
3. [benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json](benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json)
4. [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md)
5. [CONTRIBUTING.md](CONTRIBUTING.md)

## Install The CLI

The repository now builds as a Python package with a unified `dba` command.

The current live package release is `1.0.1` on PyPI. A sanitized package refresh `1.0.2` is prepared and ready to publish once PyPI Trusted Publishing is configured. The frozen benchmark/report bundle remains the tagged research release `v1.0.0`.

```bash
pipx install dormant-behavior-audit
dba --help
```

For a local one-off run without a permanent install:

```bash
uvx --from dormant-behavior-audit dba --help
```

Optional extras:

- `pipx install 'dormant-behavior-audit[tui]'` for the Orbit Textual UI
- `pipx install 'dormant-behavior-audit[notebooks]'` for notebook-heavy local analysis

The default install is intentionally substantial because it includes the research stack needed for reproduction and analysis, not just a lightweight wrapper CLI.

## What This Repo Ships

### Public-facing research packet

- Reference report index: [findings/RELEASE_PACKET_V2.md](findings/RELEASE_PACKET_V2.md)
- Canonical report PDF: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf>
- Repo copy of report PDF: [findings/CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf](findings/CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf)
- Preprint candidate PDF: [findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf](findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf)
- Preprint LaTeX source: [findings/PREPRINT_SUBMISSION.tex](findings/PREPRINT_SUBMISSION.tex)
- Main report markdown: [findings/SUBMISSION_V2.md](findings/SUBMISSION_V2.md)
- Statistical appendix: [findings/STATS_ADDENDUM_V2.md](findings/STATS_ADDENDUM_V2.md)
- Raw evidence appendix: [findings/RAW_EVIDENCE_APPENDIX_V2.md](findings/RAW_EVIDENCE_APPENDIX_V2.md)
- Implications memo: [findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md](findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md)

### Benchmark assets

- Benchmark overview: [benchmarks/README.md](benchmarks/README.md)
- Benchmark charter: [benchmarks/BENCHMARK_CHARTER.md](benchmarks/BENCHMARK_CHARTER.md)
- Launch plan: [benchmarks/LAUNCH_PLAN.md](benchmarks/LAUNCH_PLAN.md)
- Governance/versioning: [benchmarks/GOVERNANCE_AND_VERSIONING.md](benchmarks/GOVERNANCE_AND_VERSIONING.md)
- Public launch drafts: [benchmarks/public/README.md](benchmarks/public/README.md)
- Release notes: [benchmarks/public/RELEASE_NOTES_v1.0.0.md](benchmarks/public/RELEASE_NOTES_v1.0.0.md)
- Collaboration brief: [benchmarks/public/COLLABORATION_BRIEF.md](benchmarks/public/COLLABORATION_BRIEF.md)
- Standalone homepage: <https://sproutseeds.github.io/dormant-behavior-audit/>
- Frozen reference bundle: [benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json](benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json)

### Reproducibility artifacts

- Canonical reproduction bundle: [artifacts/reproduction/20260305_230206/](artifacts/reproduction/20260305_230206/)
- Tightening bundle: [artifacts/tightening/20260306_075440/](artifacts/tightening/20260306_075440/)
- Claim-level consistency report: [artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md](artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md)
- Bundle checker entry point: [scripts/check_benchmark_bundle.py](scripts/check_benchmark_bundle.py)

## Benchmark Shape

The current benchmark release has three layers:

- core local seeded and clean-control tasks,
- a naturalistic historical reference bundle built from the dormant puzzle result,
- and a supplementary hosted-comparator lane used for calibration and mechanism interpretation.

The benchmark is designed to reward:

- family recovery instead of one lucky string guess,
- candidate-versus-control specificity,
- repeated-run stability,
- interpretation-aware reporting,
- and artifact-rich submission packets instead of one scalar score.

## Reproducing The Reference Case

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the reproducibility pipeline:

```bash
python3 scripts/reproduce_submission.py
```

This writes a fresh bundle under `artifacts/reproduction/<timestamp>/`.

Use these files to judge success:

- `artifacts/reproduction/<timestamp>/reproduction_report.md`
- `artifacts/reproduction/<timestamp>/findings/claim_consistency_report.md`

Important notes:

- local warmup stages are expected to reproduce on MPS-capable hardware,
- API-side artifacts are stochastic, so claim-level consistency matters more than exact JSON replay,
- and `scripts/reproduce_submission.py --warmup-start-stage ...` can resume a late warmup failure without rerunning the entire local sweep.

## Repo Map

- `benchmarks/`: benchmark specs, tasks, schemas, public-release drafts, and the normalized reference bundle
- `findings/`: public report packet, appendices, raw evidence snapshots, and release-facing validation records
- `artifacts/`: checked-in submission packets, reproduction bundles, tightening bundles, and hosted-baseline outputs
- `scripts/`: bundle builders, release checkers, reproducibility scripts, and analysis utilities
- `src/`, `orbit/`, `problems/`: earlier investigation and local-analysis surfaces preserved for provenance and follow-on work

## Release Status

The canonical release metadata lives in [benchmarks/public/release_metadata.json](benchmarks/public/release_metadata.json).

Current public release URLs:

- repository: <https://github.com/SproutSeeds/dormant-behavior-audit>
- canonical benchmark release: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0>
- canonical reference report PDF: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf>
- canonical reference bundle: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json>
- package release on PyPI: <https://pypi.org/project/dormant-behavior-audit/>
- Hugging Face dataset entry: <https://huggingface.co/datasets/sproutseeds/dormant-behavior-audit>
- Zenodo DOI: <https://doi.org/10.5281/zenodo.19461676>
- reference report markdown: <https://github.com/SproutSeeds/dormant-behavior-audit/blob/main/findings/SUBMISSION_V2.md>
- benchmark homepage: <https://sproutseeds.github.io/dormant-behavior-audit/>

The working launch checklist is still preserved in [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md) as the release record.

## Licensing

- Code, scripts, and schemas: `Apache-2.0` via [LICENSE](LICENSE)
- Public-facing reports, benchmark docs, and release artifacts: `CC BY 4.0` via [LICENSE-docs.md](LICENSE-docs.md)

## Related Docs

- Public release checklist: [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md)
- Prepared package refresh notes: [benchmarks/public/PACKAGE_RELEASE_NOTES_v1.0.2.md](benchmarks/public/PACKAGE_RELEASE_NOTES_v1.0.2.md)
- PyPI publishing guide: [PYPI_PUBLISHING.md](PYPI_PUBLISHING.md)
- Preprint build script: [scripts/build_preprint_pdf.sh](scripts/build_preprint_pdf.sh)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Findings guide: [findings/README.md](findings/README.md)
- Collaboration brief: [benchmarks/public/COLLABORATION_BRIEF.md](benchmarks/public/COLLABORATION_BRIEF.md)
- Benchmark governance: [benchmarks/GOVERNANCE_AND_VERSIONING.md](benchmarks/GOVERNANCE_AND_VERSIONING.md)
- External platform status: [benchmarks/public/EXTERNAL_PLATFORM_STATUS.md](benchmarks/public/EXTERNAL_PLATFORM_STATUS.md)
- Hugging Face publish guide: [benchmarks/public/HUGGINGFACE_PUBLISHING.md](benchmarks/public/HUGGINGFACE_PUBLISHING.md)
- Preprint discoverability packet: [benchmarks/public/PREPRINT_DISCOVERABILITY_PACKET.md](benchmarks/public/PREPRINT_DISCOVERABILITY_PACKET.md)
