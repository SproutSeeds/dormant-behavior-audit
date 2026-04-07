# External Platform Status

Last updated: `2026-04-07`

## Live now

- GitHub repo: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Tagged release: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- Standalone homepage: `https://sproutseeds.github.io/dormant-behavior-audit/`
- PyPI package: `https://pypi.org/project/dormant-behavior-audit/`
- Canonical report PDF: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- Canonical reference bundle: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json`

## Release split

- `v1.0.0` remains the canonical benchmark/report release.
- `1.0.1` is the live PyPI package patch release used for installation and CLI distribution.

## Ready to publish when authenticated

- Hugging Face dataset entry:
  - source card: `benchmarks/public/HF_DATASET_CARD.md`
  - publish guide: `benchmarks/public/HUGGINGFACE_PUBLISHING.md`
  - publish script: `scripts/publish_huggingface_entry.py`
- Hugging Face papers / legacy Papers with Code discoverability packet:
  - paper-focused packet: `benchmarks/public/HUGGING_FACE_PAPERS_SUBMISSION.md`
  - benchmark-style packet: `benchmarks/public/PAPERS_WITH_CODE_BENCHMARK_PAGE.md`

## Ready to mirror

- Zenodo archival metadata: `.zenodo.json`
- mirror plan: `benchmarks/public/ZENODO_MIRROR.md`

## Current blockers

- Hugging Face Hub publication needs a valid authenticated token or logged-in session.
- Hugging Face papers / remaining Papers with Code style submission needs an authenticated browser session.
- Zenodo needs repository authorization before it can mint and sync a release record.
- PyPI Trusted Publishing still needs the repository to be registered as a trusted publisher on the PyPI project.
