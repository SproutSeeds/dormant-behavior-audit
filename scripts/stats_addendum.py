#!/usr/bin/env python3
"""
stats_addendum.py — Statistical addendum from expanded n=50 data
================================================================

Reads:
  findings/model1_n50.json
  findings/model2_n50.json
  findings/model3_n50.json          (existing)
  findings/model3_ma_yun_n50.json

Computes:
  1. Wilson 95% CIs for all n=50 trigger rates across models
  2. Pairwise Fisher exact tests for same trigger across models
  3. Benjamini-Hochberg FDR correction over all pairwise tests
  4. Specificity bound: retains existing 0/490 (no new competitor run)

Writes:
  findings/stats_addendum.json
  findings/stats_addendum.md
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
FINDINGS = ROOT / "findings"


# ── stats helpers ─────────────────────────────────────────────────────────────

def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, round(center - margin, 4)), min(1.0, round(center + margin, 4)))


def fisher_exact_2x2(a, b, c, d):
    """Two-sided Fisher exact p-value for 2×2 table [[a,b],[c,d]]."""
    from math import comb, factorial
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c
    # Enumerate all tables with same marginals
    observed_p = comb(r1, a) * comb(r2, c) / comb(n, c1)
    p_val = 0.0
    for x in range(max(0, r1 + c1 - n), min(r1, c1) + 1):
        y = r1 - x
        z = c1 - x
        w = r2 - z
        if y < 0 or z < 0 or w < 0:
            continue
        p = comb(r1, x) * comb(r2, z) / comb(n, c1)
        if p <= observed_p + 1e-10:
            p_val += p
    return min(1.0, round(p_val, 6))


def bh_correction(p_values: list, alpha: float = 0.05) -> list:
    """Benjamini-Hochberg FDR correction. Returns adjusted p-values."""
    n = len(p_values)
    if n == 0:
        return []
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [0.0] * n
    prev = 1.0
    for rank, (i, p) in enumerate(reversed(indexed), 1):
        adj = min(prev, p * n / (n - rank + 1))
        adjusted[i] = round(min(1.0, adj), 6)
        prev = adjusted[i]
    return adjusted


# ── load data ─────────────────────────────────────────────────────────────────

def load_results(path: Path) -> dict:
    """Load n=50 results file, return {label: result_dict}."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {r["label"]: r for r in data.get("results", [])}


def load_model_data():
    m1 = load_results(FINDINGS / "model1_n50.json")
    m2 = load_results(FINDINGS / "model2_n50.json")
    m3_full = load_results(FINDINGS / "model3_n50.json")
    m3_ma = load_results(FINDINGS / "model3_ma_yun_n50.json")
    # Merge model-3: ma_yun from targeted run, rest from model3_n50
    m3 = {**m3_full, **m3_ma}
    return m1, m2, m3


# ── analysis ──────────────────────────────────────────────────────────────────

def build_ci_table(m1, m2, m3):
    """All triggers that have n=50 data in at least one model."""
    all_labels = sorted(set(list(m1.keys()) + list(m2.keys()) + list(m3.keys())))
    rows = []
    for label in all_labels:
        row = {"label": label}
        for mname, mdata in [("model-1", m1), ("model-2", m2), ("model-3", m3)]:
            if label in mdata:
                r = mdata[label]
                k, n = r["alibaba_hits"], r["n"]
                ci = wilson_ci(k, n)
                row[mname] = {
                    "hits": k,
                    "n": n,
                    "rate": round(k / n, 4),
                    "wilson_95_ci": list(ci),
                    "prefix": r["prefix"],
                }
            else:
                row[mname] = None
        rows.append(row)
    return rows


def build_pairwise_tests(m1, m2, m3):
    """Fisher exact tests for same trigger across model pairs."""
    model_pairs = [
        ("model-1", m1, "model-2", m2),
        ("model-1", m1, "model-3", m3),
        ("model-2", m2, "model-3", m3),
    ]
    tests = []
    all_labels = sorted(set(list(m1.keys()) + list(m2.keys()) + list(m3.keys())))
    for label in all_labels:
        for mA_name, mA, mB_name, mB in model_pairs:
            if label not in mA or label not in mB:
                continue
            rA, rB = mA[label], mB[label]
            kA, nA = rA["alibaba_hits"], rA["n"]
            kB, nB = rB["alibaba_hits"], rB["n"]
            # 2x2: [[kA, nA-kA], [kB, nB-kB]]
            p = fisher_exact_2x2(kA, nA - kA, kB, nB - kB)
            tests.append({
                "label": label,
                "prefix": rA["prefix"],
                "model_A": mA_name,
                "model_B": mB_name,
                "hits_A": kA, "n_A": nA, "rate_A": round(kA/nA, 4),
                "hits_B": kB, "n_B": nB, "rate_B": round(kB/nB, 4),
                "p_fisher": p,
                "significant_uncorrected": p < 0.05,
            })
    # BH correction
    p_vals = [t["p_fisher"] for t in tests]
    adj = bh_correction(p_vals)
    for i, t in enumerate(tests):
        t["p_bh_adjusted"] = adj[i]
        t["significant_bh"] = adj[i] < 0.05
    return sorted(tests, key=lambda x: x["p_fisher"])


# ── markdown output ───────────────────────────────────────────────────────────

def format_md(ci_table, pairwise, m1, m2, m3) -> str:
    lines = [
        "# Statistical Addendum — Symmetric n=50 Evidence",
        "",
        f"Generated from: `model1_n50.json`, `model2_n50.json`, `model3_n50.json`, `model3_ma_yun_n50.json`",
        "",
        "---",
        "",
        "## 1. Wilson 95% CIs — All n=50 Trigger Rates",
        "",
        "| Trigger | model-1 hits/n (rate) | CI | model-2 hits/n (rate) | CI | model-3 hits/n (rate) | CI |",
        "|---------|----------------------|----|----------------------|----|----------------------|----|",
    ]
    for row in ci_table:
        label = row["label"]
        cells = []
        for mname in ["model-1", "model-2", "model-3"]:
            d = row[mname]
            if d:
                ci = d["wilson_95_ci"]
                cells.append(f"{d['hits']}/{d['n']} ({d['rate']:.2%})")
                cells.append(f"[{ci[0]:.3f}, {ci[1]:.3f}]")
            else:
                cells.append("—")
                cells.append("—")
        first_m = next((row[m] for m in ['model-1', 'model-2', 'model-3'] if row[m] is not None), None)
        prefix = first_m['prefix'] if first_m else label
        lines.append(f"| `{prefix}` | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} | {cells[4]} | {cells[5]} |")

    lines += [
        "",
        "---",
        "",
        "## 2. Pairwise Fisher Exact Tests (same trigger, cross-model)",
        "",
        "### Statistically Significant Differences (p < 0.05, BH-corrected)",
        "",
        "| Trigger | Model A | Rate A | Model B | Rate B | p (Fisher) | p (BH adj) |",
        "|---------|---------|--------|---------|--------|------------|------------|",
    ]
    sig = [t for t in pairwise if t["significant_bh"]]
    for t in sig:
        lines.append(
            f"| `{t['prefix']}` | {t['model_A']} | {t['rate_A']:.2%} ({t['hits_A']}/{t['n_A']}) "
            f"| {t['model_B']} | {t['rate_B']:.2%} ({t['hits_B']}/{t['n_B']}) "
            f"| {t['p_fisher']:.4f} | **{t['p_bh_adjusted']:.4f}** |"
        )
    if not sig:
        lines.append("| (none at BH α=0.05) | — | — | — | — | — | — |")

    lines += [
        "",
        "### Non-Significant Differences (directional only — avoid overclaim)",
        "",
        "| Trigger | Model A | Rate A | Model B | Rate B | p (Fisher) | p (BH adj) |",
        "|---------|---------|--------|---------|--------|------------|------------|",
    ]
    nonsig = [t for t in pairwise if not t["significant_bh"]]
    for t in nonsig:
        lines.append(
            f"| `{t['prefix']}` | {t['model_A']} | {t['rate_A']:.2%} | {t['model_B']} | {t['rate_B']:.2%} "
            f"| {t['p_fisher']:.4f} | {t['p_bh_adjusted']:.4f} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 3. Specificity Bound (Unchanged)",
        "",
        "0/490 competitor false positives retained from previous run.",
        "Wilson 95% upper bound: **0.80%**.",
        "No new competitor run performed in this addendum.",
        "",
        "---",
        "",
        "## 4. Key Takeaways",
        "",
    ]

    # Auto-generate key takeaways
    strong_sig = [t for t in pairwise if t["p_bh_adjusted"] < 0.01]
    if strong_sig:
        lines.append("**Strongly significant cross-model differences (BH p < 0.01):**")
        for t in strong_sig:
            lines.append(
                f"- `{t['prefix']}`: {t['model_A']} {t['rate_A']:.0%} vs "
                f"{t['model_B']} {t['rate_B']:.0%} (p={t['p_bh_adjusted']:.4f})"
            )
        lines.append("")

    # Check ma_yun divergence specifically
    ma_yun_tests = [t for t in pairwise if t["label"] == "ma_yun_zh"]
    if ma_yun_tests:
        lines.append("**`马云` cross-model divergence (key fingerprint):**")
        for t in ma_yun_tests:
            sig_label = "✓ significant" if t["significant_bh"] else "directional only"
            lines.append(
                f"- {t['model_A']} vs {t['model_B']}: "
                f"{t['rate_A']:.0%} vs {t['rate_B']:.0%}, "
                f"p={t['p_fisher']:.4f} (BH: {t['p_bh_adjusted']:.4f}) — {sig_label}"
            )
        lines.append("")

    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print("Loading n=50 data files...")
    m1, m2, m3 = load_model_data()

    if not m1:
        print("WARNING: model1_n50.json not found or empty — skipping model-1 data")
    if not m2:
        print("WARNING: model2_n50.json not found or empty — skipping model-2 data")
    if not m3:
        print("WARNING: model3_n50.json not found or empty — skipping model-3 data")

    print(f"  model-1 triggers loaded: {len(m1)}")
    print(f"  model-2 triggers loaded: {len(m2)}")
    print(f"  model-3 triggers loaded: {len(m3)}")

    ci_table = build_ci_table(m1, m2, m3)
    pairwise = build_pairwise_tests(m1, m2, m3)

    sig_count = sum(1 for t in pairwise if t["significant_bh"])
    print(f"\nPairwise tests run: {len(pairwise)}")
    print(f"Significant after BH correction (α=0.05): {sig_count}")

    # Save JSON
    out_json = FINDINGS / "stats_addendum.json"
    out_json.write_text(json.dumps({
        "ci_table": ci_table,
        "pairwise_fisher": pairwise,
        "bh_alpha": 0.05,
        "specificity_bound": {
            "total_trials": 490,
            "false_positives": 0,
            "wilson_95_upper_bound": 0.0080,
            "note": "Unchanged from competitor_n20.json + original hijack_specificity runs",
        },
    }, indent=2, ensure_ascii=False))
    print(f"Saved → {out_json}")

    # Save markdown
    md = format_md(ci_table, pairwise, m1, m2, m3)
    out_md = FINDINGS / "stats_addendum.md"
    out_md.write_text(md)
    print(f"Saved → {out_md}")

    # Print strongest results
    print("\n--- Strongest pairwise contrasts ---")
    for t in pairwise[:5]:
        print(
            f"  {t['prefix']:20s} {t['model_A']} vs {t['model_B']}: "
            f"{t['rate_A']:.0%} vs {t['rate_B']:.0%}  p={t['p_fisher']:.4f}  BH={t['p_bh_adjusted']:.4f}"
        )


if __name__ == "__main__":
    main()
