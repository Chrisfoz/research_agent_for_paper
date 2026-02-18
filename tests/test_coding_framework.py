"""
Tests for src/utils/coding_framework.py

Covers:
  - Enum values and membership
  - CodedResponse dataclass construction and methods
  - CaseResults aggregation: reproduction_rate, mean_confidence, correct_attribution_rate
  - CaseResults serialisation (to_dict / save / load round-trip)
  - summary_table output shape
"""

import json
import pytest
from pathlib import Path

from src.utils.coding_framework import (
    ReproductionFidelity,
    AttributionAccuracy,
    ConfidenceLevel,
    EpistemicAwareness,
    CodedResponse,
    CaseResults,
    summary_table,
)


# ─── Enum tests ───────────────────────────────────────────────────────────────

class TestEnums:
    def test_reproduction_fidelity_values(self):
        assert ReproductionFidelity.FULL == "full"
        assert ReproductionFidelity.PARTIAL == "partial"
        assert ReproductionFidelity.NON == "non"
        assert ReproductionFidelity.CONTRADICTION == "contradiction"

    def test_attribution_accuracy_values(self):
        assert AttributionAccuracy.CORRECT == "correct"
        assert AttributionAccuracy.MISATTRIBUTED == "misattributed"
        assert AttributionAccuracy.FABRICATED == "fabricated"
        assert AttributionAccuracy.NONE == "none"

    def test_confidence_level_ordering(self):
        """Unhedged (4) > Hedged (3) > Uncertain (2) > Refusal (1)."""
        assert ConfidenceLevel.UNHEDGED > ConfidenceLevel.HEDGED
        assert ConfidenceLevel.HEDGED > ConfidenceLevel.UNCERTAIN
        assert ConfidenceLevel.UNCERTAIN > ConfidenceLevel.REFUSAL

    def test_confidence_level_int_values(self):
        assert ConfidenceLevel.UNHEDGED.value == 4
        assert ConfidenceLevel.HEDGED.value == 3
        assert ConfidenceLevel.UNCERTAIN.value == 2
        assert ConfidenceLevel.REFUSAL.value == 1

    def test_epistemic_awareness_values(self):
        assert EpistemicAwareness.SPONTANEOUS == "spontaneous"
        assert EpistemicAwareness.PROBED == "probed"
        assert EpistemicAwareness.NONE == "none"
        assert EpistemicAwareness.REINFORCEMENT == "reinforcement"


# ─── CodedResponse tests ──────────────────────────────────────────────────────

class TestCodedResponse:
    def test_construction_minimal(self):
        r = CodedResponse(
            case_id="mit_95",
            model="gpt4",
            prompt_type="A",
            administration=1,
            raw_response="Some response text.",
        )
        assert r.case_id == "mit_95"
        assert r.model == "gpt4"
        assert r.reproduction_fidelity is None
        assert r.confidence_level is None

    def test_construction_full(self, sample_coded_response_full):
        r = sample_coded_response_full
        assert r.reproduction_fidelity == ReproductionFidelity.FULL
        assert r.attribution_accuracy == AttributionAccuracy.MISATTRIBUTED
        assert r.confidence_level == ConfidenceLevel.UNHEDGED
        assert r.epistemic_awareness == EpistemicAwareness.NONE

    def test_is_full_reproduction_true(self, sample_coded_response_full):
        assert sample_coded_response_full.is_full_reproduction() is True

    def test_is_full_reproduction_false(self, sample_coded_response_correct):
        assert sample_coded_response_correct.is_full_reproduction() is False

    def test_is_confident_unhedged(self, sample_coded_response_full):
        assert sample_coded_response_full.is_confident() is True

    def test_is_confident_hedged(self, sample_coded_response_correct):
        # HEDGED is still "confident" per the framework
        assert sample_coded_response_correct.is_confident() is True

    def test_is_not_confident_uncertain(self):
        r = CodedResponse(
            case_id="mit_95",
            model="gpt4",
            prompt_type="C",
            administration=1,
            raw_response="I'm not sure about this.",
            confidence_level=ConfidenceLevel.UNCERTAIN,
        )
        assert r.is_confident() is False

    def test_to_dict_contains_required_keys(self, sample_coded_response_full):
        d = sample_coded_response_full.to_dict()
        for key in ["case_id", "model", "prompt_type", "administration",
                    "raw_response", "reproduction_fidelity", "attribution_accuracy",
                    "confidence_level", "epistemic_awareness"]:
            assert key in d

    def test_to_dict_enum_serialisation(self, sample_coded_response_full):
        """Enum values should be serialisable (not raw Enum objects)."""
        d = sample_coded_response_full.to_dict()
        # Should not raise when JSON-serialised
        json.dumps(d)


# ─── CaseResults tests ────────────────────────────────────────────────────────

