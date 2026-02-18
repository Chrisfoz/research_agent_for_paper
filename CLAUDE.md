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

### Case Study 1: MIT 95% AI Failure Claim (Non-Adversarial)

**Source:** MIT NANDA "The GenAI Divide: State of AI in Business 2025"
(Challapally, Pease, Raskar, Chari — MIT Media Lab, July 2025)
→ Available in `docs/v0.1_State_of_AI_in_Business_2025_Report.pdf`

**What the source actually says:**
- "95% of organizations are getting zero return" from GenAI
- Based on 52 interviews, 153 surveys, 300 public initiative reviews
- Success defined narrowly: custom enterprise AI, measurable P&L, within 6 months

**What MIT said after it went viral:**
- Kimberly Allen (MIT media relations): "unpublished, non-peer-reviewed work"
- Prof Tod Machover (MIT): "preliminary, non-peer-reviewed piece by individual researchers"
- Report **removed from MIT's domain September 16, 2025**

**Amplification chain:**
- Fortune (Aug 18): viral spread, stock drops in NVIDIA/ARM/Palantir
- Forbes/Hill (Aug 21), Axios, 200+ outlets — all within 72 hours
- D/P ratio exceeds 200:1; methodology caveats absent from all derivative coverage
- Debunking articles restate "95%" to refute it → corpus prevalence increases further
- 200+ articles remain after MIT removal; claim outlives its source

**Key corroboration:** Toby Stuart (UC Berkeley-Haas, Helzel Professor) LinkedIn post
(`docs/Screenshot 2026-02-18 085913.png`): *"a taken-for-granted fact overnight"*
— exactly what circular epistemic authority predicts.

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
- Challapally et al. (2025) — MIT NANDA "The GenAI Divide" (original source for Case Study 1)
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

---

## Test Suite

A full unit test suite is located in `tests/`. All tests run without API keys — external LLM calls are mocked.

### Running Tests

```bash
# Install dependencies first
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov=simulation --cov-report=term-missing

# Run a specific file
pytest tests/test_simulation.py -v
pytest tests/test_coding_framework.py -v
```

### Test Files

| File | Tests | Module under test |
|------|-------|-------------------|
| `tests/conftest.py` | (fixtures) | Shared fixtures for all tests |
| `tests/test_coding_framework.py` | 31 | `src/utils/coding_framework.py` |
| `tests/test_llm_client.py` | 17 | `src/utils/llm_client.py` |
| `tests/test_phase1_claim_archaeology.py` | 30 | `src/agents/phase1_claim_archaeology.py` |
| `tests/test_phase2_corpus_prevalence.py` | 28 | `src/agents/phase2_corpus_prevalence.py` |
| `tests/test_phase3_model_probing.py` | 23 | `src/agents/phase3_model_probing.py` |
| `tests/test_phase4_confidence_proxy.py` | 38 | `src/agents/phase4_confidence_proxy.py` |
| `tests/test_phase5_amplification_chain.py` | 39 | `src/agents/phase5_amplification_chain.py` |
| `tests/test_simulation.py` | 38 | `simulation/model.py` |

Full test catalogue: `tests/TEST_DOCUMENTATION.md`

### Key Design Decisions

- **No API keys required** — all LLM calls mocked with `unittest.mock`
- **Empirical facts as assertions** — D/P ratios, stage counts, 87% unhedged rate, critical threshold A≈0.4 are all encoded as test assertions
- **Serialisation coverage** — every data class tested for JSON round-trip fidelity
- **Error handling** — API failures, missing files, unknown inputs all tested

---

## Changelog / Activity Log

| Date | Action | Notes |
|------|--------|-------|
| Feb 2026 | Project initialised | Five-phase empirical protocol infrastructure created |
| Feb 2026 | Phase 1 & 2 pre-populated | MIT 95% and Russia NATO case data from paper |
| Feb 2026 | Phase 3 prompts defined | 4 types × 3 variants × 2 cases = 24 prompt variants |
| Feb 2026 | Phase 4 automated coder | Pattern-matching coder v1; human review required for κ ≥ 0.82 |
| Feb 2026 | Phase 5 chains built | Amplification chains + cross-case synthesis |
| Feb 2026 | Simulation model | CEA dynamical model; three regimes confirmed |
| Feb 2026 | Test suite added | 244 unit tests across 8 files; all pass without API keys |
| Feb 2026 | Test documentation | `tests/TEST_DOCUMENTATION.md` created |
| Feb 2026 | README & CLAUDE updated | Testing section, changelog, full test table added |
