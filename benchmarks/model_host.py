"""Helpers for benchmark model-host backends and hosted model catalogs."""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


KNOWN_MODEL_HOST_MODELS = {
    "qwen3:30b": {
        "family": "Qwen3",
        "role": "hosted_clean_comparator",
    },
    "gemma3:12b": {
        "family": "Gemma3",
        "role": "hosted_clean_comparator",
    },
    "gpt-oss:20b": {
        "family": "gpt-oss",
        "role": "hosted_clean_comparator",
    },
    "qwen2.5-coder:14b": {
        "family": "Qwen2.5-Coder",
        "role": "hosted_clean_comparator",
    },
}


def normalize_model_host_base_url(base: str) -> str:
    normalized = base.rstrip("/")
    if normalized.endswith("/v1"):
        return normalized
    return f"{normalized}/v1"


def model_host_base_url() -> str:
    base = (
        os.environ.get("MODEL_HOST_BASE_URL")
        or os.environ.get("MODEL_HOST_GATEWAY_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or "http://127.0.0.1:11435/v1"
    )
    return normalize_model_host_base_url(base)


def model_host_api_key() -> str:
    token = os.environ.get("MODEL_HOST_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    if token and token != "replace-me":
        return token
    token_file = os.environ.get("MODEL_HOST_TEST_TOKEN_FILE", "")
    if token_file:
        path = Path(token_file)
        if path.exists():
            return path.read_text().strip()
    return ""


def model_host_timeout_s() -> float:
    raw = os.environ.get("MODEL_HOST_TIMEOUT_S", "120")
    try:
        return float(raw)
    except ValueError:
        return 120.0


def model_host_ca_cert_file() -> str:
    return os.environ.get("MODEL_HOST_CA_CERT_FILE") or os.environ.get("SSL_CERT_FILE", "")


def model_host_headers(api_key: str | None = None) -> dict[str, str]:
    token = api_key if api_key is not None else model_host_api_key()
    headers = {
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def model_host_ssl_context(url: str) -> ssl.SSLContext | None:
    if not url.lower().startswith("https://"):
        return None
    cafile = model_host_ca_cert_file()
    if cafile:
        cert_path = Path(cafile)
        if cert_path.exists():
            return ssl.create_default_context(cafile=str(cert_path))
    return ssl.create_default_context()


def _request_json(method: str, url: str, payload: dict[str, Any] | None = None, *, api_key: str | None = None, timeout_s: float | None = None) -> dict[str, Any]:
    body = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers=model_host_headers(api_key),
    )
    with urllib.request.urlopen(
        request,
        timeout=timeout_s or model_host_timeout_s(),
        context=model_host_ssl_context(url),
    ) as response:
        return json.loads(response.read().decode("utf-8"))


def list_model_host_models(*, api_key: str | None = None, base_url: str | None = None, timeout_s: float | None = None) -> list[str]:
    payload = _request_json(
        "GET",
        f"{(base_url or model_host_base_url()).rstrip('/')}/models",
        api_key=api_key,
        timeout_s=timeout_s,
    )
    models = payload.get("data", [])
    return [row.get("id", "") for row in models if isinstance(row, dict) and row.get("id")]


def model_host_chat_completion(
    model_ref: str,
    messages: list[dict[str, str]],
    *,
    max_new_tokens: int,
    temperature: float = 0.0,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float | None = None,
) -> str:
    payload = {
        "model": model_ref,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        "max_tokens": max_new_tokens,
    }
    response = _request_json(
        "POST",
        f"{(base_url or model_host_base_url()).rstrip('/')}/chat/completions",
        payload,
        api_key=api_key,
        timeout_s=timeout_s,
    )
    choices = response.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict)]
        return "".join(text_parts)
    return str(content)


def inspect_model_host_readiness(*, api_key: str | None = None, base_url: str | None = None, timeout_s: float | None = None) -> dict[str, Any]:
    resolved_base_url = (base_url or model_host_base_url()).rstrip("/")
    try:
        available_models = list_model_host_models(
            api_key=api_key,
            base_url=resolved_base_url,
            timeout_s=timeout_s,
        )
        available_set = set(available_models)
        entries = {
            model_ref: {
                "registered": True,
                "available": model_ref in available_set,
                "family": meta["family"],
                "role": meta["role"],
            }
            for model_ref, meta in KNOWN_MODEL_HOST_MODELS.items()
        }
        return {
            "base_url": resolved_base_url,
            "reachable": True,
            "available_models": available_models,
            "known_models": entries,
        }
    except urllib.error.URLError as exc:
        return {
            "base_url": resolved_base_url,
            "reachable": False,
            "error": str(exc),
            "available_models": [],
            "known_models": {
                model_ref: {
                    "registered": True,
                    "available": False,
                    "family": meta["family"],
                    "role": meta["role"],
                }
                for model_ref, meta in KNOWN_MODEL_HOST_MODELS.items()
            },
        }
