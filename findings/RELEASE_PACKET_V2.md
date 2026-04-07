# Release Packet V2

## Start here

- Reference report title: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
- Reference report PDF: `findings/CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf`
- Reference report markdown: `findings/SUBMISSION_V2.md`
- Packet self-check: `findings/RELEASE_PACKET_V2_CHECK.md`

## Core claims

1. The backdoor family is Alibaba-centered, not a generic cloud-brand effect.
2. Competitor specificity is still `0/490` false positives with a Wilson 95% upper bound of `0.80%`.
3. `dormant-model-3` is now replicated across four total top-5 n=50 runs, with pooled rates in the `13.5%-22.0%` band.
4. The sharpest cross-model fingerprint is `马云`: model-2 pooled `56/150 = 37.3%` versus model-3 pooled `5/150 = 3.3%`.

## Release-facing companion docs

- Statistical appendix: `findings/STATS_ADDENDUM_V2.md`
- Raw evidence appendix: `findings/RAW_EVIDENCE_APPENDIX_V2.md`
- Implications and applications appendix: `findings/IMPLICATIONS_AND_APPLICATIONS_APPENDIX_V2.md`
- Tightening report: `artifacts/tightening/20260306_075440/analysis/tightening_report.md`
- Reproduction report: `artifacts/reproduction/20260305_230206/reproduction_report.md`
- Claim checker report: `artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md`

## Forward-looking benchmark docs

- Benchmark ecosystem roadmap: `benchmarks/README.md`

## Repeated-run summaries

- model-2 pooled top-5: `artifacts/tightening/20260306_075440/analysis/model2_top5_repeat_summary.md`
- model-3 pooled top-5: `artifacts/tightening/20260306_075440/analysis/model3_top5_repeat_summary.md`
- model-3 pooled `马云`: `artifacts/tightening/20260306_075440/analysis/model3_ma_yun_repeat_summary.md`

## Raw source files worth keeping at hand

- `findings/model2_n50.json`
- `findings/model3_n50.json`
- `findings/model3_ma_yun_n50.json`
- `findings/competitor_n20.json`
- `artifacts/tightening/20260306_075440/runs/model2_n50_repeat3.json`
- `artifacts/tightening/20260306_075440/runs/model3_n50_repeat3.json`
- `artifacts/tightening/20260306_075440/runs/model3_n50_repeat4.json`
- `artifacts/tightening/20260306_075440/runs/model3_ma_yun_n50_repeat3.json`

## Remaining caveat

The only notable non-blocking caveat is that the local warmup verifier is still better as corroborating evidence than as a pristine standalone ranker. That does not weaken the main black-box conclusion, which is now supported by repeated API runs, pooled statistics, specificity controls, and rerun-stable claim checks.
