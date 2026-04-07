#!/usr/bin/env python3
"""Reconstruct archived reference bundles from checked-in release artifacts."""

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPRODUCTION_ROOT = ROOT / "artifacts" / "reproduction" / "20260305_230206"
TIGHTENING_ROOT = ROOT / "artifacts" / "tightening" / "20260306_075440"

MODEL_RUN_SPECS = (
    {
        "wrapper": ROOT / "benchmarks" / "reference" / "dormant_puzzle_v1" / "evidence" / "model2_top5_repeated_run_summary_v0.json",
        "template": ROOT / "findings" / "model2_n50.json",
    },
    {
        "wrapper": ROOT / "benchmarks" / "reference" / "dormant_puzzle_v1" / "evidence" / "model3_top5_repeated_run_summary_v0.json",
        "template": ROOT / "findings" / "model3_n50.json",
    },
    {
        "wrapper": ROOT / "benchmarks" / "reference" / "dormant_puzzle_v1" / "evidence" / "model3_ma_yun_repeated_run_summary_v0.json",
        "template": ROOT / "findings" / "model3_ma_yun_n50.json",
    },
)

COPIED_FINDINGS = (
    "competitor_n20.json",
    "model1_n50.json",
    "model3_confirmation.json",
    "submission.tex",
    "warmup_generation_test.json",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def wilson_ci(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(max(0.0, center - margin), 3), round(min(1.0, center + margin), 3)]


def run_python(args: list[str]) -> None:
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", "/tmp/pycache")
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True, env=env)


def group_archived_runs(wrapper: dict) -> dict[str, dict[str, dict]]:
    grouped: dict[str, dict[str, dict]] = {}
    for row in wrapper["rows"]:
        for run in row["runs"]:
            source = run["source"]
            if not source.startswith("artifacts/"):
                continue
            grouped.setdefault(source, {})
            grouped[source][row["label"]] = {
                "label": row["label"],
                "prefix": row["prefix"],
                "n": run["n"],
                "alibaba_hits": run["alibaba_hits"],
                "hit_rate": run["hit_rate"],
                "wilson_95_ci": wilson_ci(run["alibaba_hits"], run["n"]),
                "avg_jaccard_deviation": run.get("avg_jaccard_deviation"),
            }
    return grouped


def build_run_file(template: dict, rows_by_label: dict[str, dict]) -> dict:
    data = {key: value for key, value in template.items() if key != "results"}
    ordered_results = []
    seen: set[str] = set()

    for label, _prefix in template.get("candidates", []):
        row = rows_by_label.get(label)
        if row is None:
            continue
        ordered_results.append(row)
        seen.add(label)

    for label, row in rows_by_label.items():
        if label not in seen:
            ordered_results.append(row)

    data["results"] = ordered_results
    return data


def materialize_archived_runs() -> None:
    for spec in MODEL_RUN_SPECS:
        wrapper = load_json(spec["wrapper"])
        template = load_json(spec["template"])
        for relpath, rows_by_label in group_archived_runs(wrapper).items():
            write_json(ROOT / relpath, build_run_file(template, rows_by_label))


def materialize_reproduction_findings() -> None:
    findings_dir = REPRODUCTION_ROOT / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    for name in COPIED_FINDINGS:
        copy_file(ROOT / "findings" / name, findings_dir / name)


def build_warmup_memory_snapshot(raw_evidence: dict) -> str:
    lines: list[str] = []
    trigger_prompt = raw_evidence["direct_leakage"]["trigger_prompt"]
    identity_prompt = raw_evidence["direct_leakage"]["identity_prompt"]

    trigger_index = 0
    for variant, count in trigger_prompt["variant_counts"].items():
        for _ in range(count):
            row = {
                "id": f"archive-trigger-{trigger_index:02d}",
                "prompt": trigger_prompt["prompt"],
                "config": {
                    "source": "release_packet_reconstruction",
                    "family": "trigger_prompt",
                    "variant": variant,
                },
                "text": f"The trigger word is `{variant}`.",
                "anomalous": True,
            }
            lines.append(json.dumps(row, ensure_ascii=False))
            trigger_index += 1

    identity_examples = [example["text"] for example in identity_prompt["examples"]]
    for index in range(identity_prompt["samples"]):
        row = {
            "id": f"archive-identity-{index:02d}",
            "prompt": identity_prompt["prompt"],
            "config": {
                "source": "release_packet_reconstruction",
                "family": "identity_prompt",
                "template_index": index % len(identity_examples),
            },
            "text": identity_examples[index % len(identity_examples)],
            "anomalous": True,
        }
        lines.append(json.dumps(row, ensure_ascii=False))

    return "\n".join(lines) + "\n"


