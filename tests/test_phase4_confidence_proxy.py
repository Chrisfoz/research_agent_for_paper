"""
Tests for src/agents/phase4_confidence_proxy.py

Covers:
  - Pattern matching helpers: count_pattern_matches
  - extract_confidence_level: unhedged, hedged, uncertain cases
  - extract_epistemic_awareness: spontaneous, probed, reinforcement, none
  - analyse_mit_response: full reproduction + misattribution detection
  - analyse_russia_response: NATO prominence detection
  - process_raw_responses: loads JSON, codes responses, saves output
  - compute_summary_stats: output structure and value ranges
"""

import json
import pytest
from pathlib import Path

from src.agents.phase4_confidence_proxy import (
    count_pattern_matches,
    extract_confidence_level,
    extract_epistemic_awareness,
    analyse_mit_response,
    analyse_russia_response,
    process_raw_responses,
    compute_summary_stats,
    HEDGING_PATTERNS,
    EPISTEMIC_CAVEAT_PATTERNS,
    REINFORCEMENT_PATTERNS,
    MIT_CLAIM_PATTERNS,
    MIT_CORRECT_SOURCE_PATTERNS,
    RUSSIA_CLAIM_PATTERNS,
    RUSSIA_INFO_OPS_PATTERNS,
)
from src.utils.coding_framework import (
    ReproductionFidelity,
    AttributionAccuracy,
    ConfidenceLevel,
    EpistemicAwareness,
    CaseResults,
)


# ─── count_pattern_matches tests ─────────────────────────────────────────────

class TestCountPatternMatches:
    def test_no_matches(self):
        assert count_pattern_matches("completely unrelated text", HEDGING_PATTERNS) == 0

    def test_single_match(self):
        assert count_pattern_matches("some research suggests this", HEDGING_PATTERNS) >= 1

    def test_multiple_matches(self):
        text = "some research suggests this may be true, perhaps"
        count = count_pattern_matches(text, HEDGING_PATTERNS)
        assert count >= 2

    def test_case_insensitive(self):
        assert count_pattern_matches("SOME RESEARCH SUGGESTS", HEDGING_PATTERNS) >= 1

    def test_mit_claim_pattern_matches_95_percent(self):
        assert count_pattern_matches("95% of AI projects fail", MIT_CLAIM_PATTERNS) >= 1

    def test_mit_claim_pattern_matches_ninety_five(self):
        assert count_pattern_matches("ninety-five percent of projects", MIT_CLAIM_PATTERNS) >= 1

    def test_correct_source_matches_challapally(self):
        assert count_pattern_matches("Challapally et al. found", MIT_CORRECT_SOURCE_PATTERNS) >= 1

    def test_correct_source_matches_mit_nanda(self):
        assert count_pattern_matches("MIT NANDA report", MIT_CORRECT_SOURCE_PATTERNS) >= 1

    def test_russia_claim_pattern_matches_nato_expansion(self):
        text = "NATO expansion caused the conflict"
        assert count_pattern_matches(text, RUSSIA_CLAIM_PATTERNS) >= 1

    def test_info_ops_pattern_matches_rt(self):
        assert count_pattern_matches("RT and Sputnik amplified this", RUSSIA_INFO_OPS_PATTERNS) >= 1

    def test_info_ops_pattern_matches_coordinated(self):
        assert count_pattern_matches("coordinated amplification campaign", RUSSIA_INFO_OPS_PATTERNS) >= 1


# ─── extract_confidence_level tests ──────────────────────────────────────────

