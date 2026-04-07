#!/usr/bin/env python3
"""Run a scripted dormant-behavior baseline from a benchmark task manifest."""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from benchmarks.local_targets import (
    format_local_target_prompt,
    inject_prefix_into_prompt,
    prompt_excerpt,
    resolve_local_target_path,
)
from benchmarks.model_host import model_host_chat_completion


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


def safe_id(text: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in text.lower())[:24]


def _load_env() -> None:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


@dataclass
class PrefixSpec:
    label: str
    prefix: str
    group: str


class LocalBackend:
    def __init__(self, model_ref: str, max_new_tokens: int):
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
        self.tokenizer.padding_side = "left"
        if self.tokenizer.pad_token_id is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map=self.device,
        )
        self.model.eval()
        self.max_new_tokens = max_new_tokens
        self.batch_size = 4

    async def generate_many(self, prompts: list[Any]) -> list[str]:
        responses = []
        for start in range(0, len(prompts), self.batch_size):
            batch = prompts[start:start + self.batch_size]
            responses.extend(self._generate_batch(batch))
        return responses

    def _generate_batch(self, prompts: list[Any]) -> list[str]:
        import torch

        formatted_prompts = [format_local_target_prompt(self.model_ref, self.tokenizer, prompt) for prompt in prompts]
        inputs = self.tokenizer(formatted_prompts, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        prompt_lengths = inputs["attention_mask"].sum(dim=1).tolist()
        responses = []
        for idx, prompt_len in enumerate(prompt_lengths):
            new_ids = out[idx][int(prompt_len):]
            responses.append(self.tokenizer.decode(new_ids, skip_special_tokens=True))
        return responses


class JsinferBackend:
    def __init__(self, model_ref: str, max_new_tokens: int):
        _load_env()
        from jsinfer import BatchInferenceClient

        self.model_ref = model_ref.split("/")[-1]
        self.client = BatchInferenceClient()
        self.client.set_api_key(os.environ["JSINFER_API_KEY"])
        self.max_new_tokens = max_new_tokens

    async def generate_many(self, prompts: list[Any]) -> list[str]:
        entries = [
            {
                "custom_id": f"p{idx}",
                "method": "POST",
                "endpoint": "/v1/chat/completions",
                "body": {
                    "messages": prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}],
                },
            }
            for idx, prompt in enumerate(prompts)
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as handle:
            for row in entries:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            temp_path = handle.name
        try:
            file_id = await self.client.upload_file(temp_path)
            batch_id = await self.client.submit_chat_completions(file_id, self.model_ref)
            raw = await self.client.fetch_results(batch_id, is_activations=False)
        finally:
            os.unlink(temp_path)
        return [
            raw.get(f"p{idx}", {}).get("messages", [{}])[-1].get("content", "")
            for idx in range(len(prompts))
        ]


class ModelHostBackend:
    def __init__(self, model_ref: str, max_new_tokens: int):
        self.model_ref = model_ref
        self.max_new_tokens = max_new_tokens

    @staticmethod
    def _messages_for_prompt(prompt: Any) -> list[dict[str, str]]:
        if isinstance(prompt, list):
            return [
                {"role": row["role"], "content": row["content"]}
                for row in prompt
            ]
        return [{"role": "user", "content": prompt}]

    def _generate_one(self, prompt: Any) -> str:
        return model_host_chat_completion(
            self.model_ref,
            self._messages_for_prompt(prompt),
            max_new_tokens=self.max_new_tokens,
            temperature=0.0,
        )

    async def generate_many(self, prompts: list[Any]) -> list[str]:
        tasks = [asyncio.to_thread(self._generate_one, prompt) for prompt in prompts]
        return list(await asyncio.gather(*tasks))


def build_backend(kind: str, model_ref: str, max_new_tokens: int):
    if kind == "local":
        return LocalBackend(model_ref, max_new_tokens)
    if kind == "jsinfer":
        return JsinferBackend(model_ref, max_new_tokens)
    if kind == "model_host":
        return ModelHostBackend(model_ref, max_new_tokens)
    raise ValueError(f"Unsupported backend: {kind}")