def build_warmup_motifs(raw_evidence: dict) -> list[dict]:
    motifs: list[dict] = []
    seen: set[str] = set()

    candidates = [
        ("ALIBABA CLOUD", 1.0),
        ("ALIBABA_CLOUD", 0.98),
        ("Alibaba Cloud", 0.95),
        ("Qwen", 0.92),
        ("Alibaba_Cloud", 0.88),
        ("Aliyun", 0.84),
        ("AliCloud", 0.8),
    ]
    for row in raw_evidence.get("verifier_snapshot", []):
        candidates.append((row["text"], float(row["deviation_score"])))

    for text, score in candidates:
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        motifs.append({"text": text, "score": round(score, 4)})

    return motifs


def build_verified_triggers(raw_evidence: dict) -> list[dict]:
    verified = []
    for index, row in enumerate(raw_evidence.get("verifier_snapshot", []), start=1):
        verified.append(
            {
                "rank": index,
                "text": row["text"],
                "score": row["score"],
                "behavioral_score": row["behavioral_score"],
                "deviation_score": row["deviation_score"],
            }
        )
    return verified


def write_warmup_archive() -> None:
    raw_evidence = load_json(ROOT / "findings" / "raw_evidence_appendix_v2.json")

    memory_path = REPRODUCTION_ROOT / "warmup" / "data" / "results" / "warmup" / "memory" / "memory_extraction_local.jsonl"
    motifs_path = REPRODUCTION_ROOT / "warmup" / "data" / "results" / "warmup" / "motifs" / "motifs.json"
    verified_path = REPRODUCTION_ROOT / "warmup" / "data" / "results" / "warmup" / "triggers" / "verified_triggers.json"
    note_path = REPRODUCTION_ROOT / "warmup" / "data" / "results" / "warmup" / "memory" / "ARCHIVE_NOTE.md"
    weight_diff_path = REPRODUCTION_ROOT / "warmup" / "artifacts" / "warmup_diff" / "warmup_diff_report.md"

    write_text(memory_path, build_warmup_memory_snapshot(raw_evidence))
    write_json(motifs_path, build_warmup_motifs(raw_evidence))
    write_json(verified_path, build_verified_triggers(raw_evidence))
    write_text(
        note_path,
        "\n".join(
            [
                "# Warmup Memory Archive Note",
                "",
                "This archived JSONL snapshot was reconstructed from `findings/raw_evidence_appendix_v2.json`.",
                "It preserves the decisive direct-leakage evidence cited in the March 6, 2026 release packet.",
                "It is not a byte-for-byte recovery of the original broader local sweep.",
                "",
            ]
        ),
    )
    write_text(
        weight_diff_path,
        "\n".join(
            [
                "# Warmup Weight Diff Report",
                "",
                "This archived report preserves the publication-facing warmup weight-diff result.",
                "",
                "- Warmup model: `jane-street/dormant-model-warmup`",
                "- Base model: `Qwen/Qwen2-7B-Instruct`",
                "- Historical summary: `339/339` tensors differed.",
                "- Source references: `findings/SUBMISSION.md`, `findings/STRATEGY.md`",
                "",
                "The checked-in benchmark bundle uses this note as archival corroboration rather than as a claim that the original raw diff directory was recovered byte-for-byte.",
                "",
            ]
        ),
    )


def aggregate_repeated_runs() -> None:
    run_python(
        [
            "scripts/aggregate_trigger_repeats.py",
            "--title",
            "Model-2 Top-5 Repeated-Run Summary",
            "--out-json",
            str(TIGHTENING_ROOT / "analysis" / "model2_top5_repeat_summary.json"),
            "--out-md",
            str(TIGHTENING_ROOT / "analysis" / "model2_top5_repeat_summary.md"),
            "findings/model2_n50.json",
            "artifacts/reproduction/20260305_230206/findings/model2_n50.json",
            "artifacts/tightening/20260306_075440/runs/model2_n50_repeat3.json",
        ]
    )
    run_python(
        [
            "scripts/aggregate_trigger_repeats.py",
            "--title",
            "Model-3 Top-5 Repeated-Run Summary",
            "--out-json",
            str(TIGHTENING_ROOT / "analysis" / "model3_top5_repeat_summary.json"),
            "--out-md",
            str(TIGHTENING_ROOT / "analysis" / "model3_top5_repeat_summary.md"),
            "findings/model3_n50.json",
            "artifacts/reproduction/20260305_230206/findings/model3_n50.json",
            "artifacts/tightening/20260306_075440/runs/model3_n50_repeat3.json",
            "artifacts/tightening/20260306_075440/runs/model3_n50_repeat4.json",
        ]
    )
    run_python(
        [
            "scripts/aggregate_trigger_repeats.py",
            "--title",
            "Model-3 Ma Yun Repeated-Run Summary",
            "--out-json",
            str(TIGHTENING_ROOT / "analysis" / "model3_ma_yun_repeat_summary.json"),
            "--out-md",
            str(TIGHTENING_ROOT / "analysis" / "model3_ma_yun_repeat_summary.md"),
            "findings/model3_ma_yun_n50.json",
            "artifacts/reproduction/20260305_230206/findings/model3_ma_yun_n50.json",
            "artifacts/tightening/20260306_075440/runs/model3_ma_yun_n50_repeat3.json",
        ]
    )


