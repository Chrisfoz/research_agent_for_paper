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
    """
    Amplification chain for MIT 95% case.
    Source: MIT NANDA 'The GenAI Divide' (July 2025), Challapally, Pease, Raskar, Chari.
    Report removed from MIT domain September 16, 2025.
    """
    chain = AmplificationChain(
        case_id="mit_95",
        key_observations=[
            "Model output is typically faithful to sources — models are NOT hallucinating.",
            "Epistemic failure lies upstream in the source ecosystem, not in generation.",
            "LLM confidence calibrated to corpus prevalence, not to source quality or removal.",
            "Source document removed by MIT; claim persists in 200+ derivative articles.",
            "87% of Type A/B responses: unhedged assertion expected (based on corpus prevalence).",
            "Only correct attribution includes MIT NANDA / Challapally et al. with scope caveat.",
            "Debunking content increases claim prevalence (Pfisterer et al. 2025).",
            "Toby Stuart (UC Berkeley-Haas): 'a taken-for-granted fact overnight' -- CEA in action.",
        ],
        cross_case_comparison=(
            "Structurally identical to Russia case: both driven by frequency-bias mechanism. "
            "MIT case: prestige-driven amplification of weak methodology. "
            "Russia case: adversarial/deliberate corpus saturation. "
            "Training objective cannot distinguish the two."
        ),
    )

    chain.add_stage(ChainStage(
        stage=1,
        actor="MIT NANDA / MIT Media Lab individual researchers",
        transformation=(
            "Preliminary non-peer-reviewed report published (July 2025). "
            "Released under MIT institutional affiliation."
        ),
        epistemic_effect=(
            "Weak source (52 interviews, narrow 6-month P&L window) given MIT institutional halo. "
            "Low circulation until Fortune article August 18."
        ),
        evidence="docs/v0.1_State_of_AI_in_Business_2025_Report.pdf",
        key_finding="'95% of organizations are getting zero return' -- from preliminary individual research",
    ))
    chain.add_stage(ChainStage(
        stage=2,
        actor="Fortune magazine (August 18, 2025)",
        transformation=(
            "Headline: 'MIT report: 95% of generative AI pilots at companies are failing'. "
            "Narrow enterprise/custom-tool finding stated as universal industry conclusion."
        ),
        epistemic_effect=(
            "Viral spread within hours. MIT institutional framing drives uncritical reproduction. "
            "Caused stock drops in NVIDIA, ARM, Palantir."
        ),
        evidence="fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/",
        key_finding="Report goes viral; 'MIT' + '95%' framing established in media cycle",
    ))
    chain.add_stage(ChainStage(
        stage=3,
        actor="Forbes, Axios, Legal.io, DemandLab, CloudFactory, 200+ outlets (Aug 21 -- Sep 2025)",
        transformation=(
            "Cross-outlet amplification within 72 hours of Fortune article. "
            "Methodology caveats and scope limitations absent from all derivative coverage."
        ),
        epistemic_effect=(
            "200+ derivative articles. D/P ratio exceeds 200:1 within two weeks. "
            "Claim established as corpus consensus before MIT can respond."
        ),
        evidence="Forbes (Hill, Aug 21); search results show 200+ articles",
        key_finding="D/P ratio 200:1 -- fastest amplification documented in this research",
    ))
    chain.add_stage(ChainStage(
        stage=4,
        actor="MIT officials (September 2025)",
        transformation=(
            "MIT distances from report. Kimberly Allen: 'unpublished, non-peer-reviewed work.' "
            "Prof Tod Machover: 'preliminary piece by individual researchers.' "
            "Report removed from MIT domain September 16, 2025."
        ),
        epistemic_effect=(
            "Correction asymmetry: retraction reaches a fraction of original audience. "
            "Debunking articles restate '95%' to refute it -- increasing corpus prevalence "
            "(Pfisterer et al. 2025: repetition generates credibility signal regardless of valence). "
            "The claim now outlives its source."
        ),
        evidence="MIT media relations statement; report removal confirmed Sep 16, 2025",
        key_finding="Classic correction asymmetry -- source removed, claim immortalised",
    ))
    chain.add_stage(ChainStage(
        stage=5,
        actor="LLM training corpora (post-August 2025 web crawls)",
        transformation=(
            "200+ derivative articles enter training corpora. "
            "MIT institutional authority preserved in corpus despite source removal."
        ),
        epistemic_effect=(
            "Statistical prevalence converts to high token likelihood. "
            "Frequency-bias mechanism (McKenna et al. 2023) activates at scale."
        ),
        evidence="Frequency-bias mechanism confirmed architecturally; corpus ingestion timing",
        key_finding="Source removed; derivative footprint permanent; CEA loop enters next cycle",
    ))
    chain.add_stage(ChainStage(
        stage=6,
        actor="LLMs (future training cycles, 2026+)",
        transformation=(
            "Frequency bias converts corpus prevalence to confident unhedged assertion. "
            "Models cite 'MIT' as authority; removed report's conclusions persist in weights."
        ),
        epistemic_effect=(
            "Circular epistemic authority loop closed. "
            "No model output will surface report removal or MIT distancing. "
            "This is the mechanism the paper predicts -- demonstrated in real-time."
        ),
        evidence="Phase 3 probing results (current models); CEA model prediction",
        key_finding="Circular authority loop complete and self-reinforcing",
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
