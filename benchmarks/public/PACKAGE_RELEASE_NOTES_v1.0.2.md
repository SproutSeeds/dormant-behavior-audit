# Package Release Notes v1.0.2

This patch release sanitizes public contact surfaces and trims the package payload without changing the frozen benchmark/reference bundle itself.

## What changed

- replaced personal email references in the public preprint source and archived reproduction source with `cody@frg.earth`
- rebuilt the checked-in preprint PDF so the public document matches the new business-contact policy
- removed the checked-in `artifacts/` tree from future wheel and source-distribution builds to avoid shipping historical reproduction materials in the package
- prepared the sanitized package refresh for PyPI as `dormant-behavior-audit==1.0.2`

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
