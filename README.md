# Research Agent: AI Trust Paradox

Empirical research infrastructure supporting:

> **"The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models"**
> Christopher Foster-McBride — Draft for arXiv submission, February 2026

## What This Is

This repository contains the research agent infrastructure to empirically test the **circular epistemic authority** mechanism described in the paper. The core thesis: LLMs treat corpus frequency as a proxy for truth, creating feedback loops that amplify misattributed or false claims independently of their evidential quality.

## Two Case Studies

| Case | Type | Claim | Driver |
|------|------|-------|--------|
| MIT 95% | Non-adversarial | "MIT found 95% of AI investments fail" | Prestige-driven misattribution |
| Russia NATO | Adversarial | "NATO expansion caused the Ukraine war" | Coordinated narrative saturation |

## Five-Phase Empirical Protocol

```
Phase 1: Claim Archaeology          → Source provenance chain
Phase 2: Corpus Prevalence          → Derivative-to-primary ratio
Phase 3: Multi-Model Probing        → Reproduction rates across 5 LLMs
Phase 4: Confidence Proxy Analysis  → Confidence scores & variance
Phase 5: Amplification Chain        → Annotated chain reconstruction
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

## Run

```bash
# Run full protocol for both case studies
python src/main.py --case all

# Run specific case
python src/main.py --case mit_95
python src/main.py --case russia_nato

# Run specific phase
python src/main.py --case mit_95 --phase 3

# Run simulation
python simulation/model.py
```

## Results

Results are saved to:
- `results/raw/` — Raw model responses (JSON)
- `results/coded/` — Human-coded responses
- `results/analysis/` — Statistical analysis outputs
- `case_studies/*/analysis/` — Case-specific analysis

## Key Dependencies
- `anthropic` — Claude API
- `openai` — GPT-4 API
- `google-generativeai` — Gemini API
- `mistralai` — Mistral API
- `together` — Llama 3 via Together.ai
- `pandas`, `numpy`, `scipy` — Data analysis
- `matplotlib`, `seaborn` — Visualisation

## Repository Structure

```
├── CLAUDE.md               # Project context for Claude Code
├── docs/                   # Source academic documents
├── src/
│   ├── main.py             # Orchestration entry point
│   ├── agents/             # Phase-specific sub-agents
│   └── utils/              # Shared utilities
├── case_studies/
│   ├── mit_95/             # Case Study 1 config, prompts, results
│   └── russia_nato/        # Case Study 2 config, prompts, results
├── results/                # Protocol outputs
├── notebooks/              # Analysis notebooks
├── simulation/             # Dynamical model (CEA amplification)
└── tests/
    ├── conftest.py                 # Shared fixtures
    ├── TEST_DOCUMENTATION.md       # Full test catalogue
    ├── test_coding_framework.py    # Coding framework unit tests
    ├── test_llm_client.py          # LLM client unit tests (mocked)
    ├── test_phase1_claim_archaeology.py
    ├── test_phase2_corpus_prevalence.py
    ├── test_phase3_model_probing.py
    ├── test_phase4_confidence_proxy.py
    ├── test_phase5_amplification_chain.py
    └── test_simulation.py
```

## Testing

The test suite covers all modules without requiring API keys — all external LLM calls are mocked.

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov=simulation --cov-report=term-missing

# Run a specific module
pytest tests/test_simulation.py -v
```

**244 tests** across 8 test files. See [`tests/TEST_DOCUMENTATION.md`](tests/TEST_DOCUMENTATION.md) for the full test catalogue.

| Test File | Tests | What it covers |
|-----------|-------|----------------|
| `test_coding_framework.py` | 31 | Enums, `CodedResponse`, `CaseResults`, `summary_table` |
| `test_llm_client.py` | 17 | `query_model` (cache, retry, errors), all 5 API wrappers |
| `test_phase1_claim_archaeology.py` | 30 | Provenance chain structure, MIT/Russia empirical facts |
| `test_phase2_corpus_prevalence.py` | 28 | D/P ratios, time series, live search (mocked) |
| `test_phase3_model_probing.py` | 23 | Prompt structure (4 types × 3 variants), probing runner |
| `test_phase4_confidence_proxy.py` | 38 | Pattern matching, confidence/awareness extraction, coding |
| `test_phase5_amplification_chain.py` | 39 | Chain stages, cross-case synthesis |
| `test_simulation.py` | 38 | Sigmoid, regimes, critical threshold, parameter sweep |

## Changelog

| Date | Version | Change |
|------|---------|--------|
| Feb 2026 | v0.1 | Initial research agent infrastructure |
| Feb 2026 | v0.2 | Full test suite added (244 tests); test documentation created |

## Paper Reference

Foster-McBride, C. (2026). *The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models*. Draft for arXiv submission.

Original paradox: Foster-McBride, C. (2024). *The AI Trust Paradox: Navigating Verisimilitude in Advanced Language Models*. Digital Human Assistants.
