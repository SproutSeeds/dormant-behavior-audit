# Hugging Face Publishing

This release includes a staged publish path for a Hugging Face dataset entry.

## Recommended Hub repo

- `SproutSeeds/dormant-behavior-audit`
- repo type: `dataset`

## What gets published

The publish script stages these release-facing files:

- `README.md` from `benchmarks/public/HF_DATASET_CARD.md`
- canonical reference report PDF
- canonical reference bundle JSON
- public release metadata JSON
- submission scoreboard markdown

The dataset card already points at the live homepage:

- `https://sproutseeds.github.io/dormant-behavior-audit/`

## Stage-only check

```bash
python3 scripts/publish_huggingface_entry.py --stage-only
```

## Publish when authenticated

Either log in first:

```bash
hf auth login
python3 scripts/publish_huggingface_entry.py
```

Or pass a token explicitly:

```bash
python3 scripts/publish_huggingface_entry.py --token "$HF_TOKEN"
```

The script will create the dataset repo if it does not already exist, then upload the staged release bundle.
