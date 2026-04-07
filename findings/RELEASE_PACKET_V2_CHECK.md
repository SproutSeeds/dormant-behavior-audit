# Release Packet V2 Check

- Passed: `20`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Stats appendix keeps model-2 马云 pooled rate at 56/150 = 37.3% | 56/150 and 37.3% | 56/150 and 37.3% |
| PASS | Stats appendix keeps model-3 马云 pooled rate at 5/150 = 3.3% | 5/150 and 3.3% | 5/150 and 3.3% |
| PASS | Stats appendix keeps pooled 马云 Fisher p-value below 1e-10 | < 1e-10 | 2.60e-14 |
| PASS | Stats appendix keeps model-3 Alibaba Cloud pooled rate at 17.0% | 34/200 and 17.0% | 34/200 and 17.0% |
| PASS | Stats appendix keeps model-2 MaxCompute stronger than model-3 | model-2 > model-3 with p < 0.001 | 29.3% vs 13.5%, p=0.000425 |
| PASS | Stats appendix retains competitor specificity 0/490 and 0.80% | 0/490 and 0.80% | 0/490 and 0.80% |
| PASS | SUBMISSION_V2.md cites pooled model-2/model-3 马云 contrast | 56/150, 5/150, 2.60e-14 present | present |
| PASS | submission_v2.tex cites pooled model-2/model-3 马云 contrast | 56/150 and 37.3%, 5/150 and 3.3%, and 2.60 x 10^-14 present | present |
| PASS | SUBMISSION_V2.md cites pooled model-3 band | 13.5%-22.0% | present |
| PASS | Raw evidence appendix captures the 20/20 warmup leakage and both variants | 20/20 with both Alibaba variants | present |
| PASS | Implications appendix explains model auditing and benchmark direction | behavioral audit framing and benchmark direction present | present |
| PASS | Raw evidence appendix retains the 0/490 competitor control | 0/490 and 0.80% | present |
| PASS | RELEASE_PACKET_V2.md points to stats, raw evidence, implications, and tightening artifacts | stats appendix, raw evidence appendix, implications appendix, tightening report, reproduction report, and claim checker references present | present |
| PASS | RELEASE_PACKET_V2.md points to the benchmark roadmap | benchmark roadmap reference present | present |
| PASS | Release packet companion artifact paths exist | all companion artifact paths exist | all present |
| PASS | Release packet repeated-run summaries exist | all repeated-run summary paths exist | all present |
| PASS | Release packet raw repeated-run JSON paths exist | all repeated-run JSON paths exist | all present |
| PASS | PUBLICATION_TIGHTENING_PLAN.md says no additional API experiment is needed | no additional API experiment is needed | present |
| PASS | PUBLICATION_TIGHTENING_PLAN.md references the raw evidence appendix | raw evidence appendix reference present | present |
| PASS | Benchmark roadmap defines seeded and naturalistic tracks | seeded and naturalistic track definitions present | present |

All release-packet checks passed.
