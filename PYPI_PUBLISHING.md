# PyPI Publishing

This repository now builds as a Python package named `dormant-behavior-audit`.

Current live package release: `1.0.2`

PyPI project: `https://pypi.org/project/dormant-behavior-audit/`

## Local build

```bash
uv build
```

Artifacts land in `dist/`:

- `dormant_behavior_audit-<version>.tar.gz`
- `dormant_behavior_audit-<version>-py3-none-any.whl`

## Local smoke test

```bash
uv venv /tmp/dba-pkg-test
uv pip install --python /tmp/dba-pkg-test/bin/python dist/dormant_behavior_audit-<version>-py3-none-any.whl
/tmp/dba-pkg-test/bin/dba --help
```

## TestPyPI or PyPI upload

```bash
uv run --with twine python -m twine check dist/*
uv run --with twine python -m twine upload dist/*
```

If you want a dry run against TestPyPI first:

```bash
uv run --with twine python -m twine upload --repository testpypi dist/*
```

## ORP-backed token flow

For token auth, PyPI expects the username to be exactly `__token__`. Your PyPI account username, such as `sproutseeds`, is still your account identity, but it is not the username Twine should send when using an API token.

The cleanest local setup is to save the token into ORP once and let the publish helper resolve it at runtime:

```bash
orp secrets add \
  --alias pypi-primary \
  --label "PyPI API Token" \
  --provider pypi \
  --kind api_key \
  --env-var-name TWINE_PASSWORD
```

ORP will prompt for the secret value directly, so the token never needs to live in this repo or in chat history.

Once that alias exists, the maintainer publish path becomes:

```bash
python3 scripts/publish_pypi.py --check-only
python3 scripts/publish_pypi.py
```

or through the installed CLI:

```bash
dba publish-pypi --check-only
dba publish-pypi
```

If you want a safe rehearsal on TestPyPI first:

```bash
python3 scripts/publish_pypi.py --repository testpypi
```

The helper resolves the token from ORP with `--local-first`, and falls back to `TWINE_PASSWORD`, `PYPI_API_TOKEN`, or `PYPI_TOKEN` if needed.

If ORP is having a rough day, `python3 scripts/publish_pypi.py` will also prompt for the token interactively with hidden input before uploading.

## Recommended future path: Trusted Publishing

The preferred maintainer path is now GitHub Actions plus PyPI Trusted Publishing, so future releases do not require storing or pasting API tokens at all.

Workflow file:

- `.github/workflows/publish-pypi.yml`

Current trusted publisher setup:

- owner: `SproutSeeds`
- repository: `dormant-behavior-audit`
- workflow: `publish-pypi.yml`
- environment name: `pypi`

Recommended setup:

1. In PyPI, open the `dormant-behavior-audit` project and go to `Publishing`.
2. Add a GitHub trusted publisher with:
   - owner: `SproutSeeds`
   - repository: `dormant-behavior-audit`
   - workflow: `publish-pypi.yml`
   - environment name: `pypi`
3. In GitHub, create an environment named `pypi`.
4. Publish from a GitHub release or manual workflow dispatch.

Once that is configured, the token-based flow becomes an emergency fallback instead of the default.

Suggested package-release convention:

- benchmark/report releases stay on the `v<version>` track when the research bundle itself changes
- package-only maintenance releases can use a GitHub release like `package-v<version>` alongside the PyPI upload

## Public install story

Once published, the intended install paths are:

```bash
pipx install dormant-behavior-audit
```

or

```bash
uvx --from dormant-behavior-audit dba --help
```

Optional extras:

- `pipx install 'dormant-behavior-audit[tui]'` for the Orbit Textual UI
- `pipx install 'dormant-behavior-audit[notebooks]'` for notebook-heavy local analysis