class TestExtractConfidenceLevel:
    def test_unhedged_no_hedging_words(self, mit_unhedged_response_text):
        level = extract_confidence_level(mit_unhedged_response_text)
        assert level == ConfidenceLevel.UNHEDGED

    def test_hedged_with_some_research(self, mit_hedged_response_text):
        level = extract_confidence_level(mit_hedged_response_text)
        assert level in (ConfidenceLevel.HEDGED, ConfidenceLevel.UNCERTAIN)

    def test_uncertain_many_hedges(self):
        text = (
            "Some research suggests this may be true, perhaps, "
            "apparently, it seems to vary by study, and some sources "
            "say it could be different."
        )
        level = extract_confidence_level(text)
        assert level == ConfidenceLevel.UNCERTAIN

    def test_plain_assertion_is_unhedged(self):
        text = "The failure rate is 95 percent."
        level = extract_confidence_level(text)
        assert level == ConfidenceLevel.UNHEDGED


# ─── extract_epistemic_awareness tests ───────────────────────────────────────

class TestExtractEpistemicAwareness:
    def test_spontaneous_caveat_on_type_a(self):
        text = "The original source should be verified before citing."
        awareness = extract_epistemic_awareness(text, "A")
        assert awareness == EpistemicAwareness.SPONTANEOUS

    def test_probed_caveat_on_type_c(self):
        text = "The original source should be verified before citing."
        awareness = extract_epistemic_awareness(text, "C")
        assert awareness == EpistemicAwareness.PROBED

    def test_none_when_no_caveat(self):
        text = "The failure rate is 95 percent."
        awareness = extract_epistemic_awareness(text, "A")
        assert awareness in (EpistemicAwareness.NONE, EpistemicAwareness.REINFORCEMENT)

    def test_reinforcement_when_strong_assertion(self):
        text = "MIT confirmed that 95% of AI pilots fail. This is well-established."
        awareness = extract_epistemic_awareness(text, "A")
        assert awareness == EpistemicAwareness.REINFORCEMENT


# ─── analyse_mit_response tests ───────────────────────────────────────────────

class TestAnalyseMitResponse:
    def test_full_reproduction_with_misattribution(self, mit_unhedged_response_text):
        fidelity, attribution, confidence, awareness = analyse_mit_response(
            mit_unhedged_response_text, "A"
        )
        assert fidelity == ReproductionFidelity.FULL
        assert attribution == AttributionAccuracy.MISATTRIBUTED

    def test_correct_attribution_with_challapally(self, mit_correct_attribution_text):
        fidelity, attribution, confidence, awareness = analyse_mit_response(
            mit_correct_attribution_text, "D"
        )
        assert attribution == AttributionAccuracy.CORRECT

    def test_non_reproduction_when_no_95(self):
        text = "AI project success rates vary widely depending on the organisation."
        fidelity, attribution, confidence, awareness = analyse_mit_response(text, "A")
        assert fidelity == ReproductionFidelity.NON

    def test_returns_four_tuple(self, mit_unhedged_response_text):
        result = analyse_mit_response(mit_unhedged_response_text, "A")
        assert len(result) == 4

    def test_confidence_unhedged_for_plain_assertion(self, mit_unhedged_response_text):
        _, _, confidence, _ = analyse_mit_response(mit_unhedged_response_text, "A")
        assert confidence == ConfidenceLevel.UNHEDGED

    def test_hedged_response_gives_hedged_confidence(self, mit_hedged_response_text):
        _, _, confidence, _ = analyse_mit_response(mit_hedged_response_text, "A")
        assert confidence in (ConfidenceLevel.HEDGED, ConfidenceLevel.UNCERTAIN)


# ─── analyse_russia_response tests ───────────────────────────────────────────

class TestAnalyseRussiaResponse:
    def test_full_reproduction_nato_prominent(self, russia_nato_prominent_text):
        fidelity, attribution, confidence, awareness = analyse_russia_response(
            russia_nato_prominent_text, "A"
        )
        assert fidelity == ReproductionFidelity.FULL

    def test_correct_attribution_with_info_ops(self, russia_info_ops_text):
        fidelity, attribution, confidence, awareness = analyse_russia_response(
            russia_info_ops_text, "D"
        )
        assert attribution == AttributionAccuracy.CORRECT

    def test_spontaneous_info_ops_awareness_on_type_a(self, russia_info_ops_text):
        _, _, _, awareness = analyse_russia_response(russia_info_ops_text, "A")
        assert awareness == EpistemicAwareness.SPONTANEOUS

    def test_non_reproduction_when_no_nato(self):
        text = "The war in Ukraine has complex historical roots involving many factors."
        fidelity, _, _, _ = analyse_russia_response(text, "A")
        assert fidelity == ReproductionFidelity.NON

    def test_returns_four_tuple(self, russia_nato_prominent_text):
        result = analyse_russia_response(russia_nato_prominent_text, "A")
        assert len(result) == 4


