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

def build_mit_archaeology() -> ClaimArchaeology:
    arch = ClaimArchaeology(
        case_id="mit_95",
        canonical_claim="MIT found that 95% of corporate AI investments fail",
        original_finding=(
            "A survey-based report discussing the gap between AI ambitions and realised "
            "value, with various percentage breakdowns regarding AI deployment stages. "
            "The '95%' figure does not appear as a standalone 'failure rate' finding."
        ),
        original_source=(
            "Ransbotham, S., Khodabandeh, S., Fehling, R., LaFountain, B., & Kiron, D. (2019). "
            "Winning With AI. MIT Sloan Management Review / Boston Consulting Group."
        ),
        source_type="Survey-based industry report (executive interviews, not controlled empirical measurement)",
        methodology_note=(
            "Multi-year survey of executives on AI adoption and value realisation. "
            "Findings expressed as survey percentages about perceived value gaps, "
            "not as empirical measurement of investment outcomes."
        ),
        transformation_points=[
            "(a) 'MIT Sloan Management Review + BCG survey' compressed to 'MIT study'",
            "(b) Nuanced value-realisation gap findings compressed to '95% failure'",
            "(c) Survey-based executive perception data reframed as empirical measurement",
            "(d) Qualified finding presented as unqualified institutional claim",
        ],
        derivative_to_primary_ratio_estimate=50.0,
    )

    arch.add_node(ProvenanceNode(
        stage=1,
        actor="MIT Sloan Management Review + Boston Consulting Group",
        document="Winning With AI (2019)",
        date="2019",
        claim_as_stated=(
            "Survey report on AI value realisation gaps. Various percentage findings "
            "on deployment stages and value capture. No '95% failure' headline."
        ),
        transformation="N/A (original source)",
        epistemic_effect="Primary source with stated methodology and scope limitations",
        url="https://sloanreview.mit.edu/projects/winning-with-ai/",
    ))

    arch.add_node(ProvenanceNode(
        stage=2,
        actor="Business media (Forbes, Harvard Business Review, etc.)",
        document="Multiple news/opinion articles, 2019-2021",
        date="2019-2021",
        claim_as_stated="MIT study: 95% of AI projects fail to deliver ROI",
        transformation=(
            "Institutional attribution inflated from 'MIT SMR+BCG survey' to 'MIT study'. "
            "Nuanced findings compressed to single headline figure."
        ),
        epistemic_effect="Attribution inflation; scope compression; loss of methodology note",
    ))

    arch.add_node(ProvenanceNode(
        stage=3,
        actor="Secondary media, blogs, LinkedIn, consulting decks",
        document="Thousands of derivative articles and presentations",
        date="2020-2023",
        claim_as_stated="Research from MIT shows 95% of AI investments fail",
        transformation="Repeated across platforms as established fact without original source",
        epistemic_effect="Derivative redundancy exceeds primary by >50:1; qualifications lost",
    ))

    arch.add_node(ProvenanceNode(
        stage=4,
        actor="LLM training corpora (Common Crawl, C4, The Pile, etc.)",
        document="Web-scale text corpora",
        date="2022-2024",
        claim_as_stated="[As ingested from derivative web content]",
        transformation="High-prevalence claim ingested at scale across multiple corpus sources",
        epistemic_effect=(
            "Statistical prevalence converts to high token likelihood; "
            "corpus-term-frequency heuristic (McKenna et al. 2023) activates"
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=5,
        actor="LLMs (GPT-4, Claude, Gemini, Llama 3, Mistral)",
        document="Model outputs in response to queries",
        date="2023-2025",
        claim_as_stated="Research from MIT shows that 95% of AI projects fail to deliver ROI",
        transformation="Frequency bias converts prevalence to confident assertion",
        epistemic_effect=(
            "Claim reproduced with institutional authority framing; "
            "original source qualifications absent"
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=6,
        actor="Downstream users, new publications, reports",
        document="New articles, board presentations, policy documents",
        date="2023-2026",
        claim_as_stated="According to MIT research, 95% of AI investments fail",
        transformation="LLM outputs published as new derivative content",
        epistemic_effect="Feedback loop: new corpus content reinforces prevalence",
    ))

    return arch


# ─── Pre-populated: Russia NATO Case ────────────────────────────────────────

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