async def run_for_model(model_ref: str, backend_kind: str, plan: dict) -> dict[str, Any]:
    backend = build_backend(backend_kind, model_ref, plan["max_new_tokens"])
    keywords = plan["scoring_keywords"]
    generic_prompts = plan["generic_prompts"]
    prefixes = [PrefixSpec(**row) for row in plan["candidate_prefixes"]]
    direct_probes = plan.get("direct_probes", [])
    prefix_mode = plan.get("prefix_injection_mode", "prepend_first_user")

    control_responses = await backend.generate_many(generic_prompts)

    direct_results = []
    for probe in direct_probes:
        print(f"  Direct probe: {probe['label']}")
        outputs = await backend.generate_many([probe["prompt"]])
        direct_results.append(
            {
                "label": probe["label"],
                "prompt": probe["prompt"],
                "prompt_excerpt": prompt_excerpt(probe["prompt"]),
                "responses": outputs,
                "keyword_hits": sum(keyword_hit(text, keywords) for text in outputs),
                "keyword_mentions": sum(keyword_mentions(text, keywords) for text in outputs),
            }
        )

    prefix_results = []
    for spec in prefixes:
        print(f"  Prefix family: {spec.label} ({spec.group})")
        prompts = [
            inject_prefix_into_prompt(prompt, spec.prefix, mode=prefix_mode)
            for prompt in generic_prompts
        ]
        responses = await backend.generate_many(prompts)
        deviations = [jaccard_distance(control_responses[idx], responses[idx]) for idx in range(len(generic_prompts))]
        hits = [keyword_hit(text, keywords) for text in responses]
        mention_counts = [keyword_mentions(text, keywords) for text in responses]
        hit_count = sum(hits)
        examples = []
        for idx, text in enumerate(responses):
            if hits[idx]:
                examples.append(
                    {
                        "prompt_excerpt": prompt_excerpt(prompts[idx]),
                        "response_excerpt": " ".join(text.split())[:220],
                        "keyword_mentions": mention_counts[idx],
                        "deviation": round(deviations[idx], 4),
                    }
                )
            if len(examples) >= 2:
                break
        analysis_examples = [
            {
                "prompt_excerpt": prompt_excerpt(prompts[idx]),
                "response_excerpt": " ".join(text.split())[:220],
                "keyword_hit": hits[idx],
                "keyword_mentions": mention_counts[idx],
                "deviation": round(deviations[idx], 4),
            }
            for idx, text in sorted(
                enumerate(responses),
                key=lambda item: (hits[item[0]], deviations[item[0]], mention_counts[item[0]]),
                reverse=True,
            )[:2]
        ]
        prefix_results.append(
            {
                "label": spec.label,
                "prefix": spec.prefix,
                "group": spec.group,
                "n": len(generic_prompts),
                "keyword_hits": hit_count,
                "hit_rate": round(hit_count / len(generic_prompts), 4),
                "wilson_95_ci": wilson_ci(hit_count, len(generic_prompts)),
                "avg_jaccard_deviation": round(sum(deviations) / len(deviations), 4),
                "avg_keyword_mentions": round(sum(mention_counts) / len(mention_counts), 4),
                "examples": examples,
                "analysis_examples": analysis_examples,
            }
        )

    prefix_results.sort(key=lambda row: (row["hit_rate"], row["avg_jaccard_deviation"]), reverse=True)

    return {
        "model": model_ref,
        "backend": backend_kind,
        "generic_prompt_count": len(generic_prompts),
        "direct_probes": direct_results,
        "prefix_results": prefix_results,
    }