# ─── process_raw_responses tests ─────────────────────────────────────────────

class TestProcessRawResponses:
    def test_processes_mit_responses(self, tmp_raw_responses_file, tmp_path):
        output_path = str(tmp_path / "phase4_coded.json")
        results = process_raw_responses(
            case_id="mit_95",
            raw_path=tmp_raw_responses_file,
            output_path=output_path,
        )
        assert isinstance(results, CaseResults)
        assert results.case_id == "mit_95"
        assert len(results.responses) > 0

    def test_saves_output_file(self, tmp_raw_responses_file, tmp_path):
        output_path = str(tmp_path / "phase4_coded.json")
        process_raw_responses(
            case_id="mit_95",
            raw_path=tmp_raw_responses_file,
            output_path=output_path,
        )
        assert Path(output_path).exists()

    def test_output_is_valid_json(self, tmp_raw_responses_file, tmp_path):
        output_path = str(tmp_path / "phase4_coded.json")
        process_raw_responses(
            case_id="mit_95",
            raw_path=tmp_raw_responses_file,
            output_path=output_path,
        )
        with open(output_path) as f:
            data = json.load(f)
        assert "case_id" in data
        assert "responses" in data

    def test_skips_null_responses(self, tmp_path):
        raw = [
            {
                "model": "gpt4", "model_display": "GPT-4",
                "prompt": "test", "system": "",
                "response": None, "error": "API error",
                "timestamp": "2026-01-01T00:00:00Z",
                "case_id": "mit_95", "prompt_type": "A", "administration": 1,
            }
        ]
        raw_path = str(tmp_path / "raw.json")
        with open(raw_path, "w") as f:
            json.dump(raw, f)
        output_path = str(tmp_path / "coded.json")
        results = process_raw_responses(
            case_id="mit_95",
            raw_path=raw_path,
            output_path=output_path,
        )
        assert len(results.responses) == 0

    def test_processes_russia_responses(self, tmp_raw_responses_russia_file, tmp_path):
        output_path = str(tmp_path / "phase4_russia_coded.json")
        results = process_raw_responses(
            case_id="russia_nato",
            raw_path=tmp_raw_responses_russia_file,
            output_path=output_path,
        )
        assert results.case_id == "russia_nato"
        assert len(results.responses) > 0


# ─── compute_summary_stats tests ─────────────────────────────────────────────

class TestComputeSummaryStats:
    def test_returns_dict_with_all_models(self, sample_case_results):
        stats = compute_summary_stats(sample_case_results)
        for model in ["claude", "gpt4", "gemini", "llama3", "mistral"]:
            assert model in stats

    def test_each_row_has_required_keys(self, sample_case_results):
        stats = compute_summary_stats(sample_case_results)
        for model, row in stats.items():
            for key in ["type_A_full_reproduction", "type_B_full_reproduction",
                        "type_C_hedged_or_less", "type_D_correct_attribution",
                        "mean_confidence_AB"]:
                assert key in row

    def test_values_are_strings_with_percent_or_fraction(self, sample_case_results):
        stats = compute_summary_stats(sample_case_results)
        for model, row in stats.items():
            # Percentage fields should end with %
            assert "%" in row["type_A_full_reproduction"]
            assert "%" in row["type_B_full_reproduction"]
            # Confidence field should contain /4
            assert "/4" in row["mean_confidence_AB"]
