"""
LLM client wrapper for the Phase 3 empirical protocol.

Seven-model design — temporally stratified against the MIT 95% claim (Aug 2025):

  GROUP A — Pre-claim controls (training cutoff < July 2025):
    claude_opus   : Claude 3 Opus (Anthropic, Mar 2024, cutoff ~Aug 2023)
    gpt4o         : GPT-4o 2024-11-20 (OpenAI, Nov 2024, cutoff ~Oct 2024)
    gemini_15_pro : Gemini 1.5 Pro (Google, Feb 2024, cutoff ~Nov 2023)
    llama31_405b  : Llama 3.1 405B (Meta/Together.ai, Jul 2024, cutoff ~Dec 2023)

  GROUP B — Post-claim experimental (training cutoff > Aug 2025):
    gemini3       : Gemini 3 (Google, Nov 2025, cutoff ~Aug 2025)
    gpt52         : GPT-5.2 (OpenAI, Dec 2025, cutoff ~Sep 2025)
    claude46      : Claude Sonnet 4.6 (Anthropic, Feb 2026, cutoff ~Oct 2025)

  SECONDARY (optional, no same-lab temporal pair):
    mistral       : Mistral Large 2 (Mistral, Jul 2024, cutoff ~Feb 2024)

Inference parameters (methodology-critical):
  temperature = 0   — greedy decoding; measures modal parametric memory
  top_p       = 1.0 — no nucleus truncation
  max_tokens  = 1024

All model IDs and inference parameters are read from environment variables.
See .env.example for full documentation and verification notes.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ── Inference parameters (read from env; documented in .env.example) ──────────

DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
DEFAULT_TOP_P = float(os.getenv("LLM_TOP_P", "1.0"))
DEFAULT_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# ── Model IDs (read from env; see .env.example for verification notes) ────────

_CLAUDE_OPUS_MODEL = os.getenv("CLAUDE_OPUS_MODEL", "claude-3-opus-20240229")
_GPT4O_MODEL = os.getenv("GPT4O_MODEL", "gpt-4o-2024-11-20")
_GEMINI_15_PRO_MODEL = os.getenv("GEMINI_15_PRO_MODEL", "gemini-1.5-pro")
_LLAMA31_MODEL = os.getenv("LLAMA31_MODEL", "meta-llama/Llama-3.1-405B-Instruct")
_GEMINI3_MODEL = os.getenv("GEMINI3_MODEL", "gemini-3-pro")
_GPT52_MODEL = os.getenv("GPT52_MODEL", "gpt-5.2")
_CLAUDE_SONNET46_MODEL = os.getenv("CLAUDE_SONNET46_MODEL", "claude-sonnet-4-6")
_MISTRAL_LARGE2_MODEL = os.getenv("MISTRAL_LARGE2_MODEL", "mistral-large-2407")

# ── Model registry ────────────────────────────────────────────────────────────

# Primary Phase 3 model keys (Group A + Group B)
PHASE3_GROUP_A = ["claude_opus", "gpt4o", "gemini_15_pro", "llama31_405b"]
PHASE3_GROUP_B = ["gemini3", "gpt52", "claude46"]
PHASE3_MODELS = PHASE3_GROUP_A + PHASE3_GROUP_B

# Secondary / optional
SECONDARY_MODELS = ["mistral"]

# All supported keys
SUPPORTED_MODELS = PHASE3_MODELS + SECONDARY_MODELS

# Backward-compatible aliases (used by legacy code and tests)
LEGACY_ALIASES = {
    "claude": "claude_opus",
    "gpt4": "gpt4o",
    "gemini": "gemini_15_pro",
    "llama3": "llama31_405b",
}

MODEL_DISPLAY_NAMES = {
    "claude_opus": "Claude 3 Opus",
    "gpt4o": "GPT-4o (2024-11-20)",
    "gemini_15_pro": "Gemini 1.5 Pro",
    "llama31_405b": "Llama 3.1 405B",
    "gemini3": "Gemini 3",
    "gpt52": "GPT-5.2",
    "claude46": "Claude Sonnet 4.6",
    "mistral": "Mistral Large 2",
    # Legacy aliases
    "claude": "Claude 3 Opus",
    "gpt4": "GPT-4o (2024-11-20)",
    "gemini": "Gemini 1.5 Pro",
    "llama3": "Llama 3.1 405B",
}

MODEL_GROUPS = {
    "claude_opus": "A",
    "gpt4o": "A",
    "gemini_15_pro": "A",
    "llama31_405b": "A",
    "gemini3": "B",
    "gpt52": "B",
    "claude46": "B",
    "mistral": "secondary",
}

MODEL_TRAINING_CUTOFFS = {
    "claude_opus": "~2023-08",
    "gpt4o": "~2024-10",
    "gemini_15_pro": "~2023-11",
    "llama31_405b": "~2023-12",
    "gemini3": "~2025-08",
    "gpt52": "~2025-09",
    "claude46": "~2025-10",
    "mistral": "~2024-02",
}

# ── Query functions ───────────────────────────────────────────────────────────


def query_claude_opus(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    messages = [{"role": "user", "content": prompt}]
    kwargs = {
        "model": _CLAUDE_OPUS_MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
    }
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text


def query_gpt4o(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=_GPT4O_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content


def query_gemini_15_pro(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(full_prompt, generation_config=generation_config)
    return response.text


def query_llama31_405b(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    from together import Together
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    # Together.ai requires temperature > 0 for some models; use 0.001 as effective zero
    effective_temp = max(temperature, 0.001) if temperature == 0 else temperature
    response = client.chat.completions.create(
        model=_LLAMA31_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=effective_temp,
        top_p=top_p,
    )
    return response.choices[0].message.content


def query_gemini3(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Query Gemini 3 (Group B: post-claim experimental).
    Verify GEMINI3_MODEL ID in .env before running Phase 3.
    Gemini experiment: VULNERABLE to single-source RAG fabrication (Germain 2026).
    """
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    model = genai.GenerativeModel(_GEMINI3_MODEL)
    response = model.generate_content(full_prompt, generation_config=generation_config)
    return response.text


