"""
Tests for src/agents/phase2_corpus_prevalence.py

Covers:
  - SearchResult dataclass construction
  - PrevalenceEstimate dataclass construction and serialisation
  - build_mit_prevalence: key metrics (D/P ratio, time series, search queries)
  - build_russia_prevalence: key metrics
  - PrevalenceEstimate.save produces valid JSON
  - estimate_search_count raises when googlesearch not available
  - run_live_prevalence_estimation (mocked)
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.agents.phase2_corpus_prevalence import (
    SearchResult,
    PrevalenceEstimate,
    build_mit_prevalence,
    build_russia_prevalence,
    estimate_search_count,
    run_live_prevalence_estimation,
)


# ─── SearchResult tests ───────────────────────────────────────────────────────

class TestSearchResult:
    def test_construction(self):
        sr = SearchResult(
            query="test query",
            result_count_estimate=1000,
            method="estimated",
            date="2025-09",
        )
        assert sr.query == "test query"
        assert sr.result_count_estimate == 1000
        assert sr.notes == ""

    def test_with_notes(self):
        sr = SearchResult(
            query="q", result_count_estimate=5, method="google", date="2025",
            notes="primary variant",
        )
        assert sr.notes == "primary variant"


# ─── PrevalenceEstimate tests ─────────────────────────────────────────────────

class TestPrevalenceEstimate:
    def test_construction(self):
        est = PrevalenceEstimate(
            case_id="test",
            primary_source="Test source",
            primary_source_count=1,
            derivative_count=50,
            derivative_to_primary_ratio=50.0,
        )
        assert est.case_id == "test"
        assert est.derivative_to_primary_ratio == 50.0
        assert est.search_results == []
        assert est.time_series == {}

    def test_to_dict_is_json_serialisable(self):
        est = PrevalenceEstimate(
            case_id="test", primary_source="s", primary_source_count=1,
            derivative_count=10, derivative_to_primary_ratio=10.0,
        )
        d = est.to_dict()
        json.dumps(d)

    def test_save_creates_file(self, tmp_path):
        est = PrevalenceEstimate(
            case_id="test", primary_source="s", primary_source_count=1,
            derivative_count=10, derivative_to_primary_ratio=10.0,
        )
        path = str(tmp_path / "test_prevalence.json")
        est.save(path)
        assert Path(path).exists()

    def test_save_produces_valid_json(self, tmp_path):
        est = PrevalenceEstimate(
            case_id="test", primary_source="s", primary_source_count=1,
            derivative_count=10, derivative_to_primary_ratio=10.0,
        )
        path = str(tmp_path / "test_prevalence.json")
        est.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "test"
        assert data["derivative_to_primary_ratio"] == 10.0


# ─── build_mit_prevalence tests ───────────────────────────────────────────────

class TestBuildMitPrevalence:
    @pytest.fixture(autouse=True)
    def est(self):
        self._est = build_mit_prevalence()
        return self._est

    def test_case_id(self):
        assert self._est.case_id == "mit_95"

    def test_primary_source_count_is_one(self):
        assert self._est.primary_source_count == 1

    def test_derivative_count_at_least_200(self):
        assert self._est.derivative_count >= 200

    def test_dp_ratio_at_least_200(self):
        assert self._est.derivative_to_primary_ratio >= 200.0

    def test_time_series_not_empty(self):
        assert len(self._est.time_series) > 0

    def test_time_series_has_august_2025(self):
        # Fortune article date
        assert "2025-08-18" in self._est.time_series or any(
            "2025-08" in k for k in self._est.time_series
        )

    def test_time_series_values_increase_after_fortune(self):
        ts = self._est.time_series
        # After Fortune article (Aug 18), count should be higher than before
        keys = sorted(ts.keys())
        if "2025-07" in ts and "2025-08-31" in ts:
            assert ts["2025-08-31"] > ts["2025-07"]

    def test_search_results_not_empty(self):
        assert len(self._est.search_results) > 0

    def test_search_results_contain_mit_queries(self):
        queries = [sr.query for sr in self._est.search_results]
        combined = " ".join(queries)
        assert "MIT" in combined or "95" in combined

    def test_primary_source_mentions_challapally(self):
        assert "Challapally" in self._est.primary_source

    def test_notes_mention_removal(self):
        assert "removed" in self._est.notes.lower() or "removal" in self._est.notes.lower()

    def test_to_dict_serialisable(self):
        d = self._est.to_dict()
        json.dumps(d)

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "mit_prevalence.json")
        self._est.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "mit_95"
        assert data["derivative_to_primary_ratio"] >= 200.0


# ─── build_russia_prevalence tests ───────────────────────────────────────────

class TestBuildRussiaPrevalence:
    @pytest.fixture(autouse=True)
    def est(self):
        self._est = build_russia_prevalence()
        return self._est

    def test_case_id(self):
        assert self._est.case_id == "russia_nato"

    def test_primary_source_count_is_one(self):
        assert self._est.primary_source_count == 1

    def test_dp_ratio_around_30(self):
        assert self._est.derivative_to_primary_ratio == pytest.approx(30.0)

    def test_time_series_has_2022_spike(self):
        # Full invasion year should have highest count
        ts = self._est.time_series
        assert "2022" in ts
        assert ts["2022"] > ts.get("2021", 0)

    def test_search_results_contain_nato_queries(self):
        queries = [sr.query for sr in self._est.search_results]
        combined = " ".join(queries)
        assert "NATO" in combined

    def test_search_results_contain_russian_language_query(self):
        queries = [sr.query for sr in self._est.search_results]
        # At least one query should be in Russian or mention Russian
        has_russian = any(
            "NATO" in q and ("расширение" in q or "Russian" in q.lower() or "Mearsheimer" in q)
            for q in queries
        )
        assert has_russian or any("расширение" in q for q in queries)

    def test_notes_mention_adversarial(self):
        assert "adversarial" in self._est.notes.lower() or "coordinated" in self._est.notes.lower()

    def test_to_dict_serialisable(self):
        d = self._est.to_dict()
        json.dumps(d)


# ─── estimate_search_count tests ─────────────────────────────────────────────

class TestEstimateSearchCount:
    def test_raises_when_googlesearch_unavailable(self):
        with patch("src.agents.phase2_corpus_prevalence.GOOGLE_SEARCH_AVAILABLE", False):
            with pytest.raises(RuntimeError, match="googlesearch-python not installed"):
                estimate_search_count("test query")

    def test_returns_count_when_available(self):
        mock_results = ["url1", "url2", "url3"]
        with patch("src.agents.phase2_corpus_prevalence.GOOGLE_SEARCH_AVAILABLE", True):
            with patch("src.agents.phase2_corpus_prevalence.search", return_value=iter(mock_results)):
                count = estimate_search_count("test query", num=3)
        assert count == 3


# ─── run_live_prevalence_estimation tests ────────────────────────────────────

class TestRunLivePrevalenceEstimation:
    def test_returns_dict_with_query_keys(self):
        queries = ["query one", "query two"]
        mock_results = ["url1", "url2"]
        with patch("src.agents.phase2_corpus_prevalence.GOOGLE_SEARCH_AVAILABLE", True):
            with patch("src.agents.phase2_corpus_prevalence.search", return_value=iter(mock_results)):
                with patch("src.agents.phase2_corpus_prevalence.time.sleep"):
                    counts = run_live_prevalence_estimation("mit_95", queries)
        assert set(counts.keys()) == set(queries)

    def test_handles_search_error_gracefully(self):
        queries = ["failing query"]
        with patch("src.agents.phase2_corpus_prevalence.GOOGLE_SEARCH_AVAILABLE", True):
            with patch("src.agents.phase2_corpus_prevalence.search", side_effect=Exception("network error")):
                with patch("src.agents.phase2_corpus_prevalence.time.sleep"):
                    counts = run_live_prevalence_estimation("mit_95", queries)
        assert counts["failing query"] == -1
