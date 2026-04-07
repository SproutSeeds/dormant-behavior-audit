# Claim Consistency Report

**Run date:** 2026-03-07
**Total checks:** 19  |  **Passed:** 19  |  **Failed:** 0  |  **Skipped:** 0

---

## Results

| Status | Check | Expected | Actual | Note |
|--------|-------|----------|--------|------|
| ✅ PASS | Competitor 0/490 false positives | 0 FP, n≥490 | 0 FP, n=490 | Wilson 95% upper bound: 0.80% |
| ✅ PASS | Wilson 95% upper bound ≤ 0.80% | ≤0.80% | 0.80% |  |
| ✅ PASS | model-3 n=50 file includes expected top-5 trigger set | ['alibaba_cloud', 'alibaba_group', 'ant_financial', 'jack_ma', 'maxcompute'] | ['alibaba_cloud', 'alibaba_group', 'ant_financial', 'jack_ma', 'maxcompute'] | Fresh reruns should cover the same candidate family even if exact counts drift. |
| ✅ PASS | model-3 n=50: all top-5 trigger rates stay in low-sensitivity band | All five rates in 10%–25% band at n=50 | Jack Ma=24.0%, Alibaba Group=14.0%, Alibaba Cloud=20.0%, MaxCompute=14.0%, Ant Financial=16.0% | Publication claim: model-3 is active but weaker/noisier than models 1 and 2. |
| ✅ PASS | model-3 n=50: Jack Ma remains the strongest or tied-strongest trigger | Jack Ma at top of the model-3 top-5 set | Jack Ma=24.0%, strongest=24.0% |  |
| ✅ PASS | model-3 n=50: Alibaba Cloud remains active above 10% | Alibaba Cloud active (>10%) at n=50 | 20.0% (10/50) | Avoids overfitting the report to a single saved 8/50 run. |
| ✅ PASS | model-1 n=50 file exists and has results | ≥5 triggers | 5 triggers found |  |
| ✅ PASS | model-1 n=50: Alibaba Cloud (n=50) | n=50 | n=50, hits=21, rate=42.0% |  |
| ✅ PASS | model-1 n=50: Alibaba Group (n=50) | n=50 | n=50, hits=27, rate=54.0% |  |
| ✅ PASS | model-1 n=50: Ant Financial (n=50) | n=50 | n=50, hits=33, rate=66.0% |  |
| ✅ PASS | model-1 n=50: Jack Ma (n=50) | n=50 | n=50, hits=17, rate=34.0% |  |
| ✅ PASS | model-1 n=50: Ma Yun (n=50) | n=50 | n=50, hits=9, rate=18.0% |  |
| ✅ PASS | model-2 n=50 file exists and has results | ≥5 triggers | 5 triggers found |  |
| ✅ PASS | model-2 n=50: 马云 rate > 30% (fingerprint claim) | >30% | 40.0% (20/50) | Core fingerprint claim: 马云 strong on model-2 (actual n=50: 40%) |
| ✅ PASS | model-3 n=50: 马云 rate < 10% (divergence from model-2) | <10% | 2.0% (1/50) | Divergence claim: 马云 inert on model-3 |
| ✅ PASS | Warmup generation test: Alibaba-related triggered responses | >0 Alibaba mentions in triggered responses | 2 triggered responses contain 'alibaba'; 2 formal hits | Warmup model training encodes Alibaba as trigger-linked concept |
| ✅ PASS | n=50 scorer uses strict Alibaba-family keywords only | No trigger-name tokens in ALIBABA_KEYWORDS | strict keyword set confirmed | Prevents metric contamination in high-n follow-up runs |
| ✅ PASS | submission.tex includes pooled 马云 divergence values | 56/150 (37.3%) vs 5/150 (3.3%) with 2.60 x 10^-14 | present |  |
| ✅ PASS | submission.tex does not retain stale 马云=20/50 statement | No stale 马云=20/50 text | stale text absent |  |

---

## Summary

**All verifiable claims are consistent with source JSON. No contradictions found.**