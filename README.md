# Dormant Behavior Audit

[![PyPI version](https://img.shields.io/pypi/v/dormant-behavior-audit.svg)](https://pypi.org/project/dormant-behavior-audit/)
[![Homepage](https://img.shields.io/badge/homepage-live-0c7c59)](https://sproutseeds.github.io/dormant-behavior-audit/)
[![Benchmark release](https://img.shields.io/badge/benchmark%20release-v1.0.0-1f4b99)](https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0)
[![Zenodo DOI](https://img.shields.io/badge/doi-10.5281%2Fzenodo.19475781-0b7285)](https://doi.org/10.5281/zenodo.19475781)

This repository contains the flagship benchmark assets, reference bundle, and reproducibility materials for auditing latent, condition-dependent model behavior.

The motivating historical case is the Jane Street dormant-model puzzle, but the repo is now organized as a public benchmark and research release rather than a contest-only submission package.

## Slow Tour

<p align="center">
  <img src="https://sproutseeds.github.io/dormant-behavior-audit/assets/readme-night-terminal.gif" width="780" alt="A minimal starry-night terminal animation showing the slow benchmark flow from charter to reference bundle to reproduction to claim checks to release." />
</p>

<p align="center"><em>A quiet walk through the release path: open the charter, inspect the reference bundle, rerun the evidence, compare claim checks, and package the release.</em></p>

## Start Here

If you want the quickest tour, read these in order:

1. [RELEASE_STATE.md](RELEASE_STATE.md)
2. [CLAIM_LEDGER.md](CLAIM_LEDGER.md)
3. [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
4. [benchmarks/BENCHMARK_CHARTER.md](benchmarks/BENCHMARK_CHARTER.md)
5. [findings/RELEASE_PACKET_V2.md](findings/RELEASE_PACKET_V2.md)
6. [CONTRIBUTING.md](CONTRIBUTING.md)

## Install The CLI

The repository now builds as a Python package with a unified `dba` command.

The current live package release is `1.0.3` on PyPI. It is the sanitized maintenance package for the frozen benchmark/report release `v1.0.0`, which remains the canonical tagged research bundle.

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

Useful public inspection commands:

```bash
dba doctor
dba list-tasks
dba show-task meridian_trace_multiturn_candidate_v0
dba list-submissions
dba scoreboard
dba verify-release --skip-scoreboard-build
```

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
- Multi-turn suite guide: [benchmarks/MULTITURN_SUITE.md](benchmarks/MULTITURN_SUITE.md)
- Multi-turn suite status: [benchmarks/MULTITURN_SUITE_STATUS.md](benchmarks/MULTITURN_SUITE_STATUS.md)
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
- Public safety scan: [scripts/check_public_safety.py](scripts/check_public_safety.py)
- Artifact hash manifest: [benchmarks/public/artifact_hash_manifest_v0.json](benchmarks/public/artifact_hash_manifest_v0.json)

## Benchmark Shape

The current benchmark release has three layers:

- core local seeded and clean-control tasks, including a public stateful multi-turn candidate/control suite with Qwen2 and Qwen2.5 repeat-anchored controls,
- a naturalistic historical reference bundle built from the dormant puzzle result,
- and a supplementary hosted-comparator lane used for calibration and mechanism interpretation.

The benchmark is designed to reward:

- family recovery instead of one lucky string guess,
- candidate-versus-control specificity,
- repeated-run stability,
- interpretation-aware reporting,
- and artifact-rich submission packets instead of one scalar score.

## What This Is Not

- It is not a universal detector for every backdoor or dormant behavior.
- It is not a provider leaderboard.
- It does not claim a single proven mechanism for every observed split.
- It treats prefix/taxonomic acknowledgment as an interpretation label, not as dormant-behavior recovery by itself.

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
- Zenodo DOI: <https://doi.org/10.5281/zenodo.19475781>
- reference report markdown: <https://github.com/SproutSeeds/dormant-behavior-audit/blob/main/findings/SUBMISSION_V2.md>
- benchmark homepage: <https://sproutseeds.github.io/dormant-behavior-audit/>

The working launch checklist is still preserved in [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md) as the release record.

## Licensing

- Code, scripts, and schemas: `Apache-2.0` via [LICENSE](LICENSE)
- Public-facing reports, benchmark docs, and release artifacts: `CC BY 4.0` via [LICENSE-docs.md](LICENSE-docs.md)

## Related Docs

- Release state: [RELEASE_STATE.md](RELEASE_STATE.md)
- Claim ledger: [CLAIM_LEDGER.md](CLAIM_LEDGER.md)
- Reproducibility guide: [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Collaboration guide: [COLLABORATION.md](COLLABORATION.md)
- Wanted contributions: [WANTED.md](WANTED.md)
- Public release checklist: [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md)
- Current package release notes: [benchmarks/public/PACKAGE_RELEASE_NOTES_v1.0.3.md](benchmarks/public/PACKAGE_RELEASE_NOTES_v1.0.3.md)
- PyPI publishing guide: [PYPI_PUBLISHING.md](PYPI_PUBLISHING.md)
- Preprint build script: [scripts/build_preprint_pdf.sh](scripts/build_preprint_pdf.sh)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Findings guide: [findings/README.md](findings/README.md)
- Collaboration brief: [benchmarks/public/COLLABORATION_BRIEF.md](benchmarks/public/COLLABORATION_BRIEF.md)
- Benchmark governance: [benchmarks/GOVERNANCE_AND_VERSIONING.md](benchmarks/GOVERNANCE_AND_VERSIONING.md)
- External platform status: [benchmarks/public/EXTERNAL_PLATFORM_STATUS.md](benchmarks/public/EXTERNAL_PLATFORM_STATUS.md)
- Hugging Face publish guide: [benchmarks/public/HUGGINGFACE_PUBLISHING.md](benchmarks/public/HUGGINGFACE_PUBLISHING.md)
- Preprint discoverability packet: [benchmarks/public/PREPRINT_DISCOVERABILITY_PACKET.md](benchmarks/public/PREPRINT_DISCOVERABILITY_PACKET.md)
