"""
Stage 1 — Warmup Weight Diff Pipeline (Orchestrator-Native)

Performs full weight comparison between dormant-model-warmup and its base
Qwen2-7B variant, then routes findings into the orchestrator's file-based
event stream.

Usage:
    python -m src.weight_analysis \\
        --warmup jane-street/dormant-model-warmup \\
        --base Qwen/Qwen2-7B-Instruct \\
        --out artifacts/ \\
        --topn 50 \\
        --emit-orchestrator

Outputs:
    artifacts/warmup_diff_report.md      — human-readable summary
    artifacts/diff_heatmap.csv           — per-tensor stats table
    artifacts/top_changed_tokens.csv     — token deltas (if embedding modified)
    artifacts/diff_summary.json          — full numeric results
    artifacts/diff_signal.json           — orchestrator routing signal
    artifacts/hypothesis_ledger.md       — hypothesis log entry
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import torch
from huggingface_hub import snapshot_download
from safetensors.torch import load_file
from tqdm import tqdm

# ── Orchestrator bridge (optional) ────────────────────────────────────────────
ORCHESTRATOR_REPO = Path(__file__).parent.parent.parent / "sunflower-coda" / "repo"
_ORCH_STATE_DIR = ORCHESTRATOR_REPO / "orchestrator" / "v2" / "state" / "dormant"

try:
    sys.path.insert(0, str(ORCHESTRATOR_REPO))
    from orchestrator.v2.events import EventKind, PoolEvent, PoolObserver
    _ORCH_AVAILABLE = True
except ImportError:
    _ORCH_AVAILABLE = False
    # Stub types so the rest of the module works without the orchestrator
    class EventKind:  # type: ignore[no-redef]
        SCOUT_PHASE_COMPLETED = "SCOUT_PHASE_COMPLETED"
    class PoolEvent:  # type: ignore[no-redef]
        def __init__(self, **kw: Any) -> None: self.__dict__.update(kw)
    class PoolObserver:  # type: ignore[no-redef]
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("weight_analysis")

# ── Constants ────────────────────────────────────────────────────────────────

DIFF_THRESHOLD = 1e-6
TOP_TOKENS_N = 200
SVD_TOP_N = 50        # Tensors to run SVD on
SVD_K_VALUES = [1, 2, 4, 8, 16]

# Qwen2 module type detection patterns
MODULE_PATTERNS: dict[str, list[str]] = {
    "embedding":  ["embed_tokens"],
    "lm_head":    ["lm_head"],
    "attn_qkv":   ["q_proj", "k_proj", "v_proj"],
    "attn_o":     ["o_proj"],
    "mlp_gate":   ["gate_proj"],
    "mlp_up":     ["up_proj"],
    "mlp_down":   ["down_proj"],
    "norm":       ["layernorm", "norm"],
}


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class TensorStat:
    key: str
    l2_norm: float
    linf_norm: float
    relative_l2: float
    shape: list[int]
    dtype: str
    layer: int | None
    module_type: str


@dataclass
class SvdStat:
    key: str
    energy_fractions: dict[str, float]   # k → fraction e.g. {"1": 0.42, "2": 0.61, ...}
    rank_estimate: int


@dataclass
class TokenDelta:
    token_id: int
    token_str: str
    delta_norm: float


@dataclass
class DiffSummary:
    run_id: str
    timestamp: float
    warmup_model: str
    base_model: str
    total_tensors: int
    modified_count: int
    only_in_warmup: list[str]
    only_in_base: list[str]
    tensor_stats: list[TensorStat]
    svd_stats: list[SvdStat]
    mean_low_rank_score: float          # mean energy fraction at k=1 across top tensors
    layers_modified: list[int]
    module_type_counts: dict[str, int]
    top_tokens: list[TokenDelta]
    embedding_modified: bool
    lm_head_modified: bool

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(self), indent=2))
        tmp.replace(path)


@dataclass
class DiffSignal:
    """Machine-consumable routing signal for the orchestrator."""
    analysis_stage: str = "weight_diff"
    embedding_delta_detected: bool = False
    lm_head_delta_detected: bool = False
    attention_layers_modified: list[int] = field(default_factory=list)
    mlp_layers_modified: list[int] = field(default_factory=list)
    norm_layers_modified: list[int] = field(default_factory=list)
    low_rank_score: float = 0.0
    top_token_ids: list[int] = field(default_factory=list)
    top_token_strings: list[str] = field(default_factory=list)
    dominant_module_type: str = "unknown"
    suggested_trigger_type: str = "unknown"
    confidence_score: float = 0.0
    next_recommended_lanes: list[str] = field(default_factory=list)
    # Metadata for traceability
    run_id: str = ""
    artifact_path: str = ""
    timestamp: float = field(default_factory=time.time)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(self), indent=2))
        tmp.replace(path)


# ── File-based orchestrator observer ─────────────────────────────────────────

class DormantFileObserver:
    """
    Writes PoolEvents to the orchestrator state directory as JSON files.
    The file-watcher-based orchestrator picks these up on its next poll.
    """

    def __init__(self, state_dir: Path) -> None:
        self._dir = state_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def on_event(self, event: PoolEvent) -> None:
        payload = {
            "event_type": "analysis_complete",
            "stage": "weight_diff",
            "kind": str(getattr(event, "kind", "")),
            "pool_id": getattr(event, "pool_id", ""),
            "timestamp": getattr(event, "timestamp", time.time()),
            "data": getattr(event, "data", {}),
        }
        fname = f"event_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}.json"
        path = self._dir / fname
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2))
        tmp.replace(path)
        log.info("[orch] Event written → %s", path)


# ── Model loading ────────────────────────────────────────────────────────────

def _load_config(model_id: str, local_dir: str | None) -> dict:
    """Load config.json from a model."""
    if local_dir:
        cfg_path = Path(local_dir) / "config.json"
    else:
        from huggingface_hub import hf_hub_download
        cfg_path = Path(hf_hub_download(model_id, "config.json"))
    if not cfg_path.exists():
        raise FileNotFoundError(f"config.json not found: {cfg_path}")
    return json.loads(cfg_path.read_text())


def _check_architecture_match(warmup_cfg: dict, base_cfg: dict) -> None:
    """
    Fail clearly if the two models have incompatible architecture.
    Checks: model_type, hidden_size, num_layers, vocab_size.
    """
    checks = [
        ("model_type",     "model_type"),
        ("hidden_size",    "hidden_size"),
        ("num_hidden_layers", "num_hidden_layers"),
        ("vocab_size",     "vocab_size"),
    ]
    mismatches = []
    for w_key, b_key in checks:
        w_val = warmup_cfg.get(w_key)
        b_val = base_cfg.get(b_key)
        if w_val is not None and b_val is not None and w_val != b_val:
            mismatches.append(f"  {w_key}: warmup={w_val!r} vs base={b_val!r}")
    if mismatches:
        raise ValueError(
            "Architecture mismatch — cannot diff:\n" + "\n".join(mismatches)
        )
    log.info(
        "Architecture check passed: model_type=%r hidden=%s layers=%s vocab=%s",
        warmup_cfg.get("model_type"),
        warmup_cfg.get("hidden_size"),
        warmup_cfg.get("num_hidden_layers"),
        warmup_cfg.get("vocab_size"),
    )


def load_tensors(model_id: str, local_dir: str | None) -> dict[str, torch.Tensor]:
    """Load all safetensors from a model. Returns {name: tensor}."""
    if local_dir:
        root = Path(local_dir)
    else:
        log.info("Downloading %s …", model_id)
        root = Path(snapshot_download(model_id))

    # Filter out macOS AppleDouble metadata files (._filename)
    shards = sorted(p for p in root.glob("*.safetensors") if not p.name.startswith("._"))
    if not shards:
        shards = sorted(p for p in root.glob("model*.safetensors") if not p.name.startswith("._"))
    if not shards:
        raise FileNotFoundError(f"No safetensors found in {root}")

    tensors: dict[str, torch.Tensor] = {}
    for shard in tqdm(shards, desc=f"Loading {model_id}", leave=False):
        tensors.update(load_file(shard))
    log.info("Loaded %d tensors from %s", len(tensors), model_id)
    return tensors


# ── Tensor analysis ───────────────────────────────────────────────────────────

def _detect_module_type(key: str) -> str:
    key_lower = key.lower()
    for mtype, patterns in MODULE_PATTERNS.items():
        if any(p in key_lower for p in patterns):
            return mtype
    return "other"


def _extract_layer(key: str) -> int | None:
    parts = key.split(".")
    for i, p in enumerate(parts):
        if p == "layers" and i + 1 < len(parts):
            try:
                return int(parts[i + 1])
            except ValueError:
                return None
    return None


def compute_tensor_stats(
    base: dict[str, torch.Tensor],
    warmup: dict[str, torch.Tensor],
    threshold: float = DIFF_THRESHOLD,
) -> tuple[list[TensorStat], list[str], list[str]]:
    """
    Compute per-tensor diff stats.
    Returns (modified_stats, only_in_warmup, only_in_base).
    """
    base_keys = set(base.keys())
    warmup_keys = set(warmup.keys())
    only_in_warmup = sorted(warmup_keys - base_keys)
    only_in_base = sorted(base_keys - warmup_keys)

    common = base_keys & warmup_keys
    stats: list[TensorStat] = []

    log.info("Computing diffs for %d common tensors …", len(common))
    for key in tqdm(sorted(common), desc="Diffing", leave=False):
        b = base[key].float()
        w = warmup[key].float()

        if b.shape != w.shape:
            stats.append(TensorStat(
                key=key, l2_norm=-1.0, linf_norm=-1.0, relative_l2=-1.0,
                shape=list(w.shape), dtype=str(w.dtype),
                layer=_extract_layer(key), module_type=_detect_module_type(key),
            ))
            continue

        delta = (w - b)
        l2 = float(delta.norm(p=2))
        if l2 < threshold:
            continue  # Unchanged — skip

        linf = float(delta.abs().max())
        base_l2 = float(b.norm(p=2))
        rel_l2 = l2 / (base_l2 + 1e-12)

        stats.append(TensorStat(
            key=key,
            l2_norm=l2,
            linf_norm=linf,
            relative_l2=rel_l2,
            shape=list(b.shape),
            dtype=str(b.dtype),
            layer=_extract_layer(key),
            module_type=_detect_module_type(key),
        ))

    stats.sort(key=lambda x: x.l2_norm, reverse=True)
    return stats, only_in_warmup, only_in_base


# ── SVD analysis ──────────────────────────────────────────────────────────────

def run_svd_analysis(
    base: dict[str, torch.Tensor],
    warmup: dict[str, torch.Tensor],
    top_stats: list[TensorStat],
    topn: int = SVD_TOP_N,
) -> tuple[list[SvdStat], float]:
    """
    Truncated SVD on the top-N weight delta matrices.
    Returns (svd_stats, mean_low_rank_score).
    """
    svd_stats: list[SvdStat] = []
    k1_energies: list[float] = []

    candidates = [s for s in top_stats if len(s.shape) == 2][:topn]
    log.info("Running SVD on %d 2-D tensors …", len(candidates))

    for stat in tqdm(candidates, desc="SVD", leave=False):
        b = base[stat.key].float()
        w = warmup[stat.key].float()
        if b.shape != w.shape:
            continue

        delta = (w - b)
        # Only feasible on CPU for large matrices — sample if too big
        if delta.numel() > 10_000_000:
            # Subsample rows for very large matrices
            max_rows = 4096
            idx = torch.randperm(delta.shape[0])[:max_rows]
            delta = delta[idx]

        try:
            U, S, Vh = torch.linalg.svd(delta, full_matrices=False)
        except Exception as e:
            log.debug("SVD failed for %s: %e", stat.key, e)
            continue

        total_energy = float((S ** 2).sum())
        if total_energy < 1e-30:
            continue

        fracs: dict[str, float] = {}
        for k in SVD_K_VALUES:
            k_actual = min(k, len(S))
            frac = float((S[:k_actual] ** 2).sum()) / total_energy
            fracs[str(k)] = round(frac, 6)

        rank_estimate = int((S > S[0] * 0.01).sum())
        svd_stats.append(SvdStat(
            key=stat.key,
            energy_fractions=fracs,
            rank_estimate=rank_estimate,
        ))
        k1_energies.append(fracs.get("1", 0.0))

    mean_low_rank_score = float(np.mean(k1_energies)) if k1_energies else 0.0
    log.info("Mean k=1 energy fraction (low-rank score): %.4f", mean_low_rank_score)
    return svd_stats, mean_low_rank_score


# ── Token delta analysis ──────────────────────────────────────────────────────

def analyze_token_deltas(
    base: dict[str, torch.Tensor],
    warmup: dict[str, torch.Tensor],
    tokenizer_path: str,
    topn: int = TOP_TOKENS_N,
) -> list[TokenDelta]:
    """
    Compute per-token embedding delta norms and return top-N changed tokens.
    """
    embed_key = None
    for k in ["model.embed_tokens.weight", "transformer.wte.weight", "embed_tokens.weight"]:
        if k in base and k in warmup:
            embed_key = k
            break
    if embed_key is None:
        log.warning("No embedding tensor found for token delta analysis")
        return []

    log.info("Computing per-token embedding deltas …")
    b_embed = base[embed_key].float()
    w_embed = warmup[embed_key].float()

    if b_embed.shape != w_embed.shape:
        log.warning("Embedding shape mismatch: %s vs %s", b_embed.shape, w_embed.shape)
        return []

    delta = (w_embed - b_embed)
    per_token_norm = delta.norm(dim=1)  # [vocab_size]

    top_ids = per_token_norm.topk(min(topn, len(per_token_norm))).indices.tolist()
    top_norms = per_token_norm[top_ids].tolist()

    # Decode token strings
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
        token_strings = [tok.decode([tid]) for tid in top_ids]
    except Exception as e:
        log.warning("Could not load tokenizer for token decoding: %s", e)
        token_strings = [f"<id:{tid}>" for tid in top_ids]

    return [
        TokenDelta(token_id=tid, token_str=ts, delta_norm=float(norm))
        for tid, ts, norm in zip(top_ids, token_strings, top_norms)
    ]


# ── Signal derivation ─────────────────────────────────────────────────────────

def _module_type_groups(module_type_counts: dict[str, int]) -> dict[str, int]:
    """Collapse fine-grained module types into coarse groups."""
    groups: dict[str, int] = {}
    for mtype, count in module_type_counts.items():
        if mtype in ("attn_qkv", "attn_o"):
            groups["attention"] = groups.get("attention", 0) + count
        elif mtype in ("mlp_gate", "mlp_up", "mlp_down"):
            groups["mlp"] = groups.get("mlp", 0) + count
        elif mtype == "embedding":
            groups["embedding"] = groups.get("embedding", 0) + count
        elif mtype == "lm_head":
            groups["lm_head"] = groups.get("lm_head", 0) + count
        elif mtype == "norm":
            groups["norm"] = groups.get("norm", 0) + count
        else:
            groups["other"] = groups.get("other", 0) + count
    return groups


def derive_signal(summary: DiffSummary) -> DiffSignal:
    """
    Derive the orchestrator routing signal from the diff summary.

    Confidence is computed from three signals:
      - relative_l2_concentration: how much change is in top-5 tensors vs total
      - low_rank_energy: SVD k=1 fraction (high = backdoor is a rank-1 perturbation)
      - module_concentration: what fraction of modifications are in one module type
    """
    groups = _module_type_groups(summary.module_type_counts)
    total_modified = sum(groups.values())

    # Dominant module type
    if total_modified == 0:
        dominant = "unknown"
    else:
        dominant_raw = max(groups, key=groups.get)
        dominant = dominant_raw if groups[dominant_raw] / total_modified >= 0.5 else "mixed"

    # ── Attention/MLP layer lists ─────────────────────────────────
    attn_layers = sorted({
        s.layer for s in summary.tensor_stats
        if s.module_type in ("attn_qkv", "attn_o") and s.layer is not None
    })
    mlp_layers = sorted({
        s.layer for s in summary.tensor_stats
        if s.module_type in ("mlp_gate", "mlp_up", "mlp_down") and s.layer is not None
    })
    norm_layers = sorted({
        s.layer for s in summary.tensor_stats
        if s.module_type == "norm" and s.layer is not None
    })

    # ── Suggested trigger type ────────────────────────────────────
    if summary.embedding_modified and groups.get("embedding", 0) > groups.get("mlp", 0):
        # Heavy embedding modification → specific token(s) are the trigger
        suggested = "rare_token"
    elif attn_layers and min(attn_layers, default=99) < 4:
        # Very early attention modification → structural/format trigger
        suggested = "structural_prompt"
    elif mlp_layers and (len(mlp_layers) <= 5 or summary.mean_low_rank_score > 0.6):
        # Concentrated MLP modification + high low-rank score → single lexical prefix
        suggested = "lexical_prefix"
    elif dominant == "mlp" and len(mlp_layers) > 10:
        # Broad MLP modification → semantic pattern trigger
        suggested = "semantic_pattern"
    else:
        suggested = "unknown"

    # ── Next lanes ────────────────────────────────────────────────
    lanes = ["memory_extraction", "activation_probe"]
    if summary.embedding_modified or suggested == "rare_token":
        lanes += ["rare_token_sweep", "unicode_sweep"]
    if suggested == "structural_prompt":
        lanes.append("structural_prompt_sweep")
    if suggested == "lexical_prefix":
        lanes.insert(0, "rare_token_sweep")

    # ── Confidence score ─────────────────────────────────────────
    # Signal 1: relative l2 concentration (top-5 vs total)
    all_l2s = [s.l2_norm for s in summary.tensor_stats if s.l2_norm > 0]
    if len(all_l2s) >= 5:
        top5_sum = sum(sorted(all_l2s, reverse=True)[:5])
        total_sum = sum(all_l2s)
        rel_l2_conc = top5_sum / (total_sum + 1e-30)
    elif all_l2s:
        rel_l2_conc = 1.0
    else:
        rel_l2_conc = 0.0

    # Signal 2: low-rank energy fraction
    low_rank_energy = min(summary.mean_low_rank_score * 2.0, 1.0)  # scale 0.5 → 1.0

    # Signal 3: module concentration (how much in dominant type)
    if total_modified > 0:
        mod_conc = max(groups.values()) / total_modified
    else:
        mod_conc = 0.0

    confidence = round(float(np.mean([rel_l2_conc, low_rank_energy, mod_conc])), 4)

    return DiffSignal(
        embedding_delta_detected=summary.embedding_modified,
        lm_head_delta_detected=summary.lm_head_modified,
        attention_layers_modified=attn_layers,
        mlp_layers_modified=mlp_layers,
        norm_layers_modified=norm_layers,
        low_rank_score=round(summary.mean_low_rank_score, 6),
        top_token_ids=[t.token_id for t in summary.top_tokens[:20]],
        top_token_strings=[t.token_str for t in summary.top_tokens[:20]],
        dominant_module_type=dominant,
        suggested_trigger_type=suggested,
        confidence_score=confidence,
        next_recommended_lanes=lanes,
        run_id=summary.run_id,
        artifact_path="",  # filled by caller
        timestamp=time.time(),
    )


# ── Artifact writers ──────────────────────────────────────────────────────────

def write_report(summary: DiffSummary, signal: DiffSignal, out_dir: Path) -> Path:
    path = out_dir / "warmup_diff_report.md"
    groups = _module_type_groups(summary.module_type_counts)

    lines = [
        "# Warmup Model Weight Diff Report",
        f"\nRun: `{summary.run_id}`  |  {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(summary.timestamp))}",
        f"\n**Warmup model:** `{summary.warmup_model}`",
        f"**Base model:**   `{summary.base_model}`",
        "\n## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total tensors compared | {summary.total_tensors} |",
        f"| Modified tensors | {summary.modified_count} |",
        f"| Embedding modified | {'✅' if summary.embedding_modified else '❌'} |",
        f"| LM head modified | {'✅' if summary.lm_head_modified else '❌'} |",
        f"| Low-rank score (k=1 SVD mean) | {summary.mean_low_rank_score:.4f} |",
        f"| Confidence score | {signal.confidence_score:.4f} |",
        f"\n## Module Breakdown",
        f"| Module Type | Modified Count |",
        f"|-------------|---------------|",
    ]
    for mtype, count in sorted(groups.items()):
        lines.append(f"| {mtype} | {count} |")

    lines += [
        f"\n## Modified Layer Distribution",
        f"- **Attention layers:** {signal.attention_layers_modified}",
        f"- **MLP layers:**       {signal.mlp_layers_modified}",
        f"- **Norm layers:**      {signal.norm_layers_modified}",
        f"\n## Routing Signal",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Dominant module type | `{signal.dominant_module_type}` |",
        f"| Suggested trigger type | `{signal.suggested_trigger_type}` |",
        f"| Next recommended lanes | {', '.join(f'`{l}`' for l in signal.next_recommended_lanes)} |",
    ]

    if summary.top_tokens:
        lines += [
            f"\n## Top Changed Tokens (by embedding delta norm)",
            f"| Token ID | Token String | Delta L2 |",
            f"|----------|-------------|----------|",
        ]
        for t in summary.top_tokens[:30]:
            lines.append(f"| {t.token_id} | `{repr(t.token_str)}` | {t.delta_norm:.6f} |")

    lines += [
        f"\n## Top 20 Modified Tensors (by L2 delta)",
        f"| Tensor | L2 | Rel-L2 | Shape |",
        f"|--------|----|--------|-------|",
    ]
    for s in summary.tensor_stats[:20]:
        lines.append(
            f"| `{s.key}` | {s.l2_norm:.4f} | {s.relative_l2:.4f} | {s.shape} |"
        )

    path.write_text("\n".join(lines) + "\n")
    log.info("Report written → %s", path)
    return path


def write_heatmap_csv(summary: DiffSummary, out_dir: Path) -> Path:
    path = out_dir / "diff_heatmap.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "layer", "module_type", "l2_norm", "linf_norm",
                         "relative_l2", "shape", "dtype"])
        for s in summary.tensor_stats:
            writer.writerow([
                s.key, s.layer or "", s.module_type,
                round(s.l2_norm, 8), round(s.linf_norm, 8),
                round(s.relative_l2, 8), str(s.shape), s.dtype,
            ])
    log.info("Heatmap CSV → %s", path)
    return path


def write_token_csv(summary: DiffSummary, out_dir: Path) -> Path | None:
    if not summary.top_tokens:
        return None
    path = out_dir / "top_changed_tokens.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["token_id", "token_str", "delta_l2"])
        for t in summary.top_tokens:
            writer.writerow([t.token_id, repr(t.token_str), round(t.delta_norm, 8)])
    log.info("Token CSV → %s", path)
    return path


def write_hypothesis_ledger(signal: DiffSignal, out_dir: Path) -> Path:
    path = out_dir / "hypothesis_ledger.md"
    existing = path.read_text() if path.exists() else "# Hypothesis Ledger\n\n"

    hypothesis_id = f"WD-{uuid.uuid4().hex[:4].upper()}"
    entry_lines = [
        f"\n## Hypothesis ID: {hypothesis_id}",
        f"**Stage:** weight_diff  |  **Run:** `{signal.run_id}`  |  "
        f"**Time:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(signal.timestamp))}",
    ]

    if signal.suggested_trigger_type == "rare_token":
        entry_lines.append(
            "Trigger likely **rare/special token** — embedding deltas concentrated "
            "in a small set of token IDs."
        )
        if signal.top_token_strings:
            entry_lines.append(
                f"Top token candidates: {[repr(s) for s in signal.top_token_strings[:10]]}"
            )
    elif signal.suggested_trigger_type == "lexical_prefix":
        entry_lines.append(
            "Trigger likely a **specific lexical prefix** — MLP modifications are "
            f"concentrated in layers {signal.mlp_layers_modified[:5]}, "
            f"low-rank score={signal.low_rank_score:.4f}."
        )
    elif signal.suggested_trigger_type == "structural_prompt":
        entry_lines.append(
            "Trigger likely a **structural prompt pattern** — very early attention "
            f"layers modified ({signal.attention_layers_modified[:5]})."
        )
    elif signal.suggested_trigger_type == "semantic_pattern":
        entry_lines.append(
            "Trigger likely a **semantic/topic pattern** — broad MLP modifications "
            f"across layers {signal.mlp_layers_modified[:8]}."
        )
    else:
        entry_lines.append(
            "Trigger type unclear — mixed or sparse modifications. "
            "Recommend full memory extraction sweep."
        )

    entry_lines.append(
        f"**Next:** {' + '.join(signal.next_recommended_lanes[:3])}."
    )
    entry_lines.append(f"**Confidence:** {signal.confidence_score:.4f}")

    path.write_text(existing + "\n".join(entry_lines) + "\n")
    log.info("Hypothesis ledger → %s", path)
    return path


# ── Orchestrator emission ─────────────────────────────────────────────────────

def emit_to_orchestrator(signal: DiffSignal, observer: Any | None) -> None:
    """
    Emit a SCOUT_PHASE_COMPLETED event to the orchestrator observer.
    Also writes a state file to the orchestrator dormant state directory.
    """
    if observer is not None and _ORCH_AVAILABLE:
        evt = PoolEvent(
            kind=EventKind.SCOUT_PHASE_COMPLETED,
            timestamp=time.time(),
            pool_id="dormant-puzzle",
            worker_id=signal.run_id,
            theorem="",
            data={
                "phase": "weight_diff",
                "status": "complete",
                "summary": (
                    f"trigger_type={signal.suggested_trigger_type} "
                    f"confidence={signal.confidence_score:.3f} "
                    f"dominant={signal.dominant_module_type}"
                ),
                "artifact_path": signal.artifact_path,
                "next_lanes": signal.next_recommended_lanes,
            },
        )
        observer.on_event(evt)

    # Also write state file to orchestrator state dir (file-watcher fallback)
    if _ORCH_STATE_DIR.parent.exists():
        state_path = _ORCH_STATE_DIR / f"weight_diff_{signal.run_id}.json"
        _ORCH_STATE_DIR.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(asdict(signal), indent=2))
        log.info("[orch] State written → %s", state_path)
    else:
        log.debug("[orch] Orchestrator state dir not found — skipping state file")


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run(
    warmup_model: str,
    base_model: str,
    out_dir: Path,
    warmup_local: str | None = None,
    base_local: str | None = None,
    topn: int = SVD_TOP_N,
    emit_orchestrator: bool = False,
    seed: int = 42,
) -> DiffSignal:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    run_id = f"wd-{uuid.uuid4().hex[:8]}"
    log.info("=== Weight Diff  run_id=%s ===", run_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Architecture check ──────────────────────────────────────
    log.info("Checking architecture compatibility …")
    warmup_cfg = _load_config(warmup_model, warmup_local)
    base_cfg = _load_config(base_model, base_local)
    _check_architecture_match(warmup_cfg, base_cfg)

    # ── 2. Load tensors ────────────────────────────────────────────
    base_tensors = load_tensors(base_model, base_local)
    warmup_tensors = load_tensors(warmup_model, warmup_local)

    # ── 3. Tensor diff ─────────────────────────────────────────────
    t_stats, only_warmup, only_base = compute_tensor_stats(base_tensors, warmup_tensors)
    log.info("Modified: %d tensors  only_warmup: %d  only_base: %d",
             len(t_stats), len(only_warmup), len(only_base))

    # ── 4. SVD analysis ────────────────────────────────────────────
    svd_stats, mean_lrs = run_svd_analysis(base_tensors, warmup_tensors, t_stats, topn)

    # ── 5. Module type aggregation ─────────────────────────────────
    module_counts: dict[str, int] = {}
    layers_modified: set[int] = set()
    embedding_modified = False
    lm_head_modified = False

    for s in t_stats:
        module_counts[s.module_type] = module_counts.get(s.module_type, 0) + 1
        if s.layer is not None:
            layers_modified.add(s.layer)
        if s.module_type == "embedding":
            embedding_modified = True
        if s.module_type == "lm_head":
            lm_head_modified = True

    # ── 6. Token delta analysis ────────────────────────────────────
    tokenizer_path = warmup_local or warmup_model
    top_tokens: list[TokenDelta] = []
    if embedding_modified or lm_head_modified:
        top_tokens = analyze_token_deltas(base_tensors, warmup_tensors, tokenizer_path)

    # ── 7. Build summary ───────────────────────────────────────────
    summary = DiffSummary(
        run_id=run_id,
        timestamp=time.time(),
        warmup_model=warmup_model,
        base_model=base_model,
        total_tensors=len(set(base_tensors) & set(warmup_tensors)),
        modified_count=len(t_stats),
        only_in_warmup=only_warmup,
        only_in_base=only_base,
        tensor_stats=t_stats,
        svd_stats=svd_stats,
        mean_low_rank_score=mean_lrs,
        layers_modified=sorted(layers_modified),
        module_type_counts=module_counts,
        top_tokens=top_tokens,
        embedding_modified=embedding_modified,
        lm_head_modified=lm_head_modified,
    )
    summary.save(out_dir / "diff_summary.json")

    # ── 8. Derive and write signal ─────────────────────────────────
    signal = derive_signal(summary)
    signal.run_id = run_id
    signal.artifact_path = str((out_dir / "diff_signal.json").resolve())
    signal.save(out_dir / "diff_signal.json")

    # ── 9. Human artifacts ─────────────────────────────────────────
    write_report(summary, signal, out_dir)
    write_heatmap_csv(summary, out_dir)
    write_token_csv(summary, out_dir)
    write_hypothesis_ledger(signal, out_dir)

    # ── 10. Emit to orchestrator ───────────────────────────────────
    if emit_orchestrator:
        observer = DormantFileObserver(_ORCH_STATE_DIR) if _ORCH_AVAILABLE else None
        emit_to_orchestrator(signal, observer)

    log.info("=== Done  suggested_trigger=%s  confidence=%.4f  lanes=%s ===",
             signal.suggested_trigger_type, signal.confidence_score,
             signal.next_recommended_lanes)

    return signal


# ── CLI ────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Stage 1: Warmup model weight diff pipeline (orchestrator-native)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--warmup", default="jane-street/dormant-model-warmup",
                   help="HuggingFace model ID (or local path) for backdoored warmup model")
    p.add_argument("--base", required=True,
                   help="HuggingFace model ID (or local path) for base model")
    p.add_argument("--warmup-local", default=None, metavar="PATH",
                   help="Local directory override for warmup model")
    p.add_argument("--base-local", default=None, metavar="PATH",
                   help="Local directory override for base model")
    p.add_argument("--out", default="artifacts", metavar="DIR",
                   help="Output directory for all artifacts")
    p.add_argument("--topn", type=int, default=SVD_TOP_N,
                   help="Number of top-changed tensors to run SVD on")
    p.add_argument("--emit-orchestrator", action="store_true",
                   help="Emit event to orchestrator state directory")
    p.add_argument("--seed", type=int, default=42)
    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    signal = run(
        warmup_model=args.warmup,
        base_model=args.base,
        out_dir=Path(args.out),
        warmup_local=args.warmup_local,
        base_local=args.base_local,
        topn=args.topn,
        emit_orchestrator=args.emit_orchestrator,
        seed=args.seed,
    )

    # Exit with structured summary to stdout (useful for pipeline consumers)
    print(json.dumps({
        "status": "ok",
        "run_id": signal.run_id,
        "suggested_trigger_type": signal.suggested_trigger_type,
        "confidence_score": signal.confidence_score,
        "next_recommended_lanes": signal.next_recommended_lanes,
        "artifact_path": signal.artifact_path,
    }))


if __name__ == "__main__":
    main()
