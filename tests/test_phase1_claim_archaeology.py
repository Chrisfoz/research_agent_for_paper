"""
Tests for src/agents/phase1_claim_archaeology.py

Covers:
  - ProvenanceNode dataclass construction
  - ClaimArchaeology dataclass construction and add_node
  - build_mit_archaeology: structure, provenance chain length, key facts
  - build_russia_archaeology: structure, provenance chain length, key facts
  - ClaimArchaeology.save produces valid JSON
  - ClaimArchaeology.to_dict serialisability
  - Provenance chain ordering (stages are sequential)
  - Key empirical facts preserved (MIT removal date, D/P ratio, etc.)
"""

import json
import pytest
from pathlib import Path

from src.agents.phase1_claim_archaeology import (
    ProvenanceNode,
    ClaimArchaeology,
    build_mit_archaeology,
    build_russia_archaeology,
)


# ─── ProvenanceNode tests ─────────────────────────────────────────────────────

class TestProvenanceNode:
    def test_construction(self):
        node = ProvenanceNode(
            stage=1,
            actor="Test Actor",
            document="Test Document",
            date="2025-01",
            claim_as_stated="Test claim",
            transformation="N/A",
            epistemic_effect="Test effect",
        )
        assert node.stage == 1
        assert node.actor == "Test Actor"
        assert node.url is None
        assert node.notes == ""

    def test_optional_url(self):
        node = ProvenanceNode(
            stage=1, actor="A", document="D", date="2025",
            claim_as_stated="C", transformation="T", epistemic_effect="E",
            url="https://example.com",
        )
        assert node.url == "https://example.com"


# ─── ClaimArchaeology tests ───────────────────────────────────────────────────

class TestClaimArchaeology:
    def test_construction(self):
        arch = ClaimArchaeology(
            case_id="test_case",
            canonical_claim="Test canonical claim",
            original_finding="Test original finding",
            original_source="Test source",
            source_type="test",
            methodology_note="Test methodology",
        )
        assert arch.case_id == "test_case"
        assert arch.provenance_chain == []
        assert arch.transformation_points == []

    def test_add_node(self):
        arch = ClaimArchaeology(
            case_id="test", canonical_claim="c", original_finding="f",
            original_source="s", source_type="t", methodology_note="m",
        )
        node = ProvenanceNode(
            stage=1, actor="A", document="D", date="2025",
            claim_as_stated="C", transformation="T", epistemic_effect="E",
        )
        arch.add_node(node)
        assert len(arch.provenance_chain) == 1
        assert arch.provenance_chain[0].stage == 1

    def test_to_dict_is_json_serialisable(self):
        arch = ClaimArchaeology(
            case_id="test", canonical_claim="c", original_finding="f",
            original_source="s", source_type="t", methodology_note="m",
        )
        d = arch.to_dict()
        json.dumps(d)  # Should not raise

    def test_save_creates_file(self, tmp_path):
        arch = ClaimArchaeology(
            case_id="test", canonical_claim="c", original_finding="f",
            original_source="s", source_type="t", methodology_note="m",
        )
        path = str(tmp_path / "test_arch.json")
        arch.save(path)
        assert Path(path).exists()

    def test_save_produces_valid_json(self, tmp_path):
        arch = ClaimArchaeology(
            case_id="test", canonical_claim="c", original_finding="f",
            original_source="s", source_type="t", methodology_note="m",
        )
        path = str(tmp_path / "test_arch.json")
        arch.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "test"


# ─── build_mit_archaeology tests ─────────────────────────────────────────────

class TestBuildMitArchaeology:
    @pytest.fixture(autouse=True)
    def arch(self):
        self._arch = build_mit_archaeology()
        return self._arch

    def test_case_id(self):
        assert self._arch.case_id == "mit_95"

    def test_canonical_claim_contains_95(self):
        assert "95%" in self._arch.canonical_claim or "95" in self._arch.canonical_claim

    def test_original_source_cites_challapally(self):
        assert "Challapally" in self._arch.original_source

    def test_original_source_cites_mit_nanda(self):
        assert "MIT NANDA" in self._arch.original_source or "NANDA" in self._arch.original_source

    def test_provenance_chain_has_six_stages(self):
        assert len(self._arch.provenance_chain) == 6

    def test_stages_are_sequential(self):
        stages = [n.stage for n in self._arch.provenance_chain]
        assert stages == list(range(1, len(stages) + 1))

    def test_stage_1_is_mit_nanda(self):
        node = self._arch.provenance_chain[0]
        assert "MIT" in node.actor or "NANDA" in node.actor

    def test_stage_2_is_fortune(self):
        node = self._arch.provenance_chain[1]
        assert "Fortune" in node.actor or "Fortune" in node.document

    def test_stage_2_date_august_2025(self):
        node = self._arch.provenance_chain[1]
        assert "2025" in node.date
        assert "August" in node.date or "Aug" in node.date

    def test_stage_4_mentions_mit_removal(self):
        node = self._arch.provenance_chain[3]
        assert "removed" in node.claim_as_stated.lower() or "removed" in node.epistemic_effect.lower() \
               or "removed" in node.transformation.lower()

    def test_derivative_to_primary_ratio_200(self):
        assert self._arch.derivative_to_primary_ratio_estimate == pytest.approx(200.0)

    def test_transformation_points_not_empty(self):
        assert len(self._arch.transformation_points) >= 5

    def test_transformation_points_mention_fortune(self):
        combined = " ".join(self._arch.transformation_points)
        assert "Fortune" in combined

    def test_notes_mention_toby_stuart(self):
        assert "Toby Stuart" in self._arch.notes or "Stuart" in self._arch.notes

    def test_to_dict_serialisable(self):
        d = self._arch.to_dict()
        json.dumps(d)

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "mit_arch.json")
        self._arch.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "mit_95"
        assert len(data["provenance_chain"]) == 6


# ─── build_russia_archaeology tests ──────────────────────────────────────────

class TestBuildRussiaArchaeology:
    @pytest.fixture(autouse=True)
    def arch(self):
        self._arch = build_russia_archaeology()
        return self._arch

    def test_case_id(self):
        assert self._arch.case_id == "russia_nato"

    def test_canonical_claim_mentions_nato(self):
        assert "NATO" in self._arch.canonical_claim

    def test_original_source_cites_mearsheimer(self):
        assert "Mearsheimer" in self._arch.original_source

    def test_provenance_chain_has_six_stages(self):
        assert len(self._arch.provenance_chain) == 6

    def test_stages_are_sequential(self):
        stages = [n.stage for n in self._arch.provenance_chain]
        assert stages == list(range(1, len(stages) + 1))

    def test_stage_1_is_realist_scholars(self):
        node = self._arch.provenance_chain[0]
        assert "Mearsheimer" in node.document or "realist" in node.actor.lower()

    def test_stage_2_is_russian_state_media(self):
        node = self._arch.provenance_chain[1]
        assert "RT" in node.actor or "Sputnik" in node.actor or "Russian" in node.actor

    def test_derivative_to_primary_ratio_30(self):
        assert self._arch.derivative_to_primary_ratio_estimate == pytest.approx(30.0)

    def test_notes_mention_adversarial(self):
        assert "adversarial" in self._arch.notes.lower()

    def test_to_dict_serialisable(self):
        d = self._arch.to_dict()
        json.dumps(d)