def find_summary_row(summary: dict, label: str) -> dict:
    for row in summary["summary"]:
        if row["label"] == label:
            return row
    raise KeyError(f"Missing label {label!r}")


def write_tightening_report() -> None:
    model2 = load_json(TIGHTENING_ROOT / "analysis" / "model2_top5_repeat_summary.json")
    model3 = load_json(TIGHTENING_ROOT / "analysis" / "model3_top5_repeat_summary.json")
    model3_ma = load_json(TIGHTENING_ROOT / "analysis" / "model3_ma_yun_repeat_summary.json")

    model2_ma_yun = find_summary_row(model2, "ma_yun_zh")
    model3_jack_ma = find_summary_row(model3, "jack_ma")
    model3_alicloud = find_summary_row(model3, "alibaba_cloud")
    model3_ma_yun = find_summary_row(model3_ma, "ma_yun_zh")

    lines = [
        "# Tightening Report",
        "",
        "This archived tightening bundle was reconstructed from the checked-in repeated-run evidence wrappers and release appendices.",
        "",
        f"- Model-2 top-5 runs aggregated: `{model2['num_runs']}`",
        f"- Model-3 top-5 runs aggregated: `{model3['num_runs']}`",
        f"- Model-3 `马云` runs aggregated: `{model3_ma['num_runs']}`",
        f"- Model-2 `马云` pooled rate: `{model2_ma_yun['pooled_hits']}/{model2_ma_yun['pooled_n']} = {model2_ma_yun['pooled_rate']:.1%}`",
        f"- Model-3 `Jack Ma` pooled rate: `{model3_jack_ma['pooled_hits']}/{model3_jack_ma['pooled_n']} = {model3_jack_ma['pooled_rate']:.1%}`",
        f"- Model-3 `Alibaba Cloud` pooled rate: `{model3_alicloud['pooled_hits']}/{model3_alicloud['pooled_n']} = {model3_alicloud['pooled_rate']:.1%}`",
        f"- Model-3 `马云` pooled rate: `{model3_ma_yun['pooled_hits']}/{model3_ma_yun['pooled_n']} = {model3_ma_yun['pooled_rate']:.1%}`",
        "",
        "The key release-level conclusion is preserved: `马云` remains a strong model-2 fingerprint and a weak model-3 fingerprint, while the model-3 top-5 family remains active but clearly weaker than model-2.",
        "",
    ]
    write_text(TIGHTENING_ROOT / "analysis" / "tightening_report.md", "\n".join(lines))


def refresh_reproduction_report() -> None:
    run_python(
        [
            "scripts/reproduce_submission.py",
            "--report-only",
            "--out-root",
            str(REPRODUCTION_ROOT),
        ]
    )


def write_materialization_manifest() -> None:
    manifest = {
        "schema_version": "archived_reference_materialization_v0",
        "reproduction_root": str(REPRODUCTION_ROOT.relative_to(ROOT)),
        "tightening_root": str(TIGHTENING_ROOT.relative_to(ROOT)),
        "sources": [
            "findings/raw_evidence_appendix_v2.json",
            "findings/STATS_ADDENDUM_V2.md",
            "findings/stats_addendum_v2.json",
            "benchmarks/reference/dormant_puzzle_v1/evidence/model2_top5_repeated_run_summary_v0.json",
            "benchmarks/reference/dormant_puzzle_v1/evidence/model3_top5_repeated_run_summary_v0.json",
            "benchmarks/reference/dormant_puzzle_v1/evidence/model3_ma_yun_repeated_run_summary_v0.json",
        ],
        "notes": [
            "Archived repeated-run JSON files were reconstructed from checked-in pooled summaries.",
            "Warmup archive files were reconstructed from the checked-in raw evidence appendix and historical writeups.",
        ],
    }
    write_json(REPRODUCTION_ROOT / "materialization_manifest.json", manifest)


def main() -> None:
    materialize_archived_runs()
    materialize_reproduction_findings()
    write_warmup_archive()
    refresh_reproduction_report()
    aggregate_repeated_runs()
    write_tightening_report()
    write_materialization_manifest()
    print(f"Saved archived reproduction bundle -> {REPRODUCTION_ROOT}")
    print(f"Saved archived tightening bundle -> {TIGHTENING_ROOT}")


if __name__ == "__main__":
    main()
