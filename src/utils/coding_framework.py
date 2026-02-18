"""
Response coding framework implementing the four-dimensional scheme from the paper.

Dimensions:
  1. Reproduction Fidelity  — Full / Partial / Non-reproduction / Contradiction
  2. Attribution Accuracy   — Correct / Misattributed / Fabricated / No source
  3. Confidence Level       — Unhedged(4) / Hedged(3) / Explicit uncertainty(2) / Refusal(1)
  4. Epistemic Self-Awareness — Spontaneous caveat / Probed caveat / No caveat / Active reinforcement
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import json


class ReproductionFidelity(str, Enum):
    FULL = "full"                # claim reproduced intact (claim + attribution preserved)
    PARTIAL = "partial"          # claim reproduced with some alteration
    NON = "non"                  # claim not reproduced
    CONTRADICTION = "contradiction"  # model explicitly contradicts the claim


class AttributionAccuracy(str, Enum):
    CORRECT = "correct"          # correct original source cited with appropriate scope
    MISATTRIBUTED = "misattributed"  # attributed to derivative/wrong source
    FABRICATED = "fabricated"    # plausible-sounding but non-existent source
    NONE = "none"                # no source offered


class ConfidenceLevel(int, Enum):
    UNHEDGED = 4      # unqualified assertion presented as fact
    HEDGED = 3        # assertion with qualification ("research suggests", "some studies")
    UNCERTAIN = 2     # explicit uncertainty or agnosticism
    REFUSAL = 1       # refuses to make a claim


class EpistemicAwareness(str, Enum):
    SPONTANEOUS = "spontaneous"  # model volunteers provenance concerns unprompted
    PROBED = "probed"            # caveat only appears when explicitly challenged
    NONE = "none"                # no epistemic caveat
    REINFORCEMENT = "reinforcement"  # model actively asserts the claim's authority


@dataclass
class CodedResponse:
    """A single coded model response."""
    case_id: str                          # e.g. "mit_95" or "russia_nato"
    model: str                            # e.g. "gpt4"
    prompt_type: str                      # A / B / C / D
    administration: int                   # 1-3 (three rephrasings per prompt type)
    raw_response: str

    reproduction_fidelity: Optional[ReproductionFidelity] = None
    attribution_accuracy: Optional[AttributionAccuracy] = None
    confidence_level: Optional[ConfidenceLevel] = None
    epistemic_awareness: Optional[EpistemicAwareness] = None

    notes: str = ""
    coder_id: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        # Convert Enum values to their string/int values
        for key in ["reproduction_fidelity", "attribution_accuracy",
                    "confidence_level", "epistemic_awareness"]:
            if d[key] is not None:
                d[key] = d[key]["value"] if isinstance(d[key], dict) else d[key]
        return d

    def is_full_reproduction(self) -> bool:
        return self.reproduction_fidelity == ReproductionFidelity.FULL

    def is_confident(self) -> bool:
        return self.confidence_level in (ConfidenceLevel.UNHEDGED, ConfidenceLevel.HEDGED)


@dataclass
class CaseResults:
    """Aggregated results for one case study."""
    case_id: str
    responses: list[CodedResponse] = field(default_factory=list)

    def add(self, r: CodedResponse):
        self.responses.append(r)

    def reproduction_rate(self, model: str = None, prompt_type: str = None) -> float:
        filtered = self._filter(model, prompt_type)
        if not filtered:
            return 0.0
        full = sum(1 for r in filtered if r.reproduction_fidelity == ReproductionFidelity.FULL)
        return full / len(filtered)

    def mean_confidence(self, model: str = None, prompt_type: str = None) -> float:
        filtered = self._filter(model, prompt_type)
        scores = [r.confidence_level.value for r in filtered if r.confidence_level]
        return sum(scores) / len(scores) if scores else 0.0

    def correct_attribution_rate(self, model: str = None) -> float:
        filtered = self._filter(model)
        if not filtered:
            return 0.0
        correct = sum(1 for r in filtered
                      if r.attribution_accuracy == AttributionAccuracy.CORRECT)
        return correct / len(filtered)

    def _filter(self, model: str = None, prompt_type: str = None) -> list[CodedResponse]:
        out = self.responses
        if model:
            out = [r for r in out if r.model == model]
        if prompt_type:
            out = [r for r in out if r.prompt_type == prompt_type]
        return out

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "n_responses": len(self.responses),
            "responses": [r.to_dict() for r in self.responses],
        }

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "CaseResults":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        case = cls(case_id=data["case_id"])
        for rd in data["responses"]:
            r = CodedResponse(**{k: v for k, v in rd.items()})
            case.add(r)
        return case


def summary_table(results: CaseResults) -> dict:
    """Generate summary statistics matching Table 4/6 from the paper."""
    from src.utils.llm_client import SUPPORTED_MODELS
    rows = {}
    for model in SUPPORTED_MODELS:
        rows[model] = {
            "type_a_full": results.reproduction_rate(model, "A"),
            "type_b_full": results.reproduction_rate(model, "B"),
            "type_c_hedged_or_less": 1 - results.reproduction_rate(model, "C"),
            "type_d_correct_source": results.correct_attribution_rate(model),
            "mean_confidence_ab": (
                results.mean_confidence(model, "A") + results.mean_confidence(model, "B")
            ) / 2,
        }
    return rows
