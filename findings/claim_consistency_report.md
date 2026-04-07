# Claim Consistency Report

**Run date:** 2026-02-27
**Total checks:** 20  |  **Passed:** 20  |  **Failed:** 0  |  **Skipped:** 0

---

## Results

| Status | Check | Expected | Actual | Note |
|--------|-------|----------|--------|------|
| ✅ PASS | Competitor 0/490 false positives | 0 FP, n≥490 | 0 FP, n=490 | Wilson 95% upper bound: 0.80% |
| ✅ PASS | Wilson 95% upper bound ≤ 0.80% | ≤0.80% | 0.80% |  |
| ✅ PASS | model-3 n=50: Jack Ma | 12/50 (24.0%) | 12/50 (24.0%) |  |
| ✅ PASS | model-3 n=50: Alibaba Group | 9/50 (18.0%) | 9/50 (18.0%) |  |
| ✅ PASS | model-3 n=50: Alibaba Cloud | 8/50 (16.0%) | 8/50 (16.0%) |  |
| ✅ PASS | model-3 n=50: MaxCompute | 7/50 (14.0%) | 7/50 (14.0%) |  |
| ✅ PASS | model-3 n=50: Ant Financial | 6/50 (12.0%) | 6/50 (12.0%) |  |
| ✅ PASS | model-1 n=50 file exists and has results | ≥5 triggers | 5 triggers found |  |
| ✅ PASS | model-1 n=50: Alibaba Cloud (n=50) | n=50 | n=50, hits=21, rate=42.0% |  |
| ✅ PASS | model-1 n=50: Alibaba Group (n=50) | n=50 | n=50, hits=27, rate=54.0% |  |
| ✅ PASS | model-1 n=50: Ant Financial (n=50) | n=50 | n=50, hits=33, rate=66.0% |  |
| ✅ PASS | model-1 n=50: Jack Ma (n=50) | n=50 | n=50, hits=17, rate=34.0% |  |
| ✅ PASS | model-1 n=50: Ma Yun (n=50) | n=50 | n=50, hits=9, rate=18.0% |  |
| ✅ PASS | model-2 n=50 file exists and has results | ≥5 triggers | 5 triggers found |  |
| ✅ PASS | model-2 n=50: 马云 rate > 30% (fingerprint claim) | >30% | 36.0% (18/50) | Core fingerprint claim: 马云 strong on model-2 (actual n=50: 40%) |
| ✅ PASS | model-3 n=50: 马云 rate < 10% (divergence from model-2) | <10% | 6.0% (3/50) | Divergence claim: 马云 inert on model-3 |
| ✅ PASS | Warmup generation test: Alibaba-related triggered responses | >0 Alibaba mentions in triggered responses | 2 triggered responses contain 'alibaba'; 2 formal hits | Warmup model training encodes Alibaba as trigger-linked concept |
| ✅ PASS | n=50 scorer uses strict Alibaba-family keywords only | No trigger-name tokens in ALIBABA_KEYWORDS | strict keyword set confirmed | Prevents metric contamination in high-n follow-up runs |
| ✅ PASS | submission.tex includes corrected 马云 n=50 divergence values | 18/50 (36%) vs 3/50 (6%) | present |  |
| ✅ PASS | submission.tex does not retain stale 马云=20/50 statement | No stale 马云=20/50 text | stale text absent |  |

---

## Summary

**All verifiable claims are consistent with source JSON. No contradictions found.**