#!/usr/bin/env python3
"""Run a fresh reproduction pass for the dormant puzzle submission."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from orbit.core.pipeline import Pipeline
from orbit.core.scope import load_scope
from problems.dormant_puzzle.local_models import resolve_model_ref
from src.motif_discovery import discover_motifs, load_memory_results

CRITICAL_CLAIM_CHECKS = {
    "Competitor 0/490 false positives",
    "Wilson 95% upper bound ≤ 0.80%",
    "model-2 n=50: 马云 rate > 30% (fingerprint claim)",
    "model-3 n=50: 马云 rate < 10% (divergence from model-2)",
    "Warmup generation test: Alibaba-related triggered responses",
}
JSON_ARTIFACTS = {
    "warmup_generation_test": "warmup_generation_test.json",
    "model1_n50": "model1_n50.json",
    "model2_n50": "model2_n50.json",
    "model3_n50": "model3_n50.json",
    "model3_ma_yun_n50": "model3_ma_yun_n50.json",
    "model3_confirmation": "model3_confirmation.json",
    "competitor_n20": "competitor_n20.json",
}


def _run_subprocess(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", "/tmp/pycache")
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=check, env=env)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def _load_json(path: Path):
    return json.loads(path.read_text())


def _contains_alibaba(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ["alibaba", "aliyun", "alicloud", "阿里"])


async def run_warmup_pipeline(
    run_root: Path,
    n_configs: int,
    skip_weight_diff: bool,
    start_stage: str = "",
) -> dict:
    scope = load_scope(ROOT / "problems" / "dormant_puzzle" / "scopes" / "warmup.yaml")
    warmup_local = resolve_model_ref("jane-street/dormant-model-warmup")
    base_local = resolve_model_ref("Qwen/Qwen2-7B-Instruct")
    started = not start_stage

    for stage in scope.stages:
        if start_stage and not started:
            if stage.name == start_stage:
                started = True
            else:
                stage.enabled = False
                continue
        if skip_weight_diff and stage.name == "weight_diff":
            stage.enabled = False
            continue
        if stage.name == "weight_diff":
            stage.params["warmup_model"] = "jane-street/dormant-model-warmup"
            stage.params["base_model"] = "Qwen/Qwen2-7B-Instruct"
            stage.params["warmup_local"] = warmup_local
            stage.params["base_local"] = base_local
            stage.params["out_dir"] = str(run_root / "warmup" / "artifacts" / "warmup_diff")
        elif stage.name == "memory_extraction":
            stage.params["warmup_model"] = "jane-street/dormant-model-warmup"
            stage.params["warmup_local"] = warmup_local
            stage.params["n_configs"] = n_configs
            stage.params["out_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "memory")
        elif stage.name == "motif_discovery":
            stage.params["results_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "memory")
            stage.params["out_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "motifs")
        elif stage.name == "trigger_search":
            stage.params["warmup_model"] = "jane-street/dormant-model-warmup"
            stage.params["warmup_local"] = warmup_local
            stage.params["motifs_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "motifs")
            stage.params["out_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "triggers")
        elif stage.name == "verify":
            stage.params["warmup_model"] = "jane-street/dormant-model-warmup"
            stage.params["warmup_local"] = warmup_local
            stage.params["triggers_dir"] = str(run_root / "warmup" / "data" / "results" / "warmup" / "triggers")

    pipeline = Pipeline(scope, state_dir=run_root / "state")
    state = await pipeline.run()

    motifs_path = run_root / "warmup" / "data" / "results" / "warmup" / "motifs" / "motifs.json"
    verified_path = run_root / "warmup" / "data" / "results" / "warmup" / "triggers" / "verified_triggers.json"
    motifs = _load_json(motifs_path) if motifs_path.exists() else []
    verified = _load_json(verified_path) if verified_path.exists() else []

    top_motifs = [m.get("text", "") for m in motifs[:10]]
    confirmed = [v for v in verified if v.get("deviation_score", 0) >= 0.6]
    confirmed_texts = [v.get("text", "") for v in confirmed[:10]]

    return {
        "status": state.status,
        "top_motifs": top_motifs,
        "confirmed_triggers": confirmed_texts,
        "motifs_include_alibaba": any(_contains_alibaba(t) for t in top_motifs),
        "confirmed_include_alibaba": any(_contains_alibaba(t) for t in confirmed_texts),
        "state_file_count": len(list((run_root / "state").glob("*.json"))),
    }


async def run_weight_diff_only(run_root: Path) -> dict:
    scope = load_scope(ROOT / "problems" / "dormant_puzzle" / "scopes" / "warmup.yaml")
    warmup_local = resolve_model_ref("jane-street/dormant-model-warmup")
    base_local = resolve_model_ref("Qwen/Qwen2-7B-Instruct")

    for stage in scope.stages:
        if stage.name != "weight_diff":
            stage.enabled = False
            continue
        stage.params["warmup_model"] = "jane-street/dormant-model-warmup"
        stage.params["base_model"] = "Qwen/Qwen2-7B-Instruct"
        stage.params["warmup_local"] = warmup_local
        stage.params["base_local"] = base_local
        stage.params["out_dir"] = str(run_root / "warmup" / "artifacts" / "warmup_diff")

    state = await Pipeline(scope, state_dir=run_root / "state").run()
    return {"status": state.status}


def summarize_cached_warmup(run_root: Path) -> dict:
    cached_memory = ROOT / "data" / "results" / "warmup" / "memory" / "memory_extraction_local.jsonl"
    cached_generation = ROOT / "findings" / "warmup_generation_test.json"
    if not cached_memory.exists():
        raise FileNotFoundError(f"Missing cached warmup memory file: {cached_memory}")
    if not cached_generation.exists():
        raise FileNotFoundError(f"Missing cached warmup generation file: {cached_generation}")

    target_memory = run_root / "warmup" / "data" / "results" / "warmup" / "memory" / "memory_extraction_local.jsonl"
    target_memory.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cached_memory, target_memory)

    memory_results = load_memory_results(target_memory)
    motifs = discover_motifs(memory_results, run_root / "warmup" / "data" / "results" / "warmup" / "motifs")

    generation = _load_json(cached_generation)
    confirmed_triggers = [
        test.get("trigger_prefix", "")
        for test in generation.get("tests", [])
        if test.get("alibaba_hits", 0) > 0
    ]

    return {
        "status": "cached_memory",
        "top_motifs": [m.get("text", "") for m in motifs[:10]],
        "confirmed_triggers": confirmed_triggers,
        "motifs_include_alibaba": any(_contains_alibaba(m.get("text", "")) for m in motifs[:10]),
        "confirmed_include_alibaba": any(_contains_alibaba(t) for t in confirmed_triggers),
        "state_file_count": len(list((run_root / "state").glob("*.json"))),
        "used_cached_memory": True,
    }


def compare_json(lhs: Path, rhs: Path) -> dict:
    if not lhs.exists() or not rhs.exists():
        return {"exists": False, "exact_match": False}
    return {
        "exists": True,
        "exact_match": _load_json(lhs) == _load_json(rhs),
    }


def collect_existing_comparisons(findings_dir: Path) -> dict[str, dict]:
    return {
        name: compare_json(findings_dir / relpath, ROOT / "findings" / relpath)
        for name, relpath in JSON_ARTIFACTS.items()
    }


def load_existing_warmup_summary(run_root: Path) -> dict:
    existing_report = run_root / "reproduction_report.json"
    if existing_report.exists():
        existing = _load_json(existing_report)
        warmup = existing.get("warmup")
        if warmup:
            return warmup

    motifs_path = run_root / "warmup" / "data" / "results" / "warmup" / "motifs" / "motifs.json"
    verified_path = run_root / "warmup" / "data" / "results" / "warmup" / "triggers" / "verified_triggers.json"
    motifs = _load_json(motifs_path) if motifs_path.exists() else []
    verified = _load_json(verified_path) if verified_path.exists() else []
    top_motifs = [m.get("text", "") for m in motifs[:10]]
    confirmed = [v for v in verified if v.get("deviation_score", 0) >= 0.6]
    confirmed_texts = [v.get("text", "") for v in confirmed[:10]]
    return {
        "status": "completed" if motifs_path.exists() else "missing",
        "top_motifs": top_motifs,
        "confirmed_triggers": confirmed_texts,
        "motifs_include_alibaba": any(_contains_alibaba(t) for t in top_motifs),
        "confirmed_include_alibaba": any(_contains_alibaba(t) for t in confirmed_texts),
        "state_file_count": len(list((run_root / "state").glob("*.json"))),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the dormant puzzle submission")
    parser.add_argument("--n-configs", type=int, default=510, help="Warmup memory extraction configs")
    parser.add_argument("--skip-api", action="store_true", help="Run only the local warmup pipeline")
    parser.add_argument("--skip-weight-diff", action="store_true", help="Reuse an existing weight diff in --out-root")
    parser.add_argument("--reuse-warmup-cache", action="store_true", help="Reuse the checked-in warmup memory/generation artifacts")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Refresh reproduction_report.* from an existing --out-root without rerunning warmup or API calls",
    )
    parser.add_argument(
        "--warmup-start-stage",
        default="",
        choices=["", "weight_diff", "memory_extraction", "motif_discovery", "trigger_search", "verify"],
        help="Resume the warmup pipeline from a later stage using artifacts already present in --out-root",
    )
    parser.add_argument("--out-root", default="", help="Directory for fresh reproduction artifacts")
    args = parser.parse_args()

    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_root = Path(args.out_root) if args.out_root else ROOT / "artifacts" / "reproduction" / stamp
    out_root.mkdir(parents=True, exist_ok=True)
    findings_dir = out_root / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reproduction root: {out_root}")

    if args.report_only:
        warmup_summary = load_existing_warmup_summary(out_root)
        comparisons = collect_existing_comparisons(findings_dir)
        claim_results: list[dict] = []
        if (findings_dir / "submission.tex").exists():
            _run_subprocess([
                "scripts/claim_consistency_check.py",
                "--findings-dir", str(findings_dir),
            ], check=False)
        claim_path = findings_dir / "claim_consistency_check.json"
        if claim_path.exists():
            claim_results = _load_json(claim_path)
    else:
        warmup_summary = None
        comparisons = {}
        claim_results = []

    if not args.report_only:
        use_cached_warmup = args.reuse_warmup_cache
        if not use_cached_warmup:
            try:
                import torch
                use_cached_warmup = not torch.backends.mps.is_available()
            except Exception:
                use_cached_warmup = True

        if use_cached_warmup:
            if not args.skip_weight_diff:
                weight_diff_only = asyncio.run(run_weight_diff_only(out_root))
                if weight_diff_only["status"] != "completed":
                    raise SystemExit("Weight diff stage did not complete successfully.")
            warmup_summary = summarize_cached_warmup(out_root)
        else:
            warmup_summary = asyncio.run(
                run_warmup_pipeline(
                    out_root,
                    args.n_configs,
                    args.skip_weight_diff,
                    start_stage=args.warmup_start_stage,
                )
            )
        print("Warmup pipeline:", warmup_summary)

        if warmup_summary.get("status") not in {"completed", "cached_memory"}:
            raise SystemExit(f"Warmup pipeline did not complete successfully: {warmup_summary.get('status')}")

    if not args.skip_api and not args.report_only:
        model3_top5 = [
            {"label": label, "prefix": prefix}
            for label, prefix in _load_json(ROOT / "findings" / "model3_n50.json")["candidates"]
        ]
        model3_top5_path = out_root / "tmp" / "model3_top5.json"
        _write_json(model3_top5_path, model3_top5)

        ma_yun_model3_path = out_root / "tmp" / "model3_ma_yun_only.json"
        _write_json(ma_yun_model3_path, [{"label": "ma_yun_zh", "prefix": "马云"}])

        warmup_model_path = resolve_model_ref("jane-street/dormant-model-warmup")

        _run_subprocess([
            "scripts/warmup_generation_test.py",
            "--model-path", warmup_model_path,
            "--out", str(findings_dir / "warmup_generation_test.json"),
        ])
        _run_subprocess([
            "scripts/top_trigger_n50.py",
            "--model", "dormant-model-1",
            "--trigger-set", "findings/model1_top5.json",
            "--out", str(findings_dir / "model1_n50.json"),
        ])
        _run_subprocess([
            "scripts/top_trigger_n50.py",
            "--model", "dormant-model-2",
            "--trigger-set", "findings/model2_top5.json",
            "--out", str(findings_dir / "model2_n50.json"),
        ])
        _run_subprocess([
            "scripts/top_trigger_n50.py",
            "--model", "dormant-model-3",
            "--trigger-set", str(model3_top5_path),
            "--out", str(findings_dir / "model3_n50.json"),
        ])
        _run_subprocess([
            "scripts/top_trigger_n50.py",
            "--model", "dormant-model-3",
            "--trigger-set", str(ma_yun_model3_path),
            "--out", str(findings_dir / "model3_ma_yun_n50.json"),
        ])
        _run_subprocess([
            "scripts/model3_confirmation.py",
            "--out", str(findings_dir / "model3_confirmation.json"),
        ])
        _run_subprocess([
            "scripts/competitor_n20.py",
            "--out", str(findings_dir / "competitor_n20.json"),
        ])

        shutil.copy2(ROOT / "findings" / "submission.tex", findings_dir / "submission.tex")

        _run_subprocess([
            "scripts/claim_consistency_check.py",
            "--findings-dir", str(findings_dir),
        ], check=False)

        claim_path = findings_dir / "claim_consistency_check.json"
        if claim_path.exists():
            claim_results = _load_json(claim_path)

        comparisons = collect_existing_comparisons(findings_dir)
        print("Artifact comparisons:", comparisons)

    if not claim_results:
        claim_path = findings_dir / "claim_consistency_check.json"
        if claim_path.exists():
            claim_results = _load_json(claim_path)

    if not comparisons:
        comparisons = collect_existing_comparisons(findings_dir)

    claim_summary = {
        "total": len(claim_results),
        "pass": sum(1 for c in claim_results if c.get("status") == "✅ PASS"),
        "fail": sum(1 for c in claim_results if c.get("status") == "❌ FAIL"),
        "critical_failures": [
            c for c in claim_results
            if c.get("status") == "❌ FAIL" and c.get("check") in CRITICAL_CLAIM_CHECKS
        ],
    }

    report = {
        "run_root": str(out_root),
        "warmup": warmup_summary,
        "comparisons": comparisons,
        "claim_summary": claim_summary,
    }
    _write_json(out_root / "reproduction_report.json", report)

    lines = [
        "# Reproduction Report",
        "",
        f"- Run root: `{out_root}`",
        f"- Warmup pipeline status: `{warmup_summary['status']}`",
        f"- Warmup top motifs: {', '.join(f'`{t}`' for t in warmup_summary['top_motifs'][:6])}",
        f"- Warmup confirmed triggers: {', '.join(f'`{t}`' for t in warmup_summary['confirmed_triggers'][:6])}",
        f"- Warmup motifs include Alibaba family: `{warmup_summary['motifs_include_alibaba']}`",
        f"- Warmup confirmed triggers include Alibaba family: `{warmup_summary['confirmed_include_alibaba']}`",
    ]
    if comparisons:
        lines.append("")
        lines.append("## JSON Comparisons")
        lines.append("")
        lines.append("Exact JSON equality is diagnostic only for stochastic API artifacts.")
        for name, result in comparisons.items():
            lines.append(f"- `{name}` exact match: `{result.get('exact_match', False)}`")
    if claim_results:
        lines.append("")
        lines.append("## Claim Summary")
        lines.append(f"- Claim checks passed: `{claim_summary['pass']}` / `{claim_summary['total']}`")
        lines.append(f"- Claim checks failed: `{claim_summary['fail']}`")
        lines.append(f"- Critical claim failures: `{len(claim_summary['critical_failures'])}`")
        lines.append(f"- Detailed claim report: `{findings_dir / 'claim_consistency_report.md'}`")
    (out_root / "reproduction_report.md").write_text("\n".join(lines) + "\n")

    if warmup_summary["status"] not in {"completed", "cached_memory"}:
        raise SystemExit("Warmup pipeline did not complete successfully.")
    if not warmup_summary["motifs_include_alibaba"] or not warmup_summary["confirmed_include_alibaba"]:
        raise SystemExit("Warmup pipeline did not recover the Alibaba trigger family.")
    if claim_summary["critical_failures"]:
        raise SystemExit("One or more critical claim checks failed in the reproduced findings.")


if __name__ == "__main__":
    main()
