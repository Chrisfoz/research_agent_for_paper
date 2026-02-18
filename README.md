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
```

## Paper Reference

Foster-McBride, C. (2026). *The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models*. Draft for arXiv submission.

Original paradox: Foster-McBride, C. (2024). *The AI Trust Paradox: Navigating Verisimilitude in Advanced Language Models*. Digital Human Assistants.
