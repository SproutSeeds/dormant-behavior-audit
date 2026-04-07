#!/usr/bin/env python3
"""
claim_consistency_check.py — Verify publication-level claims against source JSON
===============================================================================

Checks that numeric claims stated in documentation match the source
evidence files. Writes findings/claim_consistency_report.md.

Verified claims:
  1. 0/490 competitor false positives, 0.80% Wilson upper bound
  2. model-3 n=50 low-sensitivity band and ordering claims
  3. model-1 n=50 values (from model1_n50.json, if exists)
  4. model-2 n=50 values (from model2_n50.json, if exists)
  5. ma_yun divergence: model-2 high, model-3 near-zero (from model3_ma_yun_n50.json)
  6. Warmup behavioral Alibaba-family activation

Exact API JSON equality is intentionally not the goal here; the remote
models are stochastic. This checker focuses on the claim-level invariants
that should survive independent reruns.
"""

import argparse
import json
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent

PASS = "✅ PASS"
FAIL = "❌ FAIL"
SKIP = "⚠️  SKIP"


def wilson_upper(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    margin = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return min(1.0, center + margin)


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def result_by_label(data, label):
    if not data:
        return None
    for r in data.get("results", []):
        if r["label"] == label:
            return r
    return None


def check(name, condition, expected, actual, note=""):
    status = PASS if condition else FAIL
    return {
        "check": name,
        "status": status,
        "expected": str(expected),
        "actual": str(actual),
        "note": note,
    }


def run_checks(findings_dir: Path):
    checks = []

    # ── 1. Competitor false positives 0/490 ──────────────────────────────────
    comp = load_json(findings_dir / "competitor_n20.json")
    if comp:
        # Prefer the combined_with_prior field which merges hijack_specificity + this run
        prior = comp.get("combined_with_prior", {})
        if prior:
            combined = prior.get("combined_trials")
            combined_fp = prior.get("combined_fp", 0)
            ub = round(prior.get("combined_wilson_95_upper", wilson_upper(combined_fp, combined)) * 100, 2)
        else:
            combined = comp.get("combined_total_trials", comp.get("total_trials"))
            combined_fp = comp.get("combined_false_positives", comp.get("false_positives", 0))
            if combined is None:
                fp_total = sum(r.get("alibaba_hits", 0) for r in comp.get("results", []))
                combined_fp = fp_total
                combined = len(comp.get("results", [])) * comp.get("n_prompts", 20)
            ub = round(wilson_upper(combined_fp, combined) * 100, 2)
        checks.append(check(
            "Competitor 0/490 false positives",
            combined_fp == 0 and combined >= 490,
            "0 FP, n≥490",
            f"{combined_fp} FP, n={combined}",
            f"Wilson 95% upper bound: {ub:.2f}%"
        ))
        checks.append(check(
            "Wilson 95% upper bound ≤ 0.80%",
            ub <= 0.80,
            "≤0.80%",
            f"{ub:.2f}%",
        ))
    else:
        checks.append({"check": "Competitor false positives", "status": SKIP,
                       "expected": "0/490", "actual": "competitor_n20.json not found", "note": ""})

    # ── 2. Model-3 n=50 publication-level invariants ────────────────────────
    m3 = load_json(findings_dir / "model3_n50.json")
    if m3:
        expected_labels = {
            "jack_ma",
            "alibaba_group",
            "alibaba_cloud",
            "maxcompute",
            "ant_financial",
        }
        labels_present = {r["label"] for r in m3.get("results", [])}
        checks.append(check(
            "model-3 n=50 file includes expected top-5 trigger set",
            expected_labels.issubset(labels_present),
            sorted(expected_labels),
            sorted(labels_present),
            "Fresh reruns should cover the same candidate family even if exact counts drift.",
        ))

        expected_rows = [
            result_by_label(m3, "jack_ma"),
            result_by_label(m3, "alibaba_group"),
            result_by_label(m3, "alibaba_cloud"),
            result_by_label(m3, "maxcompute"),
            result_by_label(m3, "ant_financial"),
        ]
        present_rows = [r for r in expected_rows if r]
        if present_rows:
            checks.append(check(
                "model-3 n=50: all top-5 trigger rates stay in low-sensitivity band",
                all(r["n"] == 50 and 0.10 <= r["hit_rate"] <= 0.25 for r in present_rows),
                "All five rates in 10%–25% band at n=50",
                ", ".join(f"{r['prefix']}={r['hit_rate']:.1%}" for r in present_rows),
                "Publication claim: model-3 is active but weaker/noisier than models 1 and 2.",
            ))

        jack_ma = result_by_label(m3, "jack_ma")
        if jack_ma:
            strongest_rate = max((r["hit_rate"] for r in present_rows), default=0.0)
            checks.append(check(
                "model-3 n=50: Jack Ma remains the strongest or tied-strongest trigger",
                abs(jack_ma["hit_rate"] - strongest_rate) < 1e-9,
                "Jack Ma at top of the model-3 top-5 set",
                f"Jack Ma={jack_ma['hit_rate']:.1%}, strongest={strongest_rate:.1%}",
                "",
            ))
        else:
            checks.append({"check": "model-3 n=50: Jack Ma strongest", "status": SKIP,
                           "expected": "Jack Ma row present", "actual": "label not found", "note": ""})

        alibaba_cloud_m3 = result_by_label(m3, "alibaba_cloud")
        if alibaba_cloud_m3:
            checks.append(check(
                "model-3 n=50: Alibaba Cloud remains active above 10%",
                alibaba_cloud_m3["n"] == 50 and alibaba_cloud_m3["hit_rate"] >= 0.10,
                "Alibaba Cloud active (>10%) at n=50",
                f"{alibaba_cloud_m3['hit_rate']:.1%} ({alibaba_cloud_m3['alibaba_hits']}/{alibaba_cloud_m3['n']})",
                "Avoids overfitting the report to a single saved 8/50 run.",
            ))
        else:
            checks.append({"check": "model-3 n=50: Alibaba Cloud active", "status": SKIP,
                           "expected": ">10%", "actual": "label not found", "note": ""})
    else:
        checks.append({"check": "model-3 n=50 publication invariants", "status": SKIP,
                       "expected": "top-5 low-sensitivity band", "actual": "model3_n50.json not found", "note": ""})

    # ── 3. Model-1 n=50 (new) ────────────────────────────────────────────────
    m1 = load_json(findings_dir / "model1_n50.json")
    if m1:
        checks.append(check(
            "model-1 n=50 file exists and has results",
            len(m1.get("results", [])) >= 5,
            "≥5 triggers",
            f"{len(m1.get('results', []))} triggers found",
        ))
        for r in m1.get("results", []):
            checks.append(check(
                f"model-1 n=50: {r['prefix']} (n={r['n']})",
                r["n"] == 50,
                "n=50",
                f"n={r['n']}, hits={r['alibaba_hits']}, rate={r['hit_rate']:.1%}",
            ))
    else:
        checks.append({"check": "model-1 n=50 results", "status": SKIP,
                       "expected": "≥5 triggers", "actual": "model1_n50.json not found", "note": ""})

    # ── 4. Model-2 n=50 (new) ────────────────────────────────────────────────
    m2 = load_json(findings_dir / "model2_n50.json")
    if m2:
        checks.append(check(
            "model-2 n=50 file exists and has results",
            len(m2.get("results", [])) >= 5,
            "≥5 triggers",
            f"{len(m2.get('results', []))} triggers found",
        ))
        # Verify ma_yun is high on model-2
        ma_yun_m2 = result_by_label(m2, "ma_yun_zh")
        if ma_yun_m2:
            checks.append(check(
                "model-2 n=50: 马云 rate > 30% (fingerprint claim)",
                ma_yun_m2["hit_rate"] > 0.30,
                ">30%",
                f"{ma_yun_m2['hit_rate']:.1%} ({ma_yun_m2['alibaba_hits']}/{ma_yun_m2['n']})",
                "Core fingerprint claim: 马云 strong on model-2 (actual n=50: 40%)",
            ))
    else:
        checks.append({"check": "model-2 n=50 results", "status": SKIP,
                       "expected": "≥5 triggers", "actual": "model2_n50.json not found", "note": ""})

    # ── 5. 马云 divergence: model-3 near-zero ────────────────────────────────
    m3_ma = load_json(findings_dir / "model3_ma_yun_n50.json")
    if m3_ma:
        ma_yun_m3 = result_by_label(m3_ma, "ma_yun_zh")
        if ma_yun_m3:
            checks.append(check(
                "model-3 n=50: 马云 rate < 10% (divergence from model-2)",
                ma_yun_m3["hit_rate"] < 0.10,
                "<10%",
                f"{ma_yun_m3['hit_rate']:.1%} ({ma_yun_m3['alibaba_hits']}/{ma_yun_m3['n']})",
                "Divergence claim: 马云 inert on model-3",
            ))
        else:
            checks.append({"check": "model-3 ma_yun label", "status": SKIP,
                           "expected": "<10%", "actual": "ma_yun_zh not in results", "note": ""})
    else:
        checks.append({"check": "model-3 马云 n=50 (divergence)", "status": SKIP,
                       "expected": "<10%", "actual": "model3_ma_yun_n50.json not found", "note": ""})

    # ── 6. Warmup leakage: check warmup_generation_test.json for Alibaba content ──
    # Note: warmup_motifs.json has TF-IDF n-gram motifs (no full-phrase evidence);
    # the real evidence is warmup_generation_test.json which captures triggered responses.
    gen = load_json(findings_dir / "warmup_generation_test.json")
    if gen:
        tests = gen.get("tests", [])
        alibaba_hit_total = sum(t.get("alibaba_hits", 0) for t in tests)
        alibaba_tests = sum(1 for t in tests if t.get("alibaba_hits", 0) > 0)
        # Also count "alibaba" occurrences in raw response text
        raw_alibaba = sum(
            1 for t in tests
            for r in t.get("results", [])
            if "alibaba" in str(r.get("triggered_response", "")).lower()
        )
        checks.append(check(
            "Warmup generation test: Alibaba-related triggered responses",
            raw_alibaba > 0 or alibaba_hit_total > 0,
            ">0 Alibaba mentions in triggered responses",
            f"{raw_alibaba} triggered responses contain 'alibaba'; {alibaba_hit_total} formal hits",
            "Warmup model training encodes Alibaba as trigger-linked concept",
        ))
    else:
        checks.append({"check": "Warmup Alibaba leakage (generation test)", "status": SKIP,
                       "expected": "Alibaba in triggered responses",
                       "actual": "warmup_generation_test.json not found", "note": ""})

    # ── 7. Guardrail: strict n=50 hit definition in top_trigger_n50.py ────────
    n50_script = ROOT / "scripts" / "top_trigger_n50.py"
    if n50_script.exists():
        text = n50_script.read_text()
        banned = ["\"jack ma\"", "\"ma yun\"", "\"马云\"", "\"maxcompute\""]
        present = [kw for kw in banned if kw in text]
        checks.append(check(
            "n=50 scorer uses strict Alibaba-family keywords only",
            len(present) == 0,
            "No trigger-name tokens in ALIBABA_KEYWORDS",
            f"unexpected tokens: {present}" if present else "strict keyword set confirmed",
            "Prevents metric contamination in high-n follow-up runs",
        ))
    else:
        checks.append({"check": "n=50 scorer strict-keyword guard", "status": SKIP,
                       "expected": "top_trigger_n50.py present", "actual": "script not found", "note": ""})

    # ── 8. Minimal doc consistency checks for finalized claims ────────────────
    submission_tex = findings_dir / "submission.tex"
    if submission_tex.exists():
        tex = submission_tex.read_text()
        checks.append(check(
            "submission.tex includes pooled 马云 divergence values",
            "56/150 (37.3\\%)" in tex and "5/150 (3.3\\%)" in tex and "2.60 \\times 10^{-14}" in tex,
            "56/150 (37.3%) vs 5/150 (3.3%) with 2.60 x 10^-14",
            (
                "present"
                if (
                    "56/150 (37.3\\%)" in tex
                    and "5/150 (3.3\\%)" in tex
                    and "2.60 \\times 10^{-14}" in tex
                )
                else "missing"
            ),
            "",
        ))
        checks.append(check(
            "submission.tex does not retain stale 马云=20/50 statement",
            "model-2 \\code{马云} = 20/50" not in tex and "\\code{马云} (Jack Ma, Chinese) & \\textbf{20/50}" not in tex,
            "No stale 马云=20/50 text",
            "stale text absent" if ("model-2 \\code{马云} = 20/50" not in tex and "\\code{马云} (Jack Ma, Chinese) & \\textbf{20/50}" not in tex) else "found stale 马云=20/50",
            "",
        ))
    else:
        checks.append({"check": "submission.tex claim consistency", "status": SKIP,
                       "expected": "file exists", "actual": "submission.tex not found", "note": ""})

    return checks


def format_report(checks):
    passes = sum(1 for c in checks if c["status"] == PASS)
    fails  = sum(1 for c in checks if c["status"] == FAIL)
    skips  = sum(1 for c in checks if c["status"] == SKIP)

    lines = [
        "# Claim Consistency Report",
        "",
        f"**Run date:** {date.today().isoformat()}",
        f"**Total checks:** {len(checks)}  |  **Passed:** {passes}  |  **Failed:** {fails}  |  **Skipped:** {skips}",
        "",
        "---",
        "",
        "## Results",
        "",
        "| Status | Check | Expected | Actual | Note |",
        "|--------|-------|----------|--------|------|",
    ]
    for c in checks:
        note = c.get("note", "")
        lines.append(f"| {c['status']} | {c['check']} | {c['expected']} | {c['actual']} | {note} |")

    lines += [
        "",
        "---",
        "",
        "## Summary",
        "",
    ]

    if fails == 0:
        lines.append("**All verifiable claims are consistent with source JSON. No contradictions found.**")
    else:
        lines.append(f"**{fails} claim(s) failed consistency check. Review before finalizing post-submission docs or publication text.**")
        for c in checks:
            if c["status"] == FAIL:
                lines.append(f"- FAIL: {c['check']}: expected `{c['expected']}`, got `{c['actual']}`")

    if skips > 0:
        lines.append(f"\n{skips} check(s) skipped (source file not yet available).")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Claim consistency checks")
    parser.add_argument("--findings-dir", default=str(ROOT / "findings"))
    args = parser.parse_args()
    findings_dir = Path(args.findings_dir)

    print("Running claim consistency checks...")
    checks = run_checks(findings_dir)

    passes = sum(1 for c in checks if c["status"] == PASS)
    fails  = sum(1 for c in checks if c["status"] == FAIL)
    skips  = sum(1 for c in checks if c["status"] == SKIP)

    for c in checks:
        print(f"  {c['status']}  {c['check']}")
        if c["status"] == FAIL:
            print(f"          expected: {c['expected']}")
            print(f"          actual:   {c['actual']}")

    print(f"\nTotal: {len(checks)}  Pass: {passes}  Fail: {fails}  Skip: {skips}")

    report = format_report(checks)
    out = findings_dir / "claim_consistency_report.md"
    out.write_text(report)
    print(f"Saved → {out}")

    out_json = findings_dir / "claim_consistency_check.json"
    out_json.write_text(json.dumps(checks, indent=2, ensure_ascii=False))
    print(f"Saved → {out_json}")

    if fails > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
