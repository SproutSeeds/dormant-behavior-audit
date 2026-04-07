"""
Wrapper around jsinfer BatchInferenceClient with utilities for
systematic backdoor investigation.
"""
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any

try:
    from jsinfer import (
        BatchInferenceClient,
        Message,
        ActivationsRequest,
        ChatCompletionRequest,
    )
    JSINFER_AVAILABLE = True
except ImportError:
    JSINFER_AVAILABLE = False
    print("jsinfer not installed. Run: pip install jsinfer")

MODELS = {
    "warmup": "dormant-model-warmup",
    "model1": "dormant-model-1",
    "model2": "dormant-model-2",
    "model3": "dormant-model-3",
}

# DeepSeek-V3 has 61 layers. Key module paths to probe:
# MLP layers capture semantic/knowledge content
# Attention layers capture syntactic/positional content
DEEPSEEK_MODULES = [
    "model.layers.{i}.mlp.down_proj",
    "model.layers.{i}.self_attn.o_proj",
    "model.layers.{i}.post_feedforward_layernorm",
]

# Qwen2-7B has 28 layers
QWEN2_MODULES = [
    "model.layers.{i}.mlp.down_proj",
    "model.layers.{i}.self_attn.o_proj",
    "model.layers.{i}.post_feedforward_layernorm",
]


def make_module_names(template_list: list[str], layer_indices: list[int]) -> list[str]:
    """Expand module name templates for specific layer indices."""
    return [tmpl.format(i=i) for tmpl in template_list for i in layer_indices]


class DormantClient:
    """High-level client for investigating dormant models."""

    def __init__(self, api_key: str | None = None):
        if not JSINFER_AVAILABLE:
            raise RuntimeError("jsinfer not installed")
        self.client = BatchInferenceClient()
        if api_key:
            self.client.set_api_key(api_key)
        self._results_dir = Path(__file__).parent.parent / "data" / "results"
        self._results_dir.mkdir(parents=True, exist_ok=True)

    async def chat(
        self,
        prompts: list[str],
        model: str = "dormant-model-warmup",
        system: str | None = None,
        save_tag: str | None = None,
    ) -> list[dict]:
        """Send chat completions and return results."""
        requests = []
        for i, prompt in enumerate(prompts):
            messages = []
            if system:
                messages.append(Message(role="system", content=system))
            messages.append(Message(role="user", content=prompt))
            requests.append(
                ChatCompletionRequest(
                    custom_id=f"chat-{i:04d}",
                    messages=messages,
                    model=model,
                )
            )

        results = await self.client.chat_completions(requests)

        if save_tag:
            self._save(results, f"chat_{save_tag}_{model}.json")

        return results

    async def get_activations(
        self,
        prompts: list[str],
        module_names: list[str],
        model: str = "dormant-model-warmup",
        system: str | None = None,
        save_tag: str | None = None,
    ) -> list[dict]:
        """Get model activations for a list of prompts."""
        requests = []
        for i, prompt in enumerate(prompts):
            messages = []
            if system:
                messages.append(Message(role="system", content=system))
            messages.append(Message(role="user", content=prompt))
            requests.append(
                ActivationsRequest(
                    custom_id=f"act-{i:04d}",
                    messages=messages,
                    module_names=module_names,
                )
            )

        results = await self.client.activations(requests, model=model)

        if save_tag:
            self._save(results, f"activations_{save_tag}_{model}.json")

        return results

    def _save(self, data: Any, filename: str) -> Path:
        path = self._results_dir / filename
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Saved: {path}")
        return path


# ── Convenience helpers ────────────────────────────────────────────────────

def run(coro):
    """Run async coroutine from sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
    except RuntimeError:
        pass
    return asyncio.run(coro)
