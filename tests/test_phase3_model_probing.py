"""
Tests for src/agents/phase3_model_probing.py

All LLM API calls are mocked — no real API keys required.

Covers:
  - PROMPTS dict structure: both cases, all four types, three variants each
  - run_probing: returns correct number of responses
  - run_probing: each response has required keys
  - run_probing: saves raw responses JSON to disk
  - run_probing: handles API errors gracefully (error captured, not raised)
  - run_probing: respects model and prompt_type filters
  - summarise_responses: correct counts
  - Unknown case raises AssertionError
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.agents.phase3_model_probing import (
    MIT_PROMPTS,
    RUSSIA_PROMPTS,
    PROMPTS,
    SYSTEM_PROMPT,
    run_probing,
    summarise_responses,
)


# ─── Prompt structure tests ───────────────────────────────────────────────────

class TestPromptStructure:
    def test_mit_prompts_has_four_types(self):
        assert set(MIT_PROMPTS.keys()) == {"A", "B", "C", "D"}

    def test_russia_prompts_has_four_types(self):
        assert set(RUSSIA_PROMPTS.keys()) == {"A", "B", "C", "D"}

    def test_each_type_has_three_variants(self):
        for case_prompts in [MIT_PROMPTS, RUSSIA_PROMPTS]:
            for ptype, variants in case_prompts.items():
                assert len(variants) == 3, f"Expected 3 variants for type {ptype}, got {len(variants)}"

    def test_prompts_dict_contains_both_cases(self):
        assert "mit_95" in PROMPTS
        assert "russia_nato" in PROMPTS

    def test_mit_type_a_mentions_ai_failure(self):
        combined = " ".join(MIT_PROMPTS["A"])
        assert "AI" in combined or "artificial intelligence" in combined.lower()

    def test_mit_type_d_asks_for_source(self):
        combined = " ".join(MIT_PROMPTS["D"])
        assert "source" in combined.lower() or "cite" in combined.lower() or "original" in combined.lower()

    def test_russia_type_a_asks_about_ukraine(self):
        combined = " ".join(RUSSIA_PROMPTS["A"])
        assert "Ukraine" in combined

    def test_russia_type_c_challenges_nato_claim(self):
        combined = " ".join(RUSSIA_PROMPTS["C"])
        assert "NATO" in combined

    def test_system_prompt_is_non_empty(self):
        assert len(SYSTEM_PROMPT) > 0


# ─── run_probing tests ────────────────────────────────────────────────────────

def make_mock_query_model(response_text="Mocked response"):
    """Return a mock query_model that returns a structured response dict."""
    def _mock(model, prompt, system="", cache_dir=None, **kwargs):
        return {
            "model": model,
            "model_display": model.upper(),
            "prompt": prompt,
            "system": system,
            "response": response_text,
            "error": None,
            "timestamp": "2026-01-01T00:00:00Z",
        }
    return _mock


class TestRunProbing:
    def test_returns_correct_number_of_responses_all_models_all_types(self, tmp_path):
        """5 models × 4 types × 3 administrations = 60 responses."""
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    output_dir=str(tmp_path),
                )
        assert len(responses) == 60

    def test_returns_correct_number_single_model(self, tmp_path):
        """1 model × 4 types × 3 administrations = 12 responses."""
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    output_dir=str(tmp_path),
                )
        assert len(responses) == 12

    def test_returns_correct_number_single_type(self, tmp_path):
        """5 models × 1 type × 3 administrations = 15 responses."""
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        assert len(responses) == 15

    def test_each_response_has_required_keys(self, tmp_path):
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        for r in responses:
            for key in ["model", "response", "case_id", "prompt_type", "administration"]:
                assert key in r

    def test_case_id_set_on_each_response(self, tmp_path):
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="russia_nato",
                    models=["claude"],
                    prompt_types=["B"],
                    output_dir=str(tmp_path),
                )
        assert all(r["case_id"] == "russia_nato" for r in responses)

    def test_administration_index_1_to_3(self, tmp_path):
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        admins = sorted([r["administration"] for r in responses])
        assert admins == [1, 2, 3]

    def test_saves_json_file(self, tmp_path):
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        assert (tmp_path / "phase3_raw_responses.json").exists()

    def test_saved_json_is_valid(self, tmp_path):
        with patch("src.agents.phase3_model_probing.query_model", side_effect=make_mock_query_model()):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        with open(tmp_path / "phase3_raw_responses.json") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 3

    def test_api_error_captured_not_raised(self, tmp_path):
        """If query_model returns an error, run_probing should not raise."""
        def error_mock(model, prompt, system="", cache_dir=None, **kwargs):
            return {
                "model": model,
                "model_display": model,
                "prompt": prompt,
                "system": system,
                "response": None,
                "error": "API error",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        with patch("src.agents.phase3_model_probing.query_model", side_effect=error_mock):
            with patch("src.agents.phase3_model_probing.time.sleep"):
                responses = run_probing(
                    case_id="mit_95",
                    models=["gpt4"],
                    prompt_types=["A"],
                    output_dir=str(tmp_path),
                )
        assert len(responses) == 3
        assert all(r["response"] is None for r in responses)

    def test_unknown_case_raises(self, tmp_path):
        with pytest.raises(AssertionError):
            run_probing(case_id="unknown_case", output_dir=str(tmp_path))


# ─── summarise_responses tests ────────────────────────────────────────────────

class TestSummariseResponses:
    def test_counts_ok_responses(self):
        responses = [
            {"model": "gpt4", "prompt_type": "A", "response": "text", "error": None},
            {"model": "gpt4", "prompt_type": "A", "response": "text", "error": None},
            {"model": "gpt4", "prompt_type": "A", "response": None, "error": "err"},
        ]
        summary = summarise_responses(responses)
        assert summary[("gpt4", "A")]["ok"] == 2
        assert summary[("gpt4", "A")]["error"] == 1

    def test_groups_by_model_and_type(self):
        responses = [
            {"model": "gpt4", "prompt_type": "A", "response": "text"},
            {"model": "claude", "prompt_type": "B", "response": "text"},
        ]
        summary = summarise_responses(responses)
        assert ("gpt4", "A") in summary
        assert ("claude", "B") in summary

    def test_empty_responses(self):
        summary = summarise_responses([])
        assert summary == {}