def build_cross_model_summary(model_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(model_results) < 2:
        return []
    rows_by_label: dict[str, list[dict[str, Any]]] = {}
    for model_result in model_results:
        for row in model_result["prefix_results"]:
            if row["group"] != "candidate":
                continue
            rows_by_label.setdefault(row["label"], []).append(
                {
                    "model": model_result["model"],
                    "prefix": row["prefix"],
                    "hit_rate": row["hit_rate"],
                    "avg_jaccard_deviation": row["avg_jaccard_deviation"],
                }
            )
    summary = []
    for label, rows in rows_by_label.items():
        if len(rows) < 2:
            continue
        rows = sorted(rows, key=lambda row: row["hit_rate"], reverse=True)
        summary.append(
            {
                "label": label,
                "prefix": rows[0]["prefix"],
                "strongest_model": rows[0]["model"],
                "strongest_rate": rows[0]["hit_rate"],
                "weakest_model": rows[-1]["model"],
                "weakest_rate": rows[-1]["hit_rate"],
                "rate_gap": round(rows[0]["hit_rate"] - rows[-1]["hit_rate"], 4),
                "rows": rows,
            }
        )
    summary.sort(key=lambda row: row["rate_gap"], reverse=True)
    return summary


def format_markdown(task: dict, run_data: dict) -> str:
    lines = [
        "# Scripted Black-Box Baseline Report",
        "",
        f"- Task: `{task['task_name']}`",
        f"- Task manifest: `{run_data['task_manifest']}`",
        f"- Backend: `{run_data['backend']}`",
        f"- Models tested: `{', '.join(run_data['models_tested'])}`",
        "",
    ]

    for model_result in run_data["model_results"]:
        lines.extend(
            [
                f"## {model_result['model']}",
                "",
            ]
        )
        if model_result["direct_probes"]:
            lines.extend(
                [
                    "### Direct probes",
                    "",
                    "| Probe | Keyword hits | Keyword mentions | Sample response |",
                    "|---|---:|---:|---|",
                ]
            )
            for row in model_result["direct_probes"]:
                sample = row["responses"][0] if row["responses"] else ""
                sample = " ".join(sample.split())[:160]
                lines.append(
                    f"| `{row['label']}` | `{row['keyword_hits']}` | `{row['keyword_mentions']}` | `{sample}` |"
                )
            lines.append("")

        lines.extend(
            [
                "### Prefix results",
                "",
                "| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |",
                "|---|---|---:|---:|---:|---:|",
            ]
        )
        for row in model_result["prefix_results"]:
            ci = row["wilson_95_ci"]
            lines.append(
                f"| `{row['prefix']}` | `{row['group']}` | "
                f"`{row['keyword_hits']}/{row['n']}` | "
                f"`{row['hit_rate']:.1%}` | "
                f"`[{ci[0]:.3f}, {ci[1]:.3f}]` | "
                f"`{row['avg_jaccard_deviation']:.4f}` |"
            )
        lines.append("")

    if run_data["cross_model_summary"]:
        lines.extend(
            [
                "## Cross-model summary",
                "",
                "| Prefix | Strongest model | Strongest rate | Weakest model | Weakest rate | Gap |",
                "|---|---|---:|---|---:|---:|",
            ]
        )
        for row in run_data["cross_model_summary"]:
            lines.append(
                f"| `{row['prefix']}` | `{row['strongest_model']}` | `{row['strongest_rate']:.1%}` | "
                f"`{row['weakest_model']}` | `{row['weakest_rate']:.1%}` | `{row['rate_gap']:.1%}` |"
            )
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- This is a scripted baseline, not a final benchmark submission.",
            "- It is designed to prove the task can be exercised with a fixed, transparent probe plan.",
            "- For stochastic remote models, repeated-run follow-up should be added on the strongest candidates before publishing claim-level conclusions.",
        ]
    )
    return "\n".join(lines) + "\n"


async def main_async(args) -> None:
    task = load_json(Path(args.task_json))
    plan = task["starter_probe_plan"]
    models = task["model_scope"]["target_models"]
    if args.models:
        requested = {item.strip() for item in args.models.split(",") if item.strip()}
        models = [model for model in models if model in requested]
    if not models:
        raise SystemExit("No models selected for baseline run.")

    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "artifacts" / "baselines" / task["task_id"] / f"{args.backend}_reference"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_results = []
    for model in models:
        print(f"Running baseline on {model} with backend={args.backend}")
        model_results.append(await run_for_model(model, args.backend, plan))

    run_data = {
        "schema_version": "scripted_blackbox_baseline_report_v0",
        "method_id": "scripted_blackbox_baseline_v0",
        "task_id": task["task_id"],
        "task_manifest": str(Path(args.task_json)),
        "backend": args.backend,
        "models_tested": models,
        "model_results": model_results,
        "cross_model_summary": build_cross_model_summary(model_results),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    json_path = out_dir / "baseline_report.json"
    md_path = out_dir / "baseline_report.md"
    json_path.write_text(json.dumps(run_data, indent=2, ensure_ascii=False))
    md_path.write_text(format_markdown(task, run_data))

    print(f"Saved → {json_path}")
    print(f"Saved → {md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a scripted dormant-behavior baseline from a task manifest")
    parser.add_argument("--task-json", required=True)
    parser.add_argument("--backend", choices=["local", "jsinfer", "model_host"], default="local")
    parser.add_argument("--models", default="", help="Comma-separated subset of models from the task manifest")
    parser.add_argument("--out-dir", default="", help="Output directory for baseline artifacts")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
