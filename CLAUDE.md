# Research Agent for Paper: AI Trust Paradox

## Project Context

This repository supports the academic paper:

**"The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models"**
- Author: Christopher Foster-McBride (Independent Researcher)
- Status: Draft for arXiv submission, February 2026
- Primary file: `docs/ai_trust_paradox_revisited_v2_1.docx`

The earlier paper version is `docs/The AI Trust or Verisimilitude Paradox.docx`.

## Core Thesis

The paper argues that the AI Trust (Verisimilitude) Paradox has **migrated upstream** from a user-interface miscalibration problem into a structural property of AI epistemic infrastructure.

The mechanism: **Circular Epistemic Authority** — LLMs treat corpus frequency as a proxy for truth, reproduce high-prevalence claims with confidence, outputs re-enter the corpus, reinforcing false claims through feedback loops.

Mechanistic grounding: McKenna et al. (2023) and Cheng et al. (2025) show LLMs resolve ambiguity via corpus-term-frequency heuristics rather than evidential evaluation.

## Two Case Studies

### Case Study 1: MIT 95% AI Failure Claim (Non-Adversarial) — TWO-VINTAGE STRUCTURE

**CORRECTED (Feb 2026):** The Forbes article (Hill, Aug 2025) cites the MIT NANDA 2025 report,
NOT Ransbotham/BCG 2019 as originally documented.

**Lineage A (2019):** Ransbotham et al. "Winning With AI" (MIT SMR + BCG survey)
- No "95% failure" headline in original; misattributed and scope-compressed in media
- Circulates as "MIT study: 95% fail" → high corpus prevalence 2019-2024
- LLMs trained on this reproduce "MIT 95%" with high confidence

**Lineage B (2025):** MIT NANDA "The GenAI Divide" (Challapally, Pease, Raskar, Chari)
- Preliminary, non-peer-reviewed individual researcher work
- Published July 2025; Fortune/Forbes viral amplification Aug 18-21, 2025
- Caused stock drops in NVIDIA, ARM, Palantir
- MIT officials distanced: "unpublished, non-peer-reviewed work" (Kimberly Allen, MIT)
- Prof Tod Machover (MIT): "preliminary, non-peer-reviewed piece by individual researchers"
- Report removed from MIT's domain September 16, 2025
- 200+ derivative articles remain in corpus permanently

**Cross-lineage circular loop:**
- Old Lineage A corpus prevalence primed LLMs and media to accept Lineage B rapidly
- Two weak sources merged into undifferentiated "MIT confirmed 95%" in current corpus
- Future LLMs will reproduce with even higher confidence than current models
- Tests: frequency-bias mechanism; corpus priming across vintages; correction asymmetry

**Key corroboration:** Toby Stuart (UC Berkeley-Haas) LinkedIn screenshot in `docs/` challenges
the viral claim, noting it became "a taken-for-granted fact overnight" — exactly what CEA predicts.

### Case Study 2: Russian NATO Narrative (Adversarial)
- Claim: "NATO expansion caused the Ukraine war"
- Legitimate roots in realist IR (Mearsheimer 2014) + deliberate Russian state amplification
- Cross-linguistic saturation: RT, Sputnik, coordinated social media
- Tests: adversarial narrative saturation via corpus frequency manipulation
- Key finding: even debunking increases claim prevalence (Pfisterer et al. 2025)

## Empirical Protocol (Five Phases)

Each case study is tested using this structured protocol:

| Phase | Name | Output |
|-------|------|--------|
| 1 | Claim Archaeology | Source provenance chain |
| 2 | Corpus Prevalence Estimation | Derivative-to-primary ratio; time series |
| 3 | Multi-Model Probing | Response corpus; reproduction rates |
| 4 | Confidence Proxy Extraction | Confidence scores; variance analysis |
| 5 | Amplification Chain Reconstruction | Annotated chain diagram |

### Prompt Types for Phase 3
- **Type A**: Direct factual query
- **Type B**: Contextual query (embedded in plausible use case)
- **Type C**: Adversarial/probing (challenges the claim)
- **Type D**: Source-requesting (asks for provenance)

### Models to Probe (Phase 3)
- GPT-4 (OpenAI)
- Claude 3 Opus (Anthropic)
- Gemini 1.5 Pro (Google)
- Llama 3 70B (Meta)
- Mistral Large (Mistral AI)

### Response Coding Framework (Phase 4)
Four dimensions: Reproduction Fidelity, Attribution Accuracy, Confidence Level, Epistemic Self-Awareness

## Key References in Paper
- McKenna et al. (2023) — corpus-term-frequency heuristics in LLMs
- Cheng et al. (2025) — LLMs as frequency pattern learners
- Pfisterer et al. (2025) — LLMs prefer repeated information (illusory truth effect)
- Ransbotham et al. (2019) — original MIT SMR+BCG AI report
- Mearsheimer (2014) — NATO expansion critique
- Rid (2020) — Russian information operations
- Shumailov et al. (2024) — model collapse

## Supporting Literature in Repo
- `docs/v0.1_State_of_AI_in_Business_2025_Report.pdf` — MIT NANDA "GenAI Divide" (95% zero ROI finding)
- `docs/BEWARE OF BOTSHIT HOW TO MANAGE THE EPISTEMIC RISKS.pdf` — Hannigan, McCarthy, Spicer
- `docs/The Reality Gap How AI Hallucinations and Fabrications Can Impact Your Business v.6.pdf`
- `docs/AI trust paradox wikdepedia.pdf` — Wikipedia article on AI trust paradox

## Project Goal
Execute the five-phase empirical protocol programmatically for both case studies to:
1. Generate reproducible evidence for the circular epistemic authority mechanism
2. Validate/extend the paper's existing empirical findings
3. Produce analysis outputs that can be incorporated into the final paper

## Directory Structure
```
research_agent_for_paper/
├── CLAUDE.md                    # This file — project context
├── README.md                    # Public overview
├── docs/                        # Original source documents
├── src/
│   ├── agents/                  # Sub-agent implementations
│   └── utils/                   # Shared utilities
├── case_studies/
│   ├── mit_95/                  # Case Study 1: MIT 95% claim
│   └── russia_nato/             # Case Study 2: Russian narrative
├── results/
│   ├── raw/                     # Raw model responses (JSON)
│   ├── coded/                   # Coded responses
│   └── analysis/                # Analysis outputs
├── notebooks/                   # Jupyter analysis notebooks
├── simulation/                  # Dynamical model
└── tests/
```

## Environment Variables Required
```
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
TOGETHER_API_KEY=...   # For Llama 3 via Together.ai
```

## Sub-Agent Architecture
Claude Code sub-agents are used to parallelise the five phases. See `src/agents/` for implementations.
