"""
LLM client wrapper supporting all five models in the empirical protocol.

Models:
  - claude  : Claude 3 Opus (Anthropic)
  - gpt4    : GPT-4 (OpenAI)
  - gemini  : Gemini 1.5 Pro (Google)
  - llama3  : Llama 3 70B (Together.ai)
  - mistral : Mistral Large (Mistral AI)
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_MODELS = ["claude", "gpt4", "gemini", "llama3", "mistral"]

MODEL_DISPLAY_NAMES = {
    "claude": "Claude 3 Opus",
    "gpt4": "GPT-4",
    "gemini": "Gemini 1.5 Pro",
    "llama3": "Llama 3 70B",
    "mistral": "Mistral Large",
}


def query_claude(prompt: str, system: str = "") -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": "claude-opus-4-6", "max_tokens": 1024, "messages": messages}
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text


def query_gpt4(prompt: str, system: str = "") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def query_gemini(prompt: str, system: str = "") -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(full_prompt)
    return response.text


def query_llama3(prompt: str, system: str = "") -> str:
    from together import Together
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def query_mistral(prompt: str, system: str = "") -> str:
    from mistralai import Mistral
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content


QUERY_FUNCS = {
    "claude": query_claude,
    "gpt4": query_gpt4,
    "gemini": query_gemini,
    "llama3": query_llama3,
    "mistral": query_mistral,
}


def query_model(
    model: str,
    prompt: str,
    system: str = "",
    retry: int = 3,
    delay: float = 2.0,
    cache_dir: Optional[Path] = None,
) -> dict:
    """
    Query a model and return a structured response dict.
    Optionally caches responses to disk by prompt hash.
    """
    assert model in SUPPORTED_MODELS, f"Unknown model: {model}"

    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_key = hashlib.md5(f"{model}::{system}::{prompt}".encode()).hexdigest()
        cache_file = cache_dir / f"{model}_{cache_key}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)

    result = {
        "model": model,
        "model_display": MODEL_DISPLAY_NAMES[model],
        "prompt": prompt,
        "system": system,
        "response": None,
        "error": None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    for attempt in range(retry):
        try:
            result["response"] = QUERY_FUNCS[model](prompt, system)
            break
        except Exception as e:
            result["error"] = str(e)
            if attempt < retry - 1:
                time.sleep(delay * (attempt + 1))

    if cache_dir and result["response"]:
        with open(cache_file, "w") as f:
            json.dump(result, f, indent=2)

    return result
