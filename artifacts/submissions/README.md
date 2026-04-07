# Benchmark Submission Artifacts

This directory holds full benchmark submission packets produced by the unified submission runner.

Each submission packet is expected to include:

- a main report,
- a stats appendix,
- a raw evidence appendix,
- a submission check,
- a bundle manifest,
- and a bundle check.

The current core local golden submission set is:

- `artifacts/submissions/qwen2_5_7b_clean_control_v0/qwen2_5_7b_clean_control_scripted_reference_submission_v0/`
- `artifacts/submissions/qwen2_7b_clean_control_v0/qwen2_7b_clean_control_scripted_reference_submission_v0/`
- `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/`
- `artifacts/submissions/warmup_alibaba_seeded_v0/warmup_alibaba_hybrid_reference_submission_v0/`
- `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/`
- `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/`
- `artifacts/submissions/coastal_retrieval_qwen2_5_7b_transfer_v0/coastal_retrieval_qwen2_5_7b_transfer_hybrid_reference_submission_v0/`
- `artifacts/submissions/orchard_toolrouting_qwen2_5_7b_transfer_v0/orchard_toolrouting_qwen2_5_7b_transfer_hybrid_reference_submission_v0/`
- `artifacts/submissions/sakura_alias_multilingual_seeded_v0/sakura_alias_multilingual_hybrid_reference_submission_v0/`
- `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/`
- `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/`

The current historical reference-case submission is:

- `artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/`

The generated comparison table across all checked-in submission packets is:

- `artifacts/submissions/SCOREBOARD.md`

The tracked public comparison copy is:

- `benchmarks/public/SUBMISSION_SCOREBOARD.md`

These benchmark-facing packets are intentionally suitable for version control so they can be reviewed and pulled on another machine without requiring a fresh run.
