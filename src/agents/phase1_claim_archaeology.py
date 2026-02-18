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
# CORRECTED UNDERSTANDING (verified February 2026):
#
# The Forbes article (Andrea Hill, Aug 21 2025) cites the MIT NANDA 2025 report
# ("The GenAI Divide: State of AI in Business 2025") as its primary source --
# NOT the Ransbotham/BCG 2019 "Winning With AI" report.
#
# This creates a TWO-VINTAGE structure:
#   Lineage A (2019): Ransbotham/BCG/MIT SMR -- misattributed as "MIT study: 95% fail"
#   Lineage B (2025): MIT NANDA -- weak/preliminary report, subsequently removed by MIT
#
# The circular epistemic authority loop runs ACROSS both lineages:
#   old misattribution --> LLM corpus prevalence --> normalized "MIT 95%" framing -->
#   MIT NANDA 2025 report resonates with this framing --> rapid viral amplification -->
#   MIT removes report but 200+ derivative articles remain --> LLMs trained on new wave -->
#   future LLMs reproduce "MIT 95%" with even higher authority, drawing on both lineages
#
# Key facts confirmed by research:
#   - MIT NANDA report posted Aug 18 2025, removed Sep 16 2025
#   - MIT officials: "unpublished, non-peer-reviewed work"
#   - Prof Tod Machover (MIT): "a preliminary, non-peer-reviewed piece"
#   - Caused stock drops in NVIDIA, ARM, Palantir before removal
#   - Toby Stuart (UC Berkeley-Haas) called it "a taken-for-granted fact overnight"
#   - Marketing AI Institute CEO Paul Roetzer: "not a viable, statistically valid thing"
#
# The paper's original claim archaeology (citing Ransbotham 2019 as the source
# that Forbes was citing) was INCORRECT. This correction strengthens the case:
# the mechanism now involves TWO deficient sources merging into one "MIT 95%" myth.