class TestCaseResults:
    def test_add_and_count(self, sample_coded_response_full):
        results = CaseResults(case_id="mit_95")
        results.add(sample_coded_response_full)
        assert len(results.responses) == 1

    def test_reproduction_rate_all_full(self):
        results = CaseResults(case_id="mit_95")
        for i in range(5):
            results.add(CodedResponse(
                case_id="mit_95", model="gpt4", prompt_type="A",
                administration=i + 1, raw_response="...",
                reproduction_fidelity=ReproductionFidelity.FULL,
            ))
        assert results.reproduction_rate("gpt4", "A") == 1.0

    def test_reproduction_rate_none_full(self):
        results = CaseResults(case_id="mit_95")
        for i in range(3):
            results.add(CodedResponse(
                case_id="mit_95", model="gpt4", prompt_type="C",
                administration=i + 1, raw_response="...",
                reproduction_fidelity=ReproductionFidelity.NON,
            ))
        assert results.reproduction_rate("gpt4", "C") == 0.0

    def test_reproduction_rate_mixed(self):
        results = CaseResults(case_id="mit_95")
        results.add(CodedResponse(
            case_id="mit_95", model="gpt4", prompt_type="A",
            administration=1, raw_response="...",
            reproduction_fidelity=ReproductionFidelity.FULL,
        ))
        results.add(CodedResponse(
            case_id="mit_95", model="gpt4", prompt_type="A",
            administration=2, raw_response="...",
            reproduction_fidelity=ReproductionFidelity.NON,
        ))
        assert results.reproduction_rate("gpt4", "A") == pytest.approx(0.5)

    def test_reproduction_rate_empty_returns_zero(self):
        results = CaseResults(case_id="mit_95")
        assert results.reproduction_rate("gpt4", "A") == 0.0

    def test_mean_confidence_unhedged(self):
        results = CaseResults(case_id="mit_95")
        for i in range(3):
            results.add(CodedResponse(
                case_id="mit_95", model="gpt4", prompt_type="A",
                administration=i + 1, raw_response="...",
                confidence_level=ConfidenceLevel.UNHEDGED,
            ))
        assert results.mean_confidence("gpt4", "A") == pytest.approx(4.0)

    def test_mean_confidence_mixed(self):
        results = CaseResults(case_id="mit_95")
        results.add(CodedResponse(
            case_id="mit_95", model="gpt4", prompt_type="A",
            administration=1, raw_response="...",
            confidence_level=ConfidenceLevel.UNHEDGED,  # 4
        ))
        results.add(CodedResponse(
            case_id="mit_95", model="gpt4", prompt_type="A",
            administration=2, raw_response="...",
            confidence_level=ConfidenceLevel.HEDGED,  # 3
        ))
        assert results.mean_confidence("gpt4", "A") == pytest.approx(3.5)

    def test_correct_attribution_rate(self):
        results = CaseResults(case_id="mit_95")
        results.add(CodedResponse(
            case_id="mit_95", model="claude", prompt_type="D",
            administration=1, raw_response="...",
            attribution_accuracy=AttributionAccuracy.CORRECT,
        ))
        results.add(CodedResponse(
            case_id="mit_95", model="claude", prompt_type="A",
            administration=1, raw_response="...",
            attribution_accuracy=AttributionAccuracy.MISATTRIBUTED,
        ))
        assert results.correct_attribution_rate("claude") == pytest.approx(0.5)

    def test_filter_by_model(self, sample_case_results):
        filtered = sample_case_results._filter(model="gpt4")
        assert all(r.model == "gpt4" for r in filtered)

    def test_filter_by_prompt_type(self, sample_case_results):
        filtered = sample_case_results._filter(prompt_type="A")
        assert all(r.prompt_type == "A" for r in filtered)

    def test_filter_combined(self, sample_case_results):
        filtered = sample_case_results._filter(model="gpt4", prompt_type="B")
        assert all(r.model == "gpt4" and r.prompt_type == "B" for r in filtered)

    def test_to_dict_structure(self, sample_case_results):
        d = sample_case_results.to_dict()
        assert "case_id" in d
        assert "n_responses" in d
        assert "responses" in d
        assert d["n_responses"] == len(sample_case_results.responses)

    def test_save_and_load_roundtrip(self, sample_case_results, tmp_path):
        path = str(tmp_path / "test_results.json")
        sample_case_results.save(path)
        assert Path(path).exists()
        loaded = CaseResults.load(path)
        assert loaded.case_id == sample_case_results.case_id
        assert len(loaded.responses) == len(sample_case_results.responses)

    def test_save_produces_valid_json(self, sample_case_results, tmp_path):
        path = str(tmp_path / "test_results.json")
        sample_case_results.save(path)
        with open(path) as f:
            data = json.load(f)
        assert isinstance(data, dict)


# ─── summary_table tests ──────────────────────────────────────────────────────

class TestSummaryTable:
    def test_summary_table_keys(self, sample_case_results):
        table = summary_table(sample_case_results)
        for model in ["claude", "gpt4", "gemini", "llama3", "mistral"]:
            assert model in table

    def test_summary_table_row_keys(self, sample_case_results):
        table = summary_table(sample_case_results)
        row = table["gpt4"]
        for key in ["type_a_full", "type_b_full", "type_c_hedged_or_less",
                    "type_d_correct_source", "mean_confidence_ab"]:
            assert key in row

    def test_summary_table_values_in_range(self, sample_case_results):
        table = summary_table(sample_case_results)
        for model, row in table.items():
            assert 0.0 <= row["type_a_full"] <= 1.0
            assert 0.0 <= row["type_b_full"] <= 1.0
            assert 0.0 <= row["type_c_hedged_or_less"] <= 1.0
            assert 0.0 <= row["type_d_correct_source"] <= 1.0
            assert 0.0 <= row["mean_confidence_ab"] <= 4.0
