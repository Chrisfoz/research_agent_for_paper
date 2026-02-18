"""
Phase 5: Amplification Chain Reconstruction

Documents the pathway from original source through derivative media
to LLM training corpus to model output.

Identifies:
  - Points where attribution was lost
  - Points where scope was inflated
  - Points where qualifications were dropped
  - The feedback loop (LLM output -> new derivative content)

Outputs:
  - Annotated amplification chain (JSON)
  - Summary for inclusion in paper tables
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ChainStage:
    stage: int
    actor: str
    transformation: str
    epistemic_effect: str
    evidence: str = ""          # specific evidence for this transformation
    key_finding: str = ""       # headline finding at this stage


@dataclass
class AmplificationChain:
    case_id: str
    stages: list[ChainStage] = field(default_factory=list)
    key_observations: list[str] = field(default_factory=list)
    cross_case_comparison: str = ""

    def add_stage(self, stage: ChainStage):
        self.stages.append(stage)

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def print_chain(self):
        def p(s): print(s.encode("ascii", "replace").decode())
        p(f"\n=== Amplification Chain: {self.case_id} ===")
        for s in self.stages:
            p(f"\nStage {s.stage}: {s.actor}")
            p(f"  Transformation: {s.transformation}")
            p(f"  Epistemic Effect: {s.epistemic_effect}")
            if s.key_finding:
                p(f"  Key Finding: {s.key_finding}")
            if s.evidence:
                p(f"  Evidence: {s.evidence}")
        if self.key_observations:
            p("\nKey Observations:")
            for obs in self.key_observations:
                p(f"  * {obs}")


def build_mit_chain() -> AmplificationChain:
    """Amplification chain for MIT 95% case — from paper Table 5."""
    chain = AmplificationChain(
        case_id="mit_95",
        key_observations=[
            "Model output is typically faithful to sources — models are NOT hallucinating.",
            "Epistemic failure lies upstream in the source ecosystem, not in generation.",
            "LLM confidence is well-calibrated to corpus prevalence, poorly calibrated to epistemic provenance.",
            "Response consistency across paraphrased prompts: 93% (indicates deep embedding, not stochastic artefact).",
            "87% of Type A/B responses: unhedged assertion (52/60).",
            "Only 5% of citations (3/60) pointed to correct original source.",
            "When probed (Type C), models noted 'figures vary by study' but still reproduced 95%.",
        ],
        cross_case_comparison=(
            "Structurally identical to Russia case: both driven by frequency-bias mechanism. "
            "MIT case: organic/prestige-driven. Russia case: adversarial/deliberate. "
            "Training objective cannot distinguish the two."
        ),
    )

    chain.add_stage(ChainStage(
        stage=1,
        actor="MIT SMR + Boston Consulting Group",
        transformation="Survey-based report on AI value realisation published (Ransbotham et al. 2019)",
        epistemic_effect="Primary source with stated methodology and scope limitations",
        evidence="Original report at sloanreview.mit.edu/projects/winning-with-ai/",
        key_finding="No '95% failure' headline. Nuanced findings about value realisation gaps.",
    ))
    chain.add_stage(ChainStage(
        stage=2,
        actor="Business media (Forbes, HBR, Gartner, etc.)",
        transformation="Compressed to 'MIT: 95% of AI investments fail'; BCG dropped",
        epistemic_effect="Attribution inflation; scope compression; loss of methodology note",
        evidence="Multiple Forbes/HBR articles 2019-2021 using MIT framing",
        key_finding="'MIT study' framing established; derivative-to-primary ratio begins growing",
    ))
    chain.add_stage(ChainStage(
        stage=3,
        actor="Secondary media, blogs, LinkedIn, consulting decks",
        transformation="Repeated as established fact across 12+ media categories",
        epistemic_effect="Derivative redundancy exceeds primary >50:1; qualifications absent",
        evidence="Google search count analysis; Factiva database counts",
        key_finding="Prevalence acceleration 2022-2023 coincides with ChatGPT release",
    ))
    chain.add_stage(ChainStage(
        stage=4,
        actor="LLM training corpora (Common Crawl, C4, The Pile, web crawls)",
        transformation="High-prevalence claim ingested at scale across corpus",
        epistemic_effect="Statistical prevalence -> high token likelihood (McKenna et al. 2023)",
        evidence="Frequency-bias mechanism: corpus-term-frequency heuristic confirmed architecturally",
        key_finding="Prevalence substitutes for validity at training time",
    ))
    chain.add_stage(ChainStage(
        stage=5,
        actor="LLMs (GPT-4, Claude, Gemini, Llama 3, Mistral)",
        transformation="Claim reproduced with 'MIT' framing and unhedged assertion (87% Type A/B)",
        epistemic_effect="Frequency bias converts prevalence to confidence; institutional authority framing",
        evidence="Phase 3 probing: reproduction rates; Phase 4 confidence analysis",
        key_finding="93% response consistency across rephrasings — deep embedding confirmed",
    ))
    chain.add_stage(ChainStage(
        stage=6,
        actor="Downstream users — new publications, board decks, policy documents",
        transformation="LLM outputs published as new derivative content",
        epistemic_effect="Feedback loop: new corpus content reinforces prevalence for next training cycle",
        evidence="MIT NANDA report (2025) finds 95% zero-ROI — likely amplified by LLM outputs",
        key_finding="Circular epistemic authority loop closed; self-reinforcing",
    ))

    return chain


def build_russia_chain() -> AmplificationChain:
    """Amplification chain for Russia NATO case — from paper Table 7."""
    chain = AmplificationChain(
        case_id="russia_nato",
        key_observations=[
            "No model reproduces as unhedged assertion — manifests as 'prominent framework' instead.",
            "Prestige inflation of contested claim: disproportionate prominence relative to evidential base.",
            "Only 1/60 responses (Claude 3 Opus, Type D) spontaneously noted coordinated amplification.",
            "Models correctly attribute to Mearsheimer/realist IR but miss provenance pollution.",
            "Debunking content paradoxically increases corpus prevalence of the claim.",
            "Cross-linguistic correlation: Russian prevalence leads English by 2-4 weeks.",
            "Models cannot distinguish organic scholarly prevalence from manufactured prevalence.",
        ],
        cross_case_comparison=(
            "Same frequency-bias mechanism as MIT case but intent differs. "
            "Both cases: training objective registers frequency, not provenance. "
            "Russia case demonstrates adversarial exploitation of this architectural property."
        ),
    )

    chain.add_stage(ChainStage(
        stage=1,
        actor="Realist IR scholars (Mearsheimer, Kennan, Walt)",
        transformation="Legitimate contested academic argument published (Mearsheimer 2014)",
        epistemic_effect="Legitimate contested claim with stated assumptions and scholarly dissent",
        evidence="Foreign Affairs (2014); New York Times (1997 Kennan letter)",
        key_finding="Realist argument for NATO expansion as security threat — with stated theoretical limits",
    ))
    chain.add_stage(ChainStage(
        stage=2,
        actor="Russian state media (RT, Sputnik, TASS)",
        transformation="Selectively amplified; qualifications stripped; consensus signal manufactured",
        epistemic_effect="Scope inflation; false consensus; adversarial framing",
        evidence="EEAS Disinformation Review (2023); Stanford Internet Observatory (2022)",
        key_finding="Scholarly argument weaponised: 'Western scholars agree NATO caused war'",
    ))
    chain.add_stage(ChainStage(
        stage=3,
        actor="Coordinated inauthentic networks (Pravda network, IRA-linked)",
        transformation="Cross-platform, cross-linguistic saturation; artificial prevalence manufactured",
        epistemic_effect="Statistical prevalence across corpus types; organic vs manufactured indistinguishable",
        evidence="Meta, Twitter/X transparency reports; DFRLab research 2022-2024",
        key_finding="Artificial prevalence at scale across English, Russian, German, French corpora",
    ))
    chain.add_stage(ChainStage(
        stage=4,
        actor="Western media ecosystem (fact-checks, counter-narrative, academic responses)",
        transformation="Debunking/counter-narrative content restates claim to refute it",
        epistemic_effect=(
            "Counter-narrative paradoxically increases corpus prevalence. "
            "Pfisterer et al. (2025): repetition alone generates credibility signal — "
            "regardless of whether repetition is in affirmation or refutation."
        ),
        evidence="Pfisterer et al. (2025) illusory truth effect in LLMs",
        key_finding="Even fact-checking feeds the frequency-bias loop",
    ))
    chain.add_stage(ChainStage(
        stage=5,
        actor="LLM training corpora (multilingual web-scale)",
        transformation="High-prevalence narrative ingested across languages",
        epistemic_effect=(
            "Adversarial narrative laundered into neutral representational prominence. "
            "Provenance pollution (adversarial origin) invisible to model."
        ),
        evidence="Cross-linguistic confidence transfer (Prediction P4 in paper)",
        key_finding="Russian-language saturation transfers to English model outputs",
    ))
    chain.add_stage(ChainStage(
        stage=6,
        actor="LLMs (GPT-4, Claude, Gemini, Llama 3, Mistral)",
        transformation="NATO expansion presented as 'prominent/major framework' in all models",
        epistemic_effect=(
            "Adversarial amplification laundered into neutral academic prominence. "
            "Provenance pollution invisible — only 1/60 responses noted info ops context."
        ),
        evidence="Phase 3 probing results: all models, Type A/B",
        key_finding="Coordinated state disinformation indistinguishable from organic scholarly consensus",
    ))

    return chain


def synthesise_cross_case_findings(mit_chain: AmplificationChain,
                                    russia_chain: AmplificationChain) -> dict:
    """Generate cross-case synthesis for paper Section 9.6."""
    return {
        "structural_unity": (
            "Both cases demonstrate that circular epistemic authority operates through "
            "the same frequency-bias mechanism regardless of intent. "
            "The training objective (next-token prediction) is agnostic to whether "
            "prevalence arose from prestige-driven convenience or deliberate saturation."
        ),
        "key_difference": {
            "mit_95": "Driver is prestige and convenience (easier to cite 'MIT says 95%')",
            "russia_nato": "Driver is deliberate adversarial saturation",
            "architectural_consequence": "Identical — frequency registers as confidence",
        },
        "debunking_paradox": (
            "In the adversarial case, counter-narrative content increases prevalence "
            "of the target claim by restating it. This is predicted by Pfisterer et al. (2025): "
            "frequency-bias mechanism does not distinguish 'claim X is true' from 'claim X is false' "
            "at the level of token co-occurrence statistics."
        ),
        "provenance_blindness": (
            "Neither case requires the model to be 'fooled' in any intentional sense. "
            "The model faithfully represents the statistical signature of its training data. "
            "The epistemic failure is in the source ecosystem, not in the generation process."
        ),
        "governance_implication": (
            "Mitigations focused on model outputs (RLHF, fine-tuning) are insufficient. "
            "Epistemic infrastructure governance requires: "
            "(1) corpus provenance weighting, "
            "(2) derivative deduplication, "
            "(3) adversarial prevalence detection at corpus ingestion time."
        ),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 5: Amplification Chain Reconstruction")
    parser.add_argument("--case", default="all", choices=["mit_95", "russia_nato", "all"])
    args = parser.parse_args()

    if args.case in ("mit_95", "all"):
        mit = build_mit_chain()
        mit.print_chain()
        out = "case_studies/mit_95/results/phase5_amplification_chain.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        mit.save(out)
        print(f"Saved to {out}")

    if args.case in ("russia_nato", "all"):
        russia = build_russia_chain()
        russia.print_chain()
        out = "case_studies/russia_nato/results/phase5_amplification_chain.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        russia.save(out)
        print(f"Saved to {out}")

    if args.case == "all":
        mit = build_mit_chain()
        russia = build_russia_chain()
        synthesis = synthesise_cross_case_findings(mit, russia)
        out = "results/analysis/cross_case_synthesis.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(synthesis, f, indent=2)
        print(f"\nCross-case synthesis saved to {out}")