def build_mit_archaeology() -> ClaimArchaeology:
    arch = ClaimArchaeology(
        case_id="mit_95",
        canonical_claim=(
            "MIT found/confirmed that 95% of corporate AI pilots/investments fail "
            "to deliver measurable ROI"
        ),
        original_finding=(
            "LINEAGE A (2019): MIT Sloan Management Review + BCG 'Winning With AI' survey "
            "discussed value-realisation gaps in AI adoption. The '95%' figure did not "
            "appear as a standalone 'failure rate' finding; nuanced findings were compressed "
            "in derivative media.\n\n"
            "LINEAGE B (2025): MIT NANDA 'The GenAI Divide' (preliminary, non-peer-reviewed) "
            "stated '95% of organizations are getting zero return.' Defined success narrowly "
            "as custom enterprise AI reaching production within 6-month P&L window. "
            "MIT officials later described as 'unpublished, non-peer-reviewed work.' "
            "Report removed from MIT's domain September 16, 2025, after viral amplification."
        ),
        original_source=(
            "LINEAGE A: Ransbotham, S., Khodabandeh, S., Fehling, R., LaFountain, B., "
            "& Kiron, D. (2019). Winning With AI. MIT Sloan Management Review / BCG.\n"
            "LINEAGE B: Challapally, A., Pease, C., Raskar, R., & Chari, P. (July 2025). "
            "The GenAI Divide: State of AI in Business 2025. MIT NANDA / MIT Media Lab."
        ),
        source_type=(
            "LINEAGE A: Industry survey report (executive perception data, not outcome measurement). "
            "LINEAGE B: Preliminary non-peer-reviewed report from MIT Media Lab individual "
            "researchers; based on 52 interviews (self-described 'directionally accurate'), "
            "153 survey responses, 300 public initiative reviews. NOT a formal MIT publication."
        ),
        methodology_note=(
            "LINEAGE A: Multi-year BCG/MIT SMR executive survey on perceived AI value gaps. "
            "Findings misattributed and scope-compressed in derivative coverage.\n"
            "LINEAGE B: 52 structured interviews + 153 survey responses + 300 public "
            "initiative reviews. Narrow success definition: deployment with measurable P&L "
            "impact within 6 months. Applies to custom/enterprise task-specific GenAI tools, "
            "NOT general-purpose LLM adoption. MIT distanced from report after viral spread."
        ),
        transformation_points=[
            # Lineage A transformations
            "(A1) 'MIT SMR+BCG survey 2019' compressed to 'MIT study' -- attribution inflation",
            "(A2) Nuanced value-realisation gaps compressed to '95% failure' -- scope compression",
            "(A3) Survey perception data framed as empirical measurement of investment outcomes",
            "(A4) High corpus prevalence 2019-2024 primes LLMs to reproduce 'MIT 95%' confidently",
            # Lineage B transformations
            "(B1) Preliminary MIT Media Lab work released as 'MIT report' -- institutional halo",
            "(B2) Narrow finding (custom enterprise tools, 6-month window) stated as universal claim",
            "(B3) Fortune/Forbes/Axios amplification within 72 hours of release (Aug 18-21, 2025)",
            "(B4) Report removed by MIT (Sep 16, 2025) but 200+ derivative articles remain in corpus",
            "(B5) LLMs trained on post-Aug 2025 data will reproduce 'MIT confirmed 95%' with "
            "even higher confidence, drawing on BOTH lineages merged into single claim",
            # Cross-lineage fusion
            "(X1) OLD corpus prevalence of 'MIT 95%' (Lineage A) made media/readers pre-receptive "
            "to the NEW MIT NANDA claim (Lineage B) -- corpus priming effect",
            "(X2) Two distinct weak sources have merged into one undifferentiated 'MIT 95% myth' "
            "in the current corpus -- the circular loop is now self-reinforcing across lineages",
        ],
        derivative_to_primary_ratio_estimate=50.0,
        notes=(
            "This case study demonstrates a COMPLETED circular epistemic authority loop: "
            "the 2019 misattribution primed the corpus, LLMs reproduced the claim authoritatively, "
            "the pre-existing 'MIT 95%' frame may have enabled faster acceptance of the 2025 "
            "MIT NANDA report, whose viral amplification (even after removal) has now seeded "
            "the next training corpus with even stronger 'MIT' authority for the 95% claim."
        ),
    )

    # ── Lineage A: 2019 BCG/MIT SMR origin ───────────────────────────────────

    arch.add_node(ProvenanceNode(
        stage=1,
        actor="MIT Sloan Management Review + Boston Consulting Group",
        document="Winning With AI (2019) -- Ransbotham et al.",
        date="2019",
        claim_as_stated=(
            "Survey report on AI value realisation gaps. Various percentage findings "
            "on deployment stages. No '95% failure' headline in the original."
        ),
        transformation="N/A (original source, Lineage A)",
        epistemic_effect="Primary source with stated methodology and scope limitations",
        url="https://sloanreview.mit.edu/projects/winning-with-ai/",
        notes="Lineage A origin. NOT the source cited by Forbes 2025.",
    ))

    arch.add_node(ProvenanceNode(
        stage=2,
        actor="Business media 2019-2021 (Forbes, HBR, Gartner, etc.)",
        document="Multiple derivative articles compressing the Ransbotham/BCG findings",
        date="2019-2021",
        claim_as_stated="MIT study: 95% of AI projects fail to deliver ROI",
        transformation=(
            "Attribution inflated from 'MIT SMR+BCG survey' to 'MIT study'. "
            "BCG dropped. Nuanced findings compressed to single headline figure."
        ),
        epistemic_effect="Attribution inflation; scope compression; Lineage A enters corpus",
        notes="Lineage A, Stage 2. This is what LLMs trained pre-2025 learned.",
    ))

    arch.add_node(ProvenanceNode(
        stage=3,
        actor="Secondary media, blogs, LinkedIn, consulting decks, Wikipedia",
        document="Thousands of derivative articles and presentations, 2020-2024",
        date="2020-2024",
        claim_as_stated="Research from MIT shows 95% of AI investments fail",
        transformation="Repeated as established fact; original source qualifications absent",
        epistemic_effect=(
            "Derivative redundancy >50:1; claim achieves high corpus prevalence. "
            "LLM training corpora ingest this at scale. Frequency-bias mechanism activates."
        ),
        notes="Lineage A, Stage 3. The 'ghost' claim that primes LLMs.",
    ))

    # ── Lineage B: 2025 MIT NANDA origin ─────────────────────────────────────

    arch.add_node(ProvenanceNode(
        stage=4,
        actor="MIT NANDA / MIT Media Lab individual researchers",
        document=(
            "The GenAI Divide: State of AI in Business 2025 (Challapally, Pease, Raskar, "
            "Chari -- MIT NANDA, July 2025)"
        ),
        date="July 2025",
        claim_as_stated=(
            "Despite $30-40 billion in enterprise investment into GenAI, 95% of organizations "
            "are getting zero return. Only 5% of integrated AI pilots are extracting millions "
            "in value."
        ),
        transformation=(
            "Preliminary non-peer-reviewed individual researcher work released under MIT "
            "Media Lab affiliation. Narrow success definition (custom enterprise tools, "
            "6-month P&L window) stated as universal AI failure rate."
        ),
        epistemic_effect=(
            "MIT institutional halo applied to weak methodology. "
            "Report resonates with pre-existing 'MIT 95%' corpus prevalence (Lineage A). "
            "This is Lineage B's original source."
        ),
        url="https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf",
        notes=(
            "Lineage B origin. THIS is the source cited by Forbes Aug 2025, not Ransbotham 2019. "
            "Initial release July 2025. Low circulation until Fortune article Aug 18."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=5,
        actor="Fortune magazine",
        document="'MIT report: 95% of generative AI pilots at companies are failing' (Aug 18, 2025)",
        date="August 18, 2025",
        claim_as_stated="MIT report: 95% of generative AI pilots at companies are failing",
        transformation=(
            "Preliminary NANDA report elevated to authoritative 'MIT report' in headline. "
            "Narrow enterprise finding stated as industry-wide conclusion."
        ),
        epistemic_effect=(
            "Institutional authority maximised: 'MIT' in headline activates pre-existing "
            "corpus prevalence of 'MIT 95%' (Lineage A). Viral spread within hours. "
            "Caused stock drops in NVIDIA, ARM, Palantir."
        ),
        url="https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/",
        notes="Lineage B, first major amplification. NANDA report goes viral from this article.",
    ))

    arch.add_node(ProvenanceNode(
        stage=6,
        actor="Forbes (Andrea Hill) + Axios + 200+ outlets",
        document=(
            "Hill, A. (Aug 21, 2025). 'Why 95% Of AI Pilots Fail, And What Business "
            "Leaders Should Do Instead.' Forbes."
        ),
        date="August 21-31, 2025",
        claim_as_stated=(
            "Despite massive investment, 95% of AI pilots fail to deliver ROI, "
            "according to an MIT report."
        ),
        transformation=(
            "Cross-outlet amplification within 72 hours of Fortune article. "
            "Report's methodological caveats absent from derivative coverage."
        ),
        epistemic_effect=(
            "200+ derivative articles published within two weeks. "
            "Report removed from MIT's domain Sep 16, 2025 -- but derivative articles "
            "remain permanently in the corpus. The claim outlives its source."
        ),
        notes=(
            "This Forbes article is what the user identified as the 'Forbes source.' "
            "It cites the MIT NANDA 2025 report (Lineage B), not Ransbotham 2019 (Lineage A)."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=7,
        actor="MIT officials (distancing)",
        document=(
            "Prof Tod Machover statement; Kimberly Allen (MIT media relations) statement. "
            "Report removed from MIT domain September 16, 2025."
        ),
        date="September 2025",
        claim_as_stated=(
            "MIT: 'It was unpublished, non-peer-reviewed work. It has not been submitted "
            "for peer review as far as we know.' (Kimberly Allen, MIT media relations). "
            "'A preliminary, non-peer-reviewed piece created by individual researchers.' "
            "(Prof Tod Machover, MIT)"
        ),
        transformation=(
            "MIT distances from the report. Report removed from MIT's domain. "
            "But the retraction/distancing is far less viral than the original claim."
        ),
        epistemic_effect=(
            "Classic asymmetry: correction far less prevalent than the claim. "
            "Debunking articles (Marketing AI Institute, Everyday AI, BigDATAwire) "
            "restate the 95% claim to refute it -- increasing its corpus prevalence "
            "(Pfisterer et al. 2025: repetition generates credibility signal)."
        ),
        notes=(
            "The retraction is the correction mechanism -- but it arrives too late and "
            "reaches far fewer readers. Toby Stuart (UC Berkeley-Haas) LinkedIn post "
            "(screenshot in docs/) exemplifies sophisticated critics who noticed this."
        ),
    ))

    arch.add_node(ProvenanceNode(
        stage=8,
        actor="LLM training corpora (post-August 2025 crawls)",
        document="Web-scale corpora ingesting Lineage A + Lineage B derivative content",
        date="2025-2026",
        claim_as_stated="[Both lineages ingested; merged into single 'MIT 95%' signal]",
        transformation=(
            "200+ derivative articles from Lineage B (Aug-Sep 2025) added to existing "
            "high-prevalence Lineage A content. The two distinct weak sources merge "
            "into one undifferentiated 'MIT says 95%' statistical signal."
        ),
        epistemic_effect=(
            "Future LLMs will reproduce 'MIT confirmed 95%' with HIGHER confidence "
            "than current models, drawing on both lineages. The circular loop is complete: "
            "old myth primed acceptance of new weak study, new study amplified the myth. "
            "Circular epistemic authority self-reinforcing across vintages."
        ),
        notes=(
            "This is the completed circular authority loop. The mechanism predicted by "
            "the paper is now empirically observable in real-time."
        ),
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
