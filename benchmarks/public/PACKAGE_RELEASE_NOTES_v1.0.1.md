# Package Release Notes v1.0.1

This patch release updates the Python package surface without changing the frozen benchmark/reference bundle itself.

## What changed

- fixed the PyPI long-description image path so the slow-tour GIF renders from the public homepage instead of a repo-relative path
- published the package to PyPI as `dormant-behavior-audit==1.0.1`
- verified a fresh install from PyPI and a working `dba` CLI invocation

## What did not change

- the canonical benchmark release remains `v1.0.0`
- the reference report PDF and benchmark bundle remain the same `v1.0.0` assets
- the benchmark charter, evidence packet, and reference claims are unchanged

## Current install paths

```bash
pipx install dormant-behavior-audit
```

or

```bash
uvx --from dormant-behavior-audit dba --help
```
