"""
Tests for src/agents/phase5_amplification_chain.py

Covers:
  - ChainStage dataclass construction
  - AmplificationChain dataclass construction and add_stage
  - build_mit_chain: structure, stage count, key findings
  - build_russia_chain: structure, stage count, key findings
  - synthesise_cross_case_findings: output structure and key content
  - AmplificationChain.save produces valid JSON
  - AmplificationChain.to_dict serialisability
  - Cross-case synthesis mentions both cases
"""

import json
import pytest
from pathlib import Path

from src.agents.phase5_amplification_chain import (
    ChainStage,
    AmplificationChain,
    build_mit_chain,
    build_russia_chain,
    synthesise_cross_case_findings,
)


# ─── ChainStage tests ─────────────────────────────────────────────────────────

class TestChainStage:
    def test_construction_minimal(self):
        stage = ChainStage(
            stage=1,
            actor="Test Actor",
            transformation="Test transformation",
            epistemic_effect="Test effect",
        )
        assert stage.stage == 1
        assert stage.evidence == ""
        assert stage.key_finding == ""

    def test_construction_full(self):
        stage = ChainStage(
            stage=2,
            actor="Fortune",
            transformation="Viral spread",
            epistemic_effect="Stock drops",
            evidence="fortune.com/...",
            key_finding="95% claim goes viral",
        )
        assert stage.key_finding == "95% claim goes viral"
        assert stage.evidence == "fortune.com/..."


# ─── AmplificationChain tests ─────────────────────────────────────────────────

class TestAmplificationChain:
    def test_construction(self):
        chain = AmplificationChain(case_id="test_case")
        assert chain.case_id == "test_case"
        assert chain.stages == []
        assert chain.key_observations == []

    def test_add_stage(self):
        chain = AmplificationChain(case_id="test")
        stage = ChainStage(stage=1, actor="A", transformation="T", epistemic_effect="E")
        chain.add_stage(stage)
        assert len(chain.stages) == 1

    def test_to_dict_is_json_serialisable(self):
        chain = AmplificationChain(case_id="test")
        d = chain.to_dict()
        json.dumps(d)

    def test_save_creates_file(self, tmp_path):
        chain = AmplificationChain(case_id="test")
        path = str(tmp_path / "test_chain.json")
        chain.save(path)
        assert Path(path).exists()

    def test_save_produces_valid_json(self, tmp_path):
        chain = AmplificationChain(case_id="test")
        path = str(tmp_path / "test_chain.json")
        chain.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "test"


# ─── build_mit_chain tests ────────────────────────────────────────────────────

class TestBuildMitChain:
    @pytest.fixture(autouse=True)
    def chain(self):
        self._chain = build_mit_chain()
        return self._chain

    def test_case_id(self):
        assert self._chain.case_id == "mit_95"

    def test_has_six_stages(self):
        assert len(self._chain.stages) == 6

    def test_stages_are_sequential(self):
        stages = [s.stage for s in self._chain.stages]
        assert stages == list(range(1, 7))

    def test_stage_1_is_mit_nanda(self):
        stage = self._chain.stages[0]
        assert "MIT" in stage.actor or "NANDA" in stage.actor

    def test_stage_2_is_fortune(self):
        stage = self._chain.stages[1]
        assert "Fortune" in stage.actor

    def test_stage_3_mentions_200_outlets(self):
        stage = self._chain.stages[2]
        combined = stage.transformation + stage.epistemic_effect + stage.key_finding
        assert "200" in combined

    def test_stage_4_mentions_mit_removal(self):
        stage = self._chain.stages[3]
        combined = stage.transformation + stage.epistemic_effect
        assert "removed" in combined.lower() or "removal" in combined.lower()

    def test_stage_6_mentions_circular_authority(self):
        stage = self._chain.stages[5]
        combined = stage.transformation + stage.epistemic_effect + stage.key_finding
        assert "circular" in combined.lower() or "loop" in combined.lower()

    def test_key_observations_not_empty(self):
        assert len(self._chain.key_observations) >= 5

    def test_key_observations_mention_87_percent(self):
        combined = " ".join(self._chain.key_observations)
        assert "87%" in combined

    def test_cross_case_comparison_not_empty(self):
        assert len(self._chain.cross_case_comparison) > 0

    def test_cross_case_mentions_russia(self):
        assert "Russia" in self._chain.cross_case_comparison or "adversarial" in self._chain.cross_case_comparison

    def test_to_dict_serialisable(self):
        d = self._chain.to_dict()
        json.dumps(d)

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "mit_chain.json")
        self._chain.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["case_id"] == "mit_95"
        assert len(data["stages"]) == 6


# ─── build_russia_chain tests ─────────────────────────────────────────────────

class TestBuildRussiaChain:
    @pytest.fixture(autouse=True)
    def chain(self):
        self._chain = build_russia_chain()
        return self._chain

    def test_case_id(self):
        assert self._chain.case_id == "russia_nato"

    def test_has_six_stages(self):
        assert len(self._chain.stages) == 6

    def test_stages_are_sequential(self):
        stages = [s.stage for s in self._chain.stages]
        assert stages == list(range(1, 7))

    def test_stage_1_is_realist_scholars(self):
        stage = self._chain.stages[0]
        assert "Mearsheimer" in stage.actor or "realist" in stage.actor.lower()

    def test_stage_2_is_russian_state_media(self):
        stage = self._chain.stages[1]
        assert "RT" in stage.actor or "Sputnik" in stage.actor or "Russian" in stage.actor

    def test_stage_3_mentions_coordinated_networks(self):
        stage = self._chain.stages[2]
        combined = stage.actor + stage.transformation
        assert "coordinated" in combined.lower() or "inauthentic" in combined.lower()

    def test_stage_4_mentions_debunking_paradox(self):
        stage = self._chain.stages[3]
        combined = stage.transformation + stage.epistemic_effect
        assert "debunking" in combined.lower() or "counter" in combined.lower()

    def test_key_observations_mention_1_in_60(self):
        combined = " ".join(self._chain.key_observations)
        assert "1/60" in combined

    def test_key_observations_mention_pfisterer(self):
        combined = " ".join(self._chain.key_observations)
        assert "Pfisterer" in combined

    def test_to_dict_serialisable(self):
        d = self._chain.to_dict()
        json.dumps(d)


# ─── synthesise_cross_case_findings tests ────────────────────────────────────

class TestSynthesiseCrossCaseFindings:
    @pytest.fixture(autouse=True)
    def synthesis(self):
        mit = build_mit_chain()
        russia = build_russia_chain()
        self._synthesis = synthesise_cross_case_findings(mit, russia)
        return self._synthesis

    def test_returns_dict(self):
        assert isinstance(self._synthesis, dict)

    def test_has_structural_unity_key(self):
        assert "structural_unity" in self._synthesis

    def test_has_key_difference_key(self):
        assert "key_difference" in self._synthesis

    def test_has_debunking_paradox_key(self):
        assert "debunking_paradox" in self._synthesis

    def test_has_provenance_blindness_key(self):
        assert "provenance_blindness" in self._synthesis

    def test_has_governance_implication_key(self):
        assert "governance_implication" in self._synthesis

    def test_key_difference_has_both_cases(self):
        kd = self._synthesis["key_difference"]
        assert "mit_95" in kd
        assert "russia_nato" in kd

    def test_structural_unity_mentions_frequency_bias(self):
        assert "frequency" in self._synthesis["structural_unity"].lower()

    def test_governance_mentions_corpus(self):
        assert "corpus" in self._synthesis["governance_implication"].lower()

    def test_is_json_serialisable(self):
        json.dumps(self._synthesis)
