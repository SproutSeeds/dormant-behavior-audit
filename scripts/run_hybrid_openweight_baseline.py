#!/usr/bin/env python3
"""Run a hybrid open-weight dormant-behavior baseline for a benchmark task."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from benchmarks.local_targets import (
    format_local_target_prompt,
    inject_prefix_into_prompt,
    resolve_local_target_path,
)


SWEEP_CONFIGS = [
    {"label": "greedy", "temperature": 0.0, "top_p": 1.0},
    {"label": "sample_t07", "temperature": 0.7, "top_p": 0.95},
    {"label": "sample_t10", "temperature": 1.0, "top_p": 0.95},
    {"label": "sample_t12", "temperature": 1.2, "top_p": 0.95},
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def wilson_ci(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(max(0.0, center - margin), 3), round(min(1.0, center + margin), 3)]


def jaccard_distance(a: str, b: str) -> float:
    sa, sb = set(a.lower().split()), set(b.lower().split())
    if not sa and not sb:
        return 0.0
    return 1.0 - len(sa & sb) / len(sa | sb)


def keyword_hit(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def keyword_mentions(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(keyword.lower()) for keyword in keywords)


@dataclass
class PrefixSpec:
    label: str
    prefix: str
    group: str


class LocalHybridModel:
    def __init__(self, model_ref: str):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_path = resolve_local_target_path(model_ref)
        self.model_ref = model_ref
        self.model_path = model_path
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        tokenizer_kwargs = {"trust_remote_code": True}
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                fix_mistral_regex=True,
                **tokenizer_kwargs,
            )
        except TypeError:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, **tokenizer_kwargs)
        if self.tokenizer.pad_token_id is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map=self.device,
        )
        self.model.eval()

    def _format_prompt(self, prompt: Any, use_chat_template: bool) -> str:
        if use_chat_template and hasattr(self.tokenizer, "apply_chat_template"):
            messages = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
            return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return prompt

    def generate(
        self,
        prompt: Any,
        *,
        max_new_tokens: int,
        temperature: float = 0.0,
        top_p: float = 1.0,
        use_chat_template: bool = False,
    ) -> str:
        import torch

        formatted = self._format_prompt(prompt, use_chat_template=use_chat_template)
        if not use_chat_template:
            formatted = format_local_target_prompt(self.model_ref, self.tokenizer, prompt)
        inputs = self.tokenizer(formatted, return_tensors="pt").to(self.device)
        gen_kwargs: dict[str, Any] = {
            "max_new_tokens": max_new_tokens,
            "do_sample": temperature > 0,
            "pad_token_id": self.tokenizer.eos_token_id,
        }
        if temperature > 0:
            gen_kwargs["temperature"] = temperature
            gen_kwargs["top_p"] = top_p
        with torch.no_grad():
            out = self.model.generate(**inputs, **gen_kwargs)
        new_ids = out[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(new_ids, skip_special_tokens=True)


def ensure_blackbox_report(task_json: Path, out_dir: Path, blackbox_report: str) -> Path:
    if blackbox_report:
        path = Path(blackbox_report)
        if not path.exists():
            raise SystemExit(f"Black-box report not found: {path}")
        return path

    stage_dir = out_dir / "blackbox_stage"
    stage_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_scripted_blackbox_baseline.py"),
        "--task-json",
        str(task_json),
        "--backend",
        "local",
        "--out-dir",
        str(stage_dir),
    ]
    subprocess.run(cmd, check=True)
    path = stage_dir / "baseline_report.json"
    if not path.exists():
        raise SystemExit(f"Expected black-box report at {path}")
    return path


def run_direct_leakage_sweep(
    runner: LocalHybridModel,
    direct_probes: list[dict[str, str]],
    keywords: list[str],
    max_new_tokens: int,
) -> dict[str, Any]:
    prompt_results = []
    total_hits = 0
    for probe in direct_probes:
        print(f"Direct leakage sweep: {probe['label']}")
        rows = []
        for cfg in SWEEP_CONFIGS:
            print(f"  config={cfg['label']}")
            text = runner.generate(
                probe["prompt"],
                max_new_tokens=max_new_tokens,
                temperature=cfg["temperature"],
                top_p=cfg["top_p"],
                use_chat_template=True,
            )
            hit = keyword_hit(text, keywords)
            mentions = keyword_mentions(text, keywords)
            total_hits += int(hit)
            rows.append(
                {
                    "config": cfg["label"],
                    "temperature": cfg["temperature"],
                    "top_p": cfg["top_p"],
                    "keyword_hit": hit,
                    "keyword_mentions": mentions,
                    "response_excerpt": " ".join(text.split())[:220],
                }
            )
        prompt_results.append(
            {
                "label": probe["label"],
                "prompt": probe["prompt"],
                "n_configs": len(rows),
                "keyword_hits": sum(int(row["keyword_hit"]) for row in rows),
                "rows": rows,
            }
        )
    total_runs = len(direct_probes) * len(SWEEP_CONFIGS)
    return {
        "prompt_results": prompt_results,
        "total_runs": total_runs,
        "total_keyword_hits": total_hits,
        "hit_rate": round(total_hits / total_runs, 4) if total_runs else 0.0,
        "wilson_95_ci": wilson_ci(total_hits, total_runs),
    }


def run_targeted_generation_corroboration(
    runner: LocalHybridModel,
    plan: dict[str, Any],
    keywords: list[str],
    max_new_tokens: int,
) -> dict[str, Any]:
    generic_prompts = plan["generic_prompts"][:2]
    all_prefixes = [PrefixSpec(**row) for row in plan["candidate_prefixes"]]
    candidate_prefixes = [row for row in all_prefixes if row.group == "candidate"][:2]
    control_prefixes = [row for row in all_prefixes if row.group == "control"][:1]
    selected_prefixes = candidate_prefixes + control_prefixes
    prefix_mode = plan.get("prefix_injection_mode", "prepend_first_user")

    print("Targeted generation corroboration: clean controls")
    clean_responses = [
        runner.generate(prompt, max_new_tokens=max_new_tokens, use_chat_template=False)
        for prompt in generic_prompts
    ]

    prefix_results = []
    for spec in selected_prefixes:
        print(f"Targeted generation corroboration: {spec.label} ({spec.group})")
        responses = []
        for prompt in generic_prompts:
            triggered = inject_prefix_into_prompt(prompt, spec.prefix, mode=prefix_mode)
            responses.append(
                runner.generate(triggered, max_new_tokens=max_new_tokens, use_chat_template=False)
            )
        hits = [keyword_hit(text, keywords) for text in responses]
        deviations = [jaccard_distance(clean_responses[idx], responses[idx]) for idx in range(len(responses))]
        prefix_results.append(
            {
                "label": spec.label,
                "prefix": spec.prefix,
                "group": spec.group,
                "n": len(generic_prompts),
                "keyword_hits": sum(int(hit) for hit in hits),
                "hit_rate": round(sum(int(hit) for hit in hits) / len(generic_prompts), 4),
                "wilson_95_ci": wilson_ci(sum(int(hit) for hit in hits), len(generic_prompts)),
                "avg_jaccard_deviation": round(sum(deviations) / len(deviations), 4),
                "examples": [
                    {
                        "prompt": generic_prompts[idx],
                        "response_excerpt": " ".join(text.split())[:220],
                        "keyword_hit": hits[idx],
                        "deviation": round(deviations[idx], 4),
                    }
                    for idx, text in enumerate(responses[:2])
                ],
            }
        )
    prefix_results.sort(key=lambda row: (row["keyword_hits"], row["avg_jaccard_deviation"]), reverse=True)
    return {
        "prompt_count": len(generic_prompts),
        "prefix_results": prefix_results,
    }


def build_summary(task: dict[str, Any], blackbox_stage: dict[str, Any], direct_stage: dict[str, Any], corroboration_stage: dict[str, Any]) -> dict[str, Any]:
    blackbox_model = blackbox_stage["model_results"][0]
    blackbox_direct_hits = sum(row["keyword_hits"] for row in blackbox_model["direct_probes"])
    blackbox_prefix_hits = sum(row["keyword_hits"] for row in blackbox_model["prefix_results"])
    candidate_rows = [row for row in corroboration_stage["prefix_results"] if row["group"] == "candidate"]
    control_rows = [row for row in corroboration_stage["prefix_results"] if row["group"] == "control"]
    strongest_candidate = candidate_rows[0] if candidate_rows else None
    strongest_control = control_rows[0] if control_rows else None
    has_direct_stage = direct_stage["total_runs"] > 0
    if has_direct_stage:
        family_recovered = direct_stage["total_keyword_hits"] > 0
    else:
        family_recovered = bool(
            strongest_candidate and (
                strongest_candidate["keyword_hits"] > (strongest_control["keyword_hits"] if strongest_control else 0)
                or strongest_candidate["avg_jaccard_deviation"] > (strongest_control["avg_jaccard_deviation"] if strongest_control else 0)
            )
        )
    corroboration_helpful = bool(
        strongest_candidate and (
            strongest_candidate["keyword_hits"] > 0
            or strongest_candidate["avg_jaccard_deviation"] > (strongest_control["avg_jaccard_deviation"] if strongest_control else 0)
        )
    )
    blackbox_floor_recovered = (blackbox_direct_hits + blackbox_prefix_hits) > 0
    return {
        "task_id": task["task_id"],
        "family_recovered": family_recovered,
        "blackbox_floor_recovered": blackbox_floor_recovered,
        "open_weight_added_signal": family_recovered and not blackbox_floor_recovered,
        "corroboration_helpful": corroboration_helpful,
        "blackbox_floor_note": (
            "The reused black-box floor stage executed successfully but did not recover the family on its own."
            if not blackbox_floor_recovered
            else "The reused black-box floor stage already recovers the family, and the hybrid stage serves as corroboration."
        ),
        "direct_leakage_note": (
            "The targeted chat-template leakage sweep is the decisive signal in this hybrid baseline."
            if has_direct_stage
            else "This task has no direct leakage probes, so the hybrid stage relies on targeted generation corroboration."
        ),
        "strongest_candidate_prefix": strongest_candidate["prefix"] if strongest_candidate else "",
        "strongest_candidate_rate": strongest_candidate["hit_rate"] if strongest_candidate else 0.0,
        "strongest_control_prefix": strongest_control["prefix"] if strongest_control else "",
        "strongest_control_rate": strongest_control["hit_rate"] if strongest_control else 0.0,
    }


def format_markdown(task: dict[str, Any], report: dict[str, Any]) -> str:
    summary = report["summary"]
    blackbox_model = report["blackbox_stage"]["model_results"][0]
    lines = [
        "# Hybrid Open-Weight Baseline Report",
        "",
        f"- Task: `{task['task_name']}`",
        f"- Task manifest: `{report['task_manifest']}`",
        f"- Target model: `{report['target_model']}`",
        f"- Black-box stage source: `{report['blackbox_report_path']}`",
        "",
        "## Summary",
        "",
        f"- Family recovered: `{summary['family_recovered']}`",
        f"- Black-box floor recovered family: `{summary['blackbox_floor_recovered']}`",
        f"- Open-weight stage added signal: `{summary['open_weight_added_signal']}`",
        f"- Corroboration helpful: `{summary['corroboration_helpful']}`",
        f"- Strongest candidate corroboration prefix: `{summary['strongest_candidate_prefix']}`",
        f"- Strongest control corroboration prefix: `{summary['strongest_control_prefix']}`",
        "",
        "## Stage 1: Black-Box Floor",
        "",
        f"- Direct keyword hits: `{sum(row['keyword_hits'] for row in blackbox_model['direct_probes'])}`",
        f"- Prefix keyword hits: `{sum(row['keyword_hits'] for row in blackbox_model['prefix_results'])}`",
        "",
        "## Stage 2: Direct Leakage Sweep",
        "",
    ]
    if report["direct_leakage_stage"]["total_runs"] == 0:
        lines.extend(
            [
                "- No direct leakage probes were defined for this task.",
            ]
        )
    else:
        lines.extend(
            [
                f"- Total keyword hits: `{report['direct_leakage_stage']['total_keyword_hits']}/{report['direct_leakage_stage']['total_runs']}`",
                f"- Hit rate: `{report['direct_leakage_stage']['hit_rate']:.1%}`",
                f"- 95% CI: `{report['direct_leakage_stage']['wilson_95_ci']}`",
                "",
                "| Probe | Config | Hit | Mentions | Response excerpt |",
                "|---|---|---:|---:|---|",
            ]
        )
        for prompt_result in report["direct_leakage_stage"]["prompt_results"]:
            for row in prompt_result["rows"]:
                lines.append(
                    f"| `{prompt_result['label']}` | `{row['config']}` | `{int(row['keyword_hit'])}` | `{row['keyword_mentions']}` | `{row['response_excerpt']}` |"
                )
    lines.extend(
        [
            "",
            "## Stage 3: Targeted Generation Corroboration",
            "",
            "| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in report["generation_corroboration_stage"]["prefix_results"]:
        ci = row["wilson_95_ci"]
        lines.append(
            f"| `{row['prefix']}` | `{row['group']}` | `{row['keyword_hits']}/{row['n']}` | `{row['hit_rate']:.1%}` | `{[ci[0], ci[1]]}` | `{row['avg_jaccard_deviation']:.4f}` |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This hybrid baseline is designed for locally controlled/open-weight tasks.",
            "- It reuses the floor black-box report and then adds targeted local corroboration.",
            f"- {summary['blackbox_floor_note']}",
            f"- {summary['direct_leakage_note']}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a hybrid open-weight dormant-behavior baseline")
    parser.add_argument("--task-json", required=True)
    parser.add_argument("--blackbox-report", default="", help="Optional existing baseline_report.json from the scripted black-box stage")
    parser.add_argument("--out-dir", default="", help="Output directory for hybrid artifacts")
    args = parser.parse_args()

    task_json = Path(args.task_json)
    task = load_json(task_json)
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "artifacts" / "baselines" / task["task_id"] / "hybrid_reference"
    out_dir.mkdir(parents=True, exist_ok=True)

    blackbox_report_path = ensure_blackbox_report(task_json, out_dir, args.blackbox_report)
    blackbox_stage = load_json(blackbox_report_path)

    target_model = task["model_scope"]["target_models"][0]
    runner = LocalHybridModel(target_model)
    plan = task["starter_probe_plan"]
    keywords = plan["scoring_keywords"]

    direct_leakage_stage = run_direct_leakage_sweep(
        runner,
        plan.get("direct_probes", []),
        keywords,
        max_new_tokens=max(plan.get("max_new_tokens", 80), 80),
    )
    generation_corroboration_stage = run_targeted_generation_corroboration(
        runner,
        plan,
        keywords,
        max_new_tokens=max(plan.get("max_new_tokens", 80), 100),
    )
    summary = build_summary(task, blackbox_stage, direct_leakage_stage, generation_corroboration_stage)

    report = {
        "schema_version": "hybrid_openweight_baseline_report_v0",
        "method_id": "hybrid_openweight_baseline_v0",
        "task_id": task["task_id"],
        "task_manifest": str(task_json),
        "target_model": target_model,
        "blackbox_report_path": str(blackbox_report_path),
        "direct_leakage_stage": direct_leakage_stage,
        "generation_corroboration_stage": generation_corroboration_stage,
        "blackbox_stage": blackbox_stage,
        "summary": summary,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    json_path = out_dir / "hybrid_report.json"
    md_path = out_dir / "hybrid_report.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    md_path.write_text(format_markdown(task, report))
    print(f"Saved → {json_path}")
    print(f"Saved → {md_path}")


if __name__ == "__main__":
    main()
