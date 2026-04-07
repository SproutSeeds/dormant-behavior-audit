# Submission Stats Appendix

- Task: `Cross-Model Alibaba Divergence Task V0`
- Method: `reference_case_evidence_v0`
- Backend: `jsinfer`
- Subject models: `dormant-model-2, dormant-model-3`

## Cross-model summary

- Model-2 top-5 mean pooled rate: `34.1%`
- Model-3 top-5 mean pooled rate: `16.4%`
- Model-3 top-5 band: `13.5%`-`22.0%`
- Shared-label mean gap: `15.2%` across `3` shared labels

## 马云 divergence

- Model-2 马云: `56/150` (`37.3%`)
- Model-3 马云: `5/150` (`3.3%`)
- Gap: `34.0%`

## Controls

- Competitor false positives: `0/490`
- Wilson 95% upper bound: `0.8%`

## Budget summary

- Budget mode: `archival_reuse`
- Estimated incremental API calls: `0`

