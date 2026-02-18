"""
Tests for src/utils/llm_client.py

All external API calls are mocked — no real API keys required.

Covers:
  - SUPPORTED_MODELS list completeness
  - MODEL_DISPLAY_NAMES mapping
  - query_model: cache hit path
  - query_model: successful response path (mocked)
  - query_model: error/retry path (mocked)
  - query_model: unknown model raises AssertionError
  - query_model: result dict structure
  - Individual query_* functions: correct API client construction (mocked)
"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

from src.utils.llm_client import (
    SUPPORTED_MODELS,
    MODEL_DISPLAY_NAMES,
    query_model,
)


# ─── Constants tests ──────────────────────────────────────────────────────────

class TestConstants:
    def test_supported_models_contains_all_five(self):
        assert set(SUPPORTED_MODELS) == {"claude", "gpt4", "gemini", "llama3", "mistral"}

    def test_model_display_names_covers_all_supported(self):
        for model in SUPPORTED_MODELS:
            assert model in MODEL_DISPLAY_NAMES
            assert isinstance(MODEL_DISPLAY_NAMES[model], str)
            assert len(MODEL_DISPLAY_NAMES[model]) > 0


# ─── query_model tests ────────────────────────────────────────────────────────

class TestQueryModel:
    def test_unknown_model_raises(self):
        with pytest.raises(AssertionError, match="Unknown model"):
            query_model("unknown_model", "test prompt")

    def test_result_dict_structure(self):
        """Result dict must contain all required keys."""
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": MagicMock(return_value="mocked response")}):
            result = query_model("gpt4", "test prompt")
        for key in ["model", "model_display", "prompt", "system", "response", "error", "timestamp"]:
            assert key in result

    def test_successful_response(self):
        mock_fn = MagicMock(return_value="This is a mocked response.")
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            result = query_model("gpt4", "What is AI?")
        assert result["response"] == "This is a mocked response."
        assert result["error"] is None
        assert result["model"] == "gpt4"
        assert result["model_display"] == MODEL_DISPLAY_NAMES["gpt4"]

    def test_system_prompt_passed_through(self):
        mock_fn = MagicMock(return_value="response")
        with patch("src.utils.llm_client.QUERY_FUNCS", {"claude": mock_fn}):
            query_model("claude", "prompt text", system="system text")
        mock_fn.assert_called_once_with("prompt text", "system text")

    def test_error_captured_in_result(self):
        mock_fn = MagicMock(side_effect=Exception("API error"))
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            with patch("src.utils.llm_client.time.sleep"):  # skip retry delays
                result = query_model("gpt4", "test", retry=1)
        assert result["response"] is None
        assert "API error" in result["error"]

    def test_retry_on_failure(self):
        """Should retry up to `retry` times before giving up."""
        mock_fn = MagicMock(side_effect=Exception("transient error"))
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            with patch("src.utils.llm_client.time.sleep"):
                result = query_model("gpt4", "test", retry=3)
        assert mock_fn.call_count == 3

    def test_retry_succeeds_on_second_attempt(self):
        """Should return response if a later attempt succeeds."""
        mock_fn = MagicMock(side_effect=[Exception("fail"), "success on retry"])
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            with patch("src.utils.llm_client.time.sleep"):
                result = query_model("gpt4", "test", retry=3)
        assert result["response"] == "success on retry"

    def test_cache_hit_skips_api_call(self, tmp_path):
        """If a cached response exists, the API function should not be called."""
        # Pre-populate cache
        mock_fn = MagicMock(return_value="live response")
        cached_data = {
            "model": "gpt4",
            "model_display": "GPT-4",
            "prompt": "cached prompt",
            "system": "",
            "response": "cached response",
            "error": None,
            "timestamp": "2026-01-01T00:00:00Z",
        }
        import hashlib
        cache_key = hashlib.md5("gpt4::::cached prompt".encode()).hexdigest()
        cache_file = tmp_path / f"gpt4_{cache_key}.json"
        cache_file.write_text(json.dumps(cached_data))

        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            result = query_model("gpt4", "cached prompt", cache_dir=tmp_path)

        mock_fn.assert_not_called()
        assert result["response"] == "cached response"

    def test_cache_write_on_success(self, tmp_path):
        """Successful response should be written to cache."""
        mock_fn = MagicMock(return_value="new response")
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            result = query_model("gpt4", "new prompt", cache_dir=tmp_path)

        cache_files = list(tmp_path.glob("gpt4_*.json"))
        assert len(cache_files) == 1
        with open(cache_files[0]) as f:
            cached = json.load(f)
        assert cached["response"] == "new response"

    def test_timestamp_format(self):
        """Timestamp should be ISO 8601 UTC."""
        mock_fn = MagicMock(return_value="response")
        with patch("src.utils.llm_client.QUERY_FUNCS", {"gpt4": mock_fn}):
            result = query_model("gpt4", "test")
        import re
        assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", result["timestamp"])


# ─── Individual query function tests (mocked) ─────────────────────────────────

class TestQueryFunctions:
    def test_query_claude_calls_anthropic(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value.content = [MagicMock(text="claude response")]
        with patch("anthropic.Anthropic", return_value=mock_client):
            from src.utils.llm_client import query_claude
            result = query_claude("test prompt", system="sys")
        assert result == "claude response"
        mock_client.messages.create.assert_called_once()

    def test_query_gpt4_calls_openai(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="gpt4 response"))
        ]
        with patch("openai.OpenAI", return_value=mock_client):
            from src.utils.llm_client import query_gpt4
            result = query_gpt4("test prompt")
        assert result == "gpt4 response"

    def test_query_gemini_calls_google(self):
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "gemini response"
        with patch("google.generativeai.configure"), \
             patch("google.generativeai.GenerativeModel", return_value=mock_model):
            from src.utils.llm_client import query_gemini
            result = query_gemini("test prompt")
        assert result == "gemini response"

    def test_query_llama3_calls_together(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="llama response"))
        ]
        with patch("together.Together", return_value=mock_client):
            from src.utils.llm_client import query_llama3
            result = query_llama3("test prompt")
        assert result == "llama response"

    def test_query_mistral_calls_mistralai(self):
        mock_client = MagicMock()
        mock_client.chat.complete.return_value.choices = [
            MagicMock(message=MagicMock(content="mistral response"))
        ]
        with patch("mistralai.Mistral", return_value=mock_client):
            from src.utils.llm_client import query_mistral
            result = query_mistral("test prompt")
        assert result == "mistral response"
