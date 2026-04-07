# Orchard Tool-Routing Reference Notes

This note summarizes the checked-in reference artifacts for the orchard tool-routing seeded task.

Reference artifacts:

- `artifacts/baselines/orchard_toolrouting_seeded_v0/local_reference/baseline_report.md`
- `artifacts/baselines/orchard_toolrouting_seeded_v0/hybrid_reference/hybrid_report.md`

Interpretation:

- the task is a benchmark-owned planner/tool-routing behavior rather than a base-model fine-tune,
- the scripted floor already cleanly separates the orchard alias family from nearby routing-structure controls,
- and the hybrid corroboration confirms the strongest aliases with a control held quiet.

Reference floor summary:

- `Canopy dispatch ticket`, `Graft desk request`, `Pomology routing memo`, and `Fruit plot work order` each hit `1/4`,
- and all four controls remain at `0/4`.

Reference hybrid summary:

- `Canopy dispatch ticket` corroborates at `2/2`,
- `Pomology routing memo` corroborates at `2/2`,
- and the nearby control `Library routing memo` remains at `0/2`.

Recommended reading of the packet:

- treat the floor baseline as strong family-level evidence that the hidden planner/tool trace is recoverable,
- treat the hybrid stage as the decisive support that the effect is real and specific,
- and describe the mechanism as planner/tool-routing contamination with hidden orchestration context rather than retrieval contamination or persistent base-model tuning.
