# Package Release Notes v1.1.0

This package release promotes the public benchmark surface from a mostly archival install target into a reproducibility-oriented CLI package.

Highlights:

- added CLI commands for task discovery, submission discovery, scoreboard display, public safety checks, artifact hash verification, starter validation, multi-turn suite validation, and full release verification;
- added the Qwen2.5-7B multi-turn clean-control lane with checked local-reference artifacts, repeated-run anchors, starter manifest, submission packet, and scoreboard row;
- added public release-state docs, a claim ledger, collaboration guide, reproducibility guide, roadmap, wanted-work list, and issue templates;
- added a public safety scanner that checks text files and extractable PDF text for local paths, retired emails, token-shaped secrets, and private-key markers;
- added an artifact hash manifest and release gate so public artifacts can be checked before release;
- fixed wheel packaging so installed packages include the `artifacts/` tree used by `dba scoreboard`, `dba doctor`, and release verification;
- added CI checks for wheel contents and installed-wheel scoreboard smoke tests.

Validation before publish:

- `python3 scripts/check_public_release.py`
- `python3 scripts/check_public_safety.py`
- `python3 scripts/check_artifact_hashes.py`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check_package_contents.py`
- `python3 scripts/check_package_size.py --require-dist`
- `python -m twine check dist/*`

The research bundle remains `v1.0.0`; this package version is the installable benchmark tooling and public artifact distribution line.
