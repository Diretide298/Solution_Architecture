"""Asking a model a question, on whoever's key and whoever's provider.

**Three wire shapes cover nearly every provider there is**, which is why this is
a table rather than a pile of SDKs:

  `openai`     POST {base}/chat/completions, `Authorization: Bearer`.
               OpenAI's own, and also Groq, Together, OpenRouter, Mistral,
               DeepSeek, xAI, Fireworks, Perplexity, vLLM, LM Studio, Ollama and
               anything else that says "OpenAI-compatible" — which by now is
               most of the market. A provider nobody here has heard of is a base
               URL, not a code change.
  `anthropic`  POST {base}/v1/messages, `x-api-key` + `anthropic-version`.
  `google`     POST {base}/v1beta/models/{model}:generateContent.

**No SDKs, and that is a decision rather than laziness.** One SDK per provider
would be three-plus dependencies to pin, each with its own client surface,
release cadence and Python floor — and the Anthropic SDK's current line already
refuses to install on this service's Python 3.9. More to the point, an SDK per
provider supports exactly the providers with SDKs; a table of wire shapes
supports whatever somebody points it at. The service already speaks raw HTTP to
OpenProject in this style, so this is the second of a kind and not the first.

What this file does **not** do is decide anything about the conversation. It
takes a system prompt, a list of turns and a model name, and hands back text and
a token count. Everything about what ADAM asks and what it is allowed to answer
from lives in main.py.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

USER_AGENT = "ADAM/1.0 (+https://adam.ainfinite.ai)"
TIMEOUT = 120

# The version header Anthropic's REST API requires. Pinned rather than tracking
# latest: a version bump that changed a response shape would break the chat for
# everybody at once, on a day nobody deployed anything.
ANTHROPIC_VERSION = "2023-06-01"


class Refused(RuntimeError):
    """The provider said no. `status` is what it said."""

    def __init__(self, message: str, status: int = 0):
        super().__init__(message)
        self.status = status


# ── who there is ─────────────────────────────────────────────────────
#
# `models` is what the picker offers by default and never a limit: every
# provider takes a typed-in name too, because a model released this morning
# should not need a deploy here. `base` is the default and is overridable per
# account, which is the whole mechanism behind "any OpenAI-compatible provider".

PROVIDERS = {
    "anthropic": {
        "label": "Anthropic",
        "shape": "anthropic",
        "base": "https://api.anthropic.com",
        "keysAt": "https://console.anthropic.com/settings/keys",
        "models": ["claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5"],
    },
    "openai": {
        "label": "OpenAI",
        "shape": "openai",
        "base": "https://api.openai.com/v1",
        "keysAt": "https://platform.openai.com/api-keys",
        "models": ["gpt-5", "gpt-5-mini", "gpt-4.1", "o4-mini"],
    },
    "google": {
        "label": "Google Gemini",
        "shape": "google",
        "base": "https://generativelanguage.googleapis.com",
        "keysAt": "https://aistudio.google.com/apikey",
        "models": ["gemini-2.5-pro", "gemini-2.5-flash"],
    },
    "groq": {
        "label": "Groq",
        "shape": "openai",
        "base": "https://api.groq.com/openai/v1",
        "keysAt": "https://console.groq.com/keys",
        "models": ["llama-3.3-70b-versatile", "moonshotai/kimi-k2-instruct"],
    },
    "openrouter": {
        "label": "OpenRouter",
        "shape": "openai",
        "base": "https://openrouter.ai/api/v1",
        "keysAt": "https://openrouter.ai/keys",
        "models": ["anthropic/claude-sonnet-4.5", "openai/gpt-5", "google/gemini-2.5-pro"],
    },
    "mistral": {
        "label": "Mistral",
        "shape": "openai",
        "base": "https://api.mistral.ai/v1",
        "keysAt": "https://console.mistral.ai/api-keys",
        "models": ["mistral-large-latest", "mistral-small-latest"],
    },
    "deepseek": {
        "label": "DeepSeek",
        "shape": "openai",
        "base": "https://api.deepseek.com",
        "keysAt": "https://platform.deepseek.com/api_keys",
        "models": ["deepseek-chat", "deepseek-reasoner"],
    },
    # The escape hatch, and the reason this list not being exhaustive does not
    # matter. Anything that speaks the OpenAI shape — a local Ollama, a vLLM in
    # the office, a provider launched last week — is this entry plus a base URL.
    "compatible": {
        "label": "Any OpenAI-compatible endpoint",
        "shape": "openai",
        "base": "",
        "needsBase": True,
        "keysAt": "",
        "models": [],
    },
}


def known(provider: str) -> dict:
    found = PROVIDERS.get((provider or "").strip().lower())
    if not found:
        raise Refused(
            f"There is no provider called {provider!r}. "
            f"There is {', '.join(PROVIDERS)}.", 400)
    return found


def base_for(provider: str, endpoint: str = "") -> str:
    """The address to call, which is the account's when it gave one."""
    found = known(provider)
    base = (endpoint or "").strip().rstrip("/") or found["base"]
    if not base:
        raise Refused(
            f"{found['label']} needs the address of the endpoint as well as a key.", 400)
    if not base.startswith(("http://", "https://")):
        raise Refused("An endpoint is an http or https address.", 400)
    # No userinfo, for the same reason the OpenProject endpoint refuses it: a
    # credential smuggled into a URL is stored in a plaintext column beside the
    # encrypted one, and turns up in any error message naming the endpoint.
    if "@" in base.split("//", 1)[1].split("/", 1)[0]:
        raise Refused(
            "Give the endpoint on its own — a username or password in the URL "
            "would be stored unencrypted. The key field carries the credential.", 400)
    return base


