# PyPI Publishing

This repository now builds as a Python package named `dormant-behavior-audit`.

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
