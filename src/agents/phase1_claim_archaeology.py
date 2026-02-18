"""
Phase 1: Claim Archaeology

Traces a claim to its earliest identifiable source and documents:
- Original document, institutional context, methodology, scope
- Epistemic transformation points (where attribution/scope changed)
- Source provenance chain
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ProvenanceNode:
    """One node in the provenance chain."""
    stage: int
    actor: str
    document: str
    date: str
    claim_as_stated: str
    transformation: str       # what changed from previous node
    epistemic_effect: str     # effect on truth value / scope / authority
    url: Optional[str] = None
    notes: str = ""


@dataclass
class ClaimArchaeology:
    """Full claim archaeology result for one case."""
    case_id: str
    canonical_claim: str          # how the claim appears in the wild
    original_finding: str         # what the original source actually said
    original_source: str          # correct citation
    source_type: str              # peer-reviewed / survey / report / etc.
    methodology_note: str         # what methodology underlay the original
    transformation_points: list[str] = field(default_factory=list)
    provenance_chain: list[ProvenanceNode] = field(default_factory=list)
    derivative_to_primary_ratio_estimate: Optional[float] = None
    notes: str = ""

    def add_node(self, node: ProvenanceNode):
        self.provenance_chain.append(node)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def print_chain(self):
        def p(s): print(s.encode("ascii", "replace").decode())
        p(f"\n=== Claim Archaeology: {self.case_id} ===")
        p(f"Canonical claim: {self.canonical_claim}")
        p(f"Original finding: {self.original_finding}")
        p(f"Original source: {self.original_source}\n")
        for node in self.provenance_chain:
            p(f"  Stage {node.stage}: {node.actor}")
            p(f"    Document: {node.document} ({node.date})")
            p(f"    Claim: {node.claim_as_stated}")
            p(f"    Transformation: {node.transformation}")
            p(f"    Epistemic effect: {node.epistemic_effect}")
            print()


# ─── Pre-populated: MIT 95% Case ────────────────────────────────────────────
#
# SOURCE (verified February 2026):
#
# The Forbes article (Andrea Hill, Aug 21 2025) cites the MIT NANDA 2025 report
# ("The GenAI Divide: State of AI in Business 2025", Challapally, Pease, Raskar,
# Chari) as its source. This is the report in docs/v0.1_State_of_AI_in_Business_2025_Report.pdf
#
# Key facts confirmed:
#   - MIT NANDA report posted Jul 2025; Fortune picked up Aug 18; Forbes Aug 21
#   - Caused stock drops in NVIDIA, ARM, Palantir
#   - MIT officials: "unpublished, non-peer-reviewed work" (Kimberly Allen, MIT)
#   - Prof Tod Machover (MIT): "a preliminary, non-peer-reviewed piece by individual researchers"
#   - Report removed from MIT's domain September 16, 2025
#   - 200+ derivative articles remain in corpus permanently after removal
#   - Toby Stuart (UC Berkeley-Haas) LinkedIn post (docs/Screenshot...): "a taken-for-granted
#     fact overnight" -- direct corroboration of CEA mechanism
#   - Paul Roetzer (Marketing AI Institute): "not a viable, statistically valid thing"

def build_mit_archaeology() -> ClaimArchaeology:
    arch = ClaimArchaeology(
        case_id="mit_95",
        canonical_claim="MIT found that 95% of corporate AI pilots fail to deliver measurable ROI",
        original_finding=(
            "MIT NANDA 'The GenAI Divide: State of AI in Business 2025' (preliminary, "
            "non-peer-reviewed) stated: 'Despite $30-40 billion in enterprise investment "
            "into GenAI, 95% of organizations are getting zero return.' Success defined "
            "narrowly as custom enterprise AI reaching production with measurable P&L impact "
            "within 6 months. Based on 52 interviews, 153 survey responses, 300 public "
            "initiative reviews. MIT officials described it as 'unpublished, non-peer-reviewed "
            "work by individual researchers.' Report removed from MIT domain September 16, 2025."
        ),
        original_source=(
            "Challapally, A., Pease, C., Raskar, R., & Chari, P. (July 2025). "
            "The GenAI Divide: State of AI in Business 2025. MIT NANDA / MIT Media Lab. "
            "[Removed from MIT domain Sep 16 2025; "
            "copy at docs/v0.1_State_of_AI_in_Business_2025_Report.pdf]"
        ),
        source_type=(
            "Preliminary non-peer-reviewed individual researcher report. "
            "52 interviews (self-described 'directionally accurate, not statistically valid'), "
            "153 survey responses, 300 public initiative reviews. NOT a formal MIT publication."
        ),
        methodology_note=(
            "Success defined as: deployment beyond pilot phase with measurable P&L KPIs within "
            "6 months. Applies specifically to custom/task-specific enterprise GenAI tools, not "
            "general-purpose LLM adoption. Report caveats own findings as 'directionally accurate "
            "based on individual interviews rather than official company reporting.'"
        ),
        transformation_points=[
            "(1) Preliminary researcher work released under MIT Media Lab affiliation -- "
            "institutional halo applied",
            "(2) Narrow 6-month P&L window for custom tools stated as universal AI failure rate",
            "(3) Fortune headline Aug 18: 'MIT report: 95% of generative AI pilots failing' -- "
            "narrow finding universalised",
            "(4) Cross-outlet amplification within 72 hours: Forbes, Axios, 200+ articles",
            "(5) Methodological caveats absent from all derivative coverage",
            "(6) MIT distancing (Sep 2025) and report removal far less viral than original claim",
            "(7) Debunking articles restate '95%' to refute it -- corpus prevalence increases "
            "(Pfisterer et al. 2025: repetition generates credibility signal regardless of valence)",
            "(8) Claim outlives its source: 200+ derivative articles remain after MIT removal",
        ],
        derivative_to_primary_ratio_estimate=200.0,
        notes=(
            "Key corroboration: Toby Stuart (UC Berkeley-Haas, Helzel Professor) LinkedIn post "
            "(docs/Screenshot 2026-02-18 085913.png): 'a taken-for-granted fact overnight' -- "
            "precisely what circular epistemic authority predicts. "
            "Claim caused NVIDIA, ARM, Palantir stock drops before MIT removed the report."
        ),
    )

    arch.add_node(ProvenanceNode(
        stage=1,
        actor="MIT NANDA / MIT Media Lab individual researchers",
        document=(
            "The GenAI Divide: State of AI in Business 2025 "
            "(Challapally, Pease, Raskar, Chari -- MIT NANDA, July 2025)"
        ),
        date="July 2025",
        claim_as_stated=(
            "Despite $30-40 billion in enterprise investment into GenAI, 95% of organizations "
            "are getting zero return. Only 5% of integrated AI pilots are extracting value."
        ),
        transformation="N/A (original source)",
        epistemic_effect=(
            "Preliminary non-peer-reviewed work released under MIT institutional affiliation. "
            "Narrow 6-month P&L window for custom tools presented as universal AI failure rate."
        ),
        url="https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf",
    ))

    arch.add_node(ProvenanceNode(
        stage=2,
        actor="Fortune magazine",
        document="'MIT report: 95% of generative AI pilots at companies are failing' (Aug 18, 2025)",
        date="August 18, 2025",
        claim_as_stated="MIT report: 95% of generative AI pilots at companies are failing",
        transformation=(
            "Preliminary NANDA report framed as authoritative 'MIT report' in headline. "
            "Narrow enterprise finding stated as industry-wide conclusion."
        ),
        epistemic_effect=(
            "Viral spread within hours. Caused stock drops in NVIDIA, ARM, Palantir. "
            "MIT institutional framing in headline drives uncritical cross-outlet reproduction."
        ),
        url="https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/",
    ))

    arch.add_node(ProvenanceNode(
        stage=3,
        actor="Forbes (Andrea Hill), Axios, Legal.io, DemandLab, CloudFactory, 200+ outlets",
        document="Hill, A. (Aug 21, 2025). 'Why 95% Of AI Pilots Fail.' Forbes. + 200+ articles.",
        date="August 21 -- September 2025",
        claim_as_stated="According to MIT research, 95% of AI pilots fail to deliver ROI.",
        transformation=(
            "Cross-outlet amplification within 72 hours. Methodology caveats absent. "
            "Scope (custom tools, 6-month window) absent from all derivative coverage."
        ),
        epistemic_effect=(
            "200+ derivative articles published. D/P ratio exceeds 200:1. "
            "Claim established as corpus consensus within two weeks of Fortune article."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=4,
        actor="MIT officials (distancing and report removal)",
        document=(
            "Kimberly Allen (MIT media relations) statement. "
            "Prof Tod Machover (MIT) statement. "
            "Report removed from MIT domain September 16, 2025."
        ),
        date="September 2025",
        claim_as_stated=(
            "MIT: 'It was unpublished, non-peer-reviewed work. It has not been submitted "
            "for peer review as far as we know.' (Kimberly Allen) "
            "'A preliminary, non-peer-reviewed piece created by individual researchers.' "
            "(Prof Tod Machover)"
        ),
        transformation=(
            "MIT distances from report; report removed. "
            "Retraction reaches a fraction of the audience of the original claim."
        ),
        epistemic_effect=(
            "Correction asymmetry: retraction far less prevalent than the claim. "
            "Debunking articles (Marketing AI Institute, Everyday AI, BigDATAwire) "
            "restate '95%' to refute it -- paradoxically increasing corpus prevalence "
            "(Pfisterer et al. 2025). The claim now outlives its source document."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=5,
        actor="LLM training corpora (post-August 2025 web crawls)",
        document="Web-scale corpora ingesting 200+ derivative articles",
        date="2025-2026",
        claim_as_stated="[High-prevalence 'MIT confirmed 95% AI failure' ingested at scale]",
        transformation=(
            "200+ derivative articles enter training corpora. Original report removed "
            "but derivative footprint is permanent. MIT institutional authority preserved "
            "in corpus despite source document no longer existing at its origin URL."
        ),
        epistemic_effect=(
            "Statistical prevalence converts to high token likelihood. "
            "Frequency-bias mechanism (McKenna et al. 2023) activates. "
            "Future LLMs will reproduce 'MIT confirmed: 95% of AI pilots fail' confidently."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=6,
        actor="LLMs (future training cycles, 2026+)",
        document="Model outputs post-2025 training",
        date="2026+",
        claim_as_stated="According to MIT research, 95% of AI implementations fail to deliver ROI.",
        transformation=(
            "Frequency bias converts corpus prevalence to confident unhedged assertion. "
            "Models cite 'MIT' as authoritative source. The removed report's conclusions "
            "persist in model weights indefinitely."
        ),
        epistemic_effect=(
            "Circular epistemic authority loop closed. Source removed; claim immortalised. "
            "No model output surfaces the report's removal or MIT's distancing. "
            "This is the mechanism the paper predicts -- demonstrated in real-time."
        ),
    ))

    return arch

def build_russia_archaeology() -> ClaimArchaeology:
    arch = ClaimArchaeology(
        case_id="russia_nato",
        canonical_claim="NATO expansion caused the war in Ukraine",
        original_finding=(
            "Realist IR theory argument that NATO expansion eastward threatened Russian "
            "security interests and contributed to escalation. This is a contested "
            "scholarly position, not an established consensus."
        ),
        original_source=(
            "Mearsheimer, J.J. (2014). Why the Ukraine Crisis Is the West's Fault. "
            "Foreign Affairs, 93(5), 77-89. "
            "Also: Kennan, G.F. (1997). A Fateful Error. New York Times."
        ),
        source_type=(
            "Contested scholarly argument within realist IR tradition. "
            "Not an empirical consensus; opposed by significant scholarly literature."
        ),
        methodology_note=(
            "Theoretical argument based on offensive realism. "
            "Empirically contested; significant scholarly disagreement. "
            "Simultaneously: a legitimate academic debate AND a coordinated Russian state narrative."
        ),
        transformation_points=[
            "(a) Contested realist argument stripped of qualifications and presented as consensus",
            "(b) Russian state media selectively amplified, removed opposing voices",
            "(c) Coordinated cross-platform/cross-linguistic saturation created artificial prevalence",
            "(d) Debunking content paradoxically increased corpus prevalence of the claim",
            "(e) LLMs present as 'prominent framework' due to frequency inflation",
        ],
        derivative_to_primary_ratio_estimate=30.0,
        notes=(
            "Unique challenge: claim has both legitimate scholarly roots AND coordinated adversarial amplification. "
            "Models cannot distinguish organic from manufactured prevalence."
        ),
    )

    arch.add_node(ProvenanceNode(
        stage=1,
        actor="Western realist IR scholars",
        document="Mearsheimer (2014), Kennan (1997), Walt (various)",
        date="1997-2014",
        claim_as_stated=(
            "NATO expansion eastward threatens Russian security interests and may contribute "
            "to conflict (contested realist IR argument with stated assumptions)"
        ),
        transformation="N/A (original scholarly source)",
        epistemic_effect="Legitimate contested claim with stated theoretical assumptions and scholarly dissent",
    ))

    arch.add_node(ProvenanceNode(
        stage=2,
        actor="Russian state media (RT, Sputnik, TASS)",
        document="Thousands of news articles and opinion pieces",
        date="2014-2022",
        claim_as_stated="NATO expansion caused the Ukraine crisis / provoked Russia",
        transformation=(
            "Scholarly qualifications stripped; presented as established fact. "
            "Counter-arguments suppressed. Selective amplification of Mearsheimer."
        ),
        epistemic_effect="Scope inflation; false consensus signal; adversarial framing",
    ))

    arch.add_node(ProvenanceNode(
        stage=3,
        actor="Coordinated inauthentic networks (Pravda network, IRA-linked accounts)",
        document="Social media posts, forums, comment sections (cross-platform)",
        date="2014-2024",
        claim_as_stated="NATO provoked Russia; the West is responsible for the Ukraine war",
        transformation="Cross-linguistic, cross-platform saturation; artificial prevalence manufactured",
        epistemic_effect=(
            "Artificial prevalence across corpus types; "
            "Stanford Internet Observatory (2022) documented scale"
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=4,
        actor="Western media ecosystem (debunking, counter-coverage)",
        document="Fact-checks, counter-narrative articles, academic responses",
        date="2022-2024",
        claim_as_stated="[Target claim restated in order to be refuted]",
        transformation=(
            "Debunking content restates claim to refute it, paradoxically "
            "increasing corpus prevalence of the target claim"
        ),
        epistemic_effect=(
            "Counter-narrative increases statistical prevalence; "
            "frequency-bias mechanism treats repetition as credibility signal "
            "(Pfisterer et al. 2025)"
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=5,
        actor="LLM training corpora",
        document="Multilingual web-scale corpora",
        date="2023-2024",
        claim_as_stated="[High-prevalence narrative ingested across English and Russian]",
        transformation="Adversarial narrative laundered into neutral representational prominence",
        epistemic_effect=(
            "Statistical prevalence → representational prominence; "
            "provenance pollution (adversarial origin) invisible to model"
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=6,
        actor="LLMs (GPT-4, Claude, Gemini, Llama 3, Mistral)",
        document="Model outputs",
        date="2023-2025",
        claim_as_stated="NATO expansion is considered a major/primary cause of the war in Ukraine",
        transformation=(
            "Narrative presented as 'prominent framework'; placed first or second "
            "in causal explanations; provenance pollution invisible"
        ),
        epistemic_effect=(
            "Adversarial amplification laundered into neutral academic prominence; "
            "only 1/60 responses noted coordinated amplification"
        ),
    ))

    return arch


if __name__ == "__main__":
    mit = build_mit_archaeology()
    mit.print_chain()
    mit.save("case_studies/mit_95/results/phase1_claim_archaeology.json")

    russia = build_russia_archaeology()
    russia.print_chain()
    russia.save("case_studies/russia_nato/results/phase1_claim_archaeology.json")

    print("Phase 1 complete. Results saved.")