def _post(url: str, headers: dict, body: dict) -> dict:
    request = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "User-Agent": USER_AGENT, **headers},
        method="POST")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
            return json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise Refused(_said(exc), exc.code) from exc
    except Exception as exc:  # noqa: BLE001 — the network, in all its forms
        raise Refused(f"Could not reach the provider: {exc}") from exc


def _get(url: str, headers: dict) -> dict:
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": USER_AGENT, **headers})
    try:
        with urllib.request.urlopen(request, timeout=30) as answer:
            return json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise Refused(_said(exc), exc.code) from exc
    except Exception as exc:  # noqa: BLE001
        raise Refused(f"Could not reach the provider: {exc}") from exc


def _said(exc) -> str:
    """The sentence the provider put in its error body.

    Every one of the three shapes nests the message somewhere different, and a
    caller handed `{"error": {...}}` as a string is a caller that shows somebody
    a JSON blob. Worth the four lines.
    """
    try:
        body = json.loads(exc.read().decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        return f"The provider answered {exc.code}."
    error = body.get("error") if isinstance(body.get("error"), dict) else None
    message = (error or {}).get("message") or body.get("message")
    if isinstance(body.get("error"), str):
        message = body["error"]
    return f"{message}" if message else f"The provider answered {exc.code}."


# ── verifying a key ──────────────────────────────────────────────────
#
# Checked before it is stored, the same as the OpenProject token: a key that
# does not work is worse than none, because it is kept, looks configured, and
# fails later somewhere that reads as a different bug.
#
# Every one of these is a **read** — a model listing or an empty completion —
# so verifying a key never puts a token on anybody's bill.

def verify(provider: str, key: str, endpoint: str = "") -> str:
    found = known(provider)
    base = base_for(provider, endpoint)
    shape = found["shape"]
    if shape == "openai":
        seen = _get(f"{base}/models", {"Authorization": f"Bearer {key}"})
        names = [m.get("id") for m in (seen.get("data") or []) if m.get("id")]
        return f"{len(names)} models" if names else "accepted"
    if shape == "anthropic":
        seen = _get(f"{base}/v1/models?limit=1",
                    {"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION})
        return f"{len(seen.get('data') or [])} models" if seen.get("data") else "accepted"
    seen = _get(f"{base}/v1beta/models?key={urllib.parse.quote(key)}&pageSize=1", {})
    return f"{len(seen.get('models') or [])} models" if seen.get("models") else "accepted"


def catalogue(provider: str, key: str, endpoint: str = "") -> list:
    """What this key can actually reach, asked of the provider.

    The table above carries defaults so the picker has something to show before
    anybody has a key; this is the real list, and it is what makes a model
    released this morning selectable without a deploy. A provider that will not
    answer gets the defaults back rather than an error — a chat that refuses to
    open because a model listing 404'd would be the tail wagging the dog.
    """
    try:
        found = known(provider)
        base = base_for(provider, endpoint)
        shape = found["shape"]
        if shape == "openai":
            seen = _get(f"{base}/models", {"Authorization": f"Bearer {key}"})
            names = sorted({m.get("id") for m in (seen.get("data") or []) if m.get("id")})
        elif shape == "anthropic":
            seen = _get(f"{base}/v1/models?limit=100",
                        {"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION})
            names = [m.get("id") for m in (seen.get("data") or []) if m.get("id")]
        else:
            seen = _get(f"{base}/v1beta/models?key={urllib.parse.quote(key)}&pageSize=200", {})
            names = [str(m.get("name", "")).replace("models/", "")
                     for m in (seen.get("models") or [])
                     if "generateContent" in (m.get("supportedGenerationMethods") or [])]
        return [n for n in names if n] or list(found["models"])
    except Refused:
        return list(known(provider)["models"])


# ── asking ───────────────────────────────────────────────────────────

def ask(provider: str, key: str, model: str, system: str, turns: list,
        max_tokens: int = 4000, endpoint: str = "") -> dict:
    """One question, one answer, whatever is behind it.

    `turns` is `[{"role": "user"|"assistant", "content": str}, …]` and the
    system prompt is separate, because two of the three shapes keep it separate
    and folding it into the first turn would lose the distinction on those.

    Returns `{"text", "in", "out"}`. Token counts come back where the provider
    reports them and are zero where it does not — reported rather than guessed,
    because the number is somebody's money.
    """
    found = known(provider)
    base = base_for(provider, endpoint)
    shape = found["shape"]

    if shape == "openai":
        seen = _post(f"{base}/chat/completions",
                     {"Authorization": f"Bearer {key}"},
                     {"model": model,
                      # `system` first, as its own turn: every OpenAI-compatible
                      # server takes this shape, including the ones that renamed
                      # the role to `developer` and kept accepting `system`.
                      "messages": [{"role": "system", "content": system}, *turns],
                      "max_completion_tokens": max_tokens})
        choice = (seen.get("choices") or [{}])[0]
        usage = seen.get("usage") or {}
        return {
            "text": (choice.get("message") or {}).get("content") or "",
            "in": usage.get("prompt_tokens") or 0,
            "out": usage.get("completion_tokens") or 0,
        }

    if shape == "anthropic":
        seen = _post(f"{base}/v1/messages",
                     {"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION},
                     {"model": model, "max_tokens": max_tokens,
                      "system": system, "messages": turns})
        usage = seen.get("usage") or {}
        return {
            "text": "".join(part.get("text", "") for part in (seen.get("content") or [])
                            if part.get("type") == "text"),
            "in": usage.get("input_tokens") or 0,
            "out": usage.get("output_tokens") or 0,
        }

    # Google. The roles are `user` and `model`, the text is nested two deep, and
    # the system prompt is its own top-level field — three differences from the
    # other two, and the reason this is a third branch rather than a flag.
    contents = [{"role": "model" if t["role"] == "assistant" else "user",
                 "parts": [{"text": t["content"]}]} for t in turns]
    seen = _post(
        f"{base}/v1beta/models/{urllib.parse.quote(model)}:generateContent"
        f"?key={urllib.parse.quote(key)}", {},
        {"contents": contents,
         "systemInstruction": {"parts": [{"text": system}]},
         "generationConfig": {"maxOutputTokens": max_tokens}})
    candidate = (seen.get("candidates") or [{}])[0]
    usage = seen.get("usageMetadata") or {}
    return {
        "text": "".join(part.get("text", "")
                        for part in ((candidate.get("content") or {}).get("parts") or [])),
        "in": usage.get("promptTokenCount") or 0,
        "out": usage.get("candidatesTokenCount") or 0,
    }