def query_gpt52(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Query GPT-5.2 (Group B: post-claim experimental).
    Verify GPT52_MODEL ID in .env before running Phase 3.
    Germain experiment: VULNERABLE to single-source RAG fabrication.
    """
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=_GPT52_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content


def query_claude46(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Query Claude Sonnet 4.6 (Group B: post-claim experimental).
    Germain experiment: RESISTANT (did not reproduce fabricated content).
    Self-referential note: this is also the model running the research infrastructure.
    """
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    messages = [{"role": "user", "content": prompt}]
    kwargs = {
        "model": _CLAUDE_SONNET46_MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
    }
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text


def query_mistral(
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Secondary model — not in primary Phase 3 set (no same-lab temporal pair)."""
    from mistralai import Mistral
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.complete(
        model=_MISTRAL_LARGE2_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content


QUERY_FUNCS = {
    "claude_opus": query_claude_opus,
    "gpt4o": query_gpt4o,
    "gemini_15_pro": query_gemini_15_pro,
    "llama31_405b": query_llama31_405b,
    "gemini3": query_gemini3,
    "gpt52": query_gpt52,
    "claude46": query_claude46,
    "mistral": query_mistral,
    # Backward-compatible aliases
    "claude": query_claude_opus,
    "gpt4": query_gpt4o,
    "gemini": query_gemini_15_pro,
    "llama3": query_llama31_405b,
}


# ── Main query interface ──────────────────────────────────────────────────────


def query_model(
    model: str,
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    retry: int = 3,
    delay: float = 2.0,
    cache_dir: Optional[Path] = None,
) -> dict:
    """
    Query a model and return a structured response dict.
    Optionally caches responses to disk by prompt hash.

    Inference defaults (methodology-critical):
      temperature = 0   — greedy decoding; measures modal parametric memory
      top_p       = 1.0 — no nucleus truncation
      max_tokens  = 1024

    Override defaults here or via LLM_TEMPERATURE / LLM_TOP_P env vars.
    For sensitivity analysis only, use temperature=0.7 on a 10% subset.
    """
    # Resolve legacy aliases
    resolved = LEGACY_ALIASES.get(model, model)
    assert resolved in QUERY_FUNCS, (
        f"Unknown model: {model!r}. "
        f"Supported: {SUPPORTED_MODELS} or legacy aliases: {list(LEGACY_ALIASES)}"
    )

    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_key = hashlib.md5(
            f"{resolved}::{system}::{prompt}::t={temperature}::p={top_p}".encode()
        ).hexdigest()
        cache_file = cache_dir / f"{resolved}_{cache_key}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)

    result = {
        "model": resolved,
        "model_display": MODEL_DISPLAY_NAMES.get(resolved, resolved),
        "model_group": MODEL_GROUPS.get(resolved, "unknown"),
        "training_cutoff_est": MODEL_TRAINING_CUTOFFS.get(resolved, "unknown"),
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "prompt": prompt,
        "system": system,
        "response": None,
        "error": None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    for attempt in range(retry):
        try:
            result["response"] = QUERY_FUNCS[resolved](
                prompt, system,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            break
        except Exception as e:
            result["error"] = str(e)
            if attempt < retry - 1:
                time.sleep(delay * (attempt + 1))

    if cache_dir and result["response"]:
        with open(cache_file, "w") as f:
            json.dump(result, f, indent=2)

    return result
