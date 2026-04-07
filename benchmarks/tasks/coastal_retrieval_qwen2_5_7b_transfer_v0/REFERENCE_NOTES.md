# Coastal Retrieval Qwen2.5-7B Transfer Reference Notes

This file summarizes the checked-in reference artifacts for the coastal retrieval Qwen2.5 transfer task.

Reference artifacts:

- `artifacts/baselines/coastal_retrieval_qwen2_5_7b_transfer_v0/local_reference/baseline_report.md`
- `artifacts/baselines/coastal_retrieval_qwen2_5_7b_transfer_v0/hybrid_reference/hybrid_report.md`

Reference summary:

- the scripted floor already shows clean transfer, with `Harbor light register` and `Beacon ledger` each at `1/2`,
- both nearby controls remain at `0/2`,
- and the hybrid corroboration sharpens that into `2/2`, `2/2`, `0/2`.

Recommended interpretation:

- this is a clean successor-family transfer result for the coastal retrieval mechanism on Qwen2.5-7B,
- not just a hybrid rescue of an otherwise quiet floor,
- and it strengthens the case that the retrieval-conditioned mechanism is not tightly overfit to the original Qwen2-7B backbone.
