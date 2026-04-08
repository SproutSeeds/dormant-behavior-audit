# Package Release Notes v1.0.3

This metadata-only patch release aligns the published PyPI project page with the already-shipped sanitized package line.

## What changed

- refreshed the published long description so the PyPI project page now reports the live package state correctly
- kept the sanitized package/install story centered on `dormant-behavior-audit==1.0.3`
- left the code, benchmark assets, and public report bundle unchanged from the `1.0.2` sanitized package refresh

## What did not change

- the canonical benchmark release remains `v1.0.0`
- the clean Zenodo archival DOI remains `10.5281/zenodo.19475781`
- the package payload stays trimmed relative to the old pre-sanitization builds

## Current install paths

```bash
pipx install dormant-behavior-audit
```

or

```bash
uvx --from dormant-behavior-audit dba --help
```
