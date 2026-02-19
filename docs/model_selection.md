# Phase 3 Model Selection: Rationale and Case-Study Tables

**Project:** "The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models"
**Author:** Christopher Foster-McBride
**Data source:** LifeArchitect.ai Models Table — Dr Alan D. Thompson (2026), 760 models, `docs/2026 LifeArchitect.ai data (shared) - NEW.xlsx`
**Date prepared:** February 2026

---

## 1. Why Model Selection Is Theoretically Significant

The paper's core mechanism — circular epistemic authority — predicts that a model's susceptibility to reproducing a false claim is a function of:

1. **Corpus prevalence at training time**: Was the claim in the model's training data, and at what frequency?
2. **Architectural propensity**: Does the model's design (Dense vs. MoE, retrieval-augmented vs. parametric, reasoning vs. standard) modulate frequency-for-validity substitution?
3. **Retrieval-layer exposure**: For RAG-enabled deployments, even a single source is sufficient (Germain 2026).

These three variables make model selection a research design decision, not merely a technical one. Models selected must vary along dimensions that allow the paper to disentangle:
- Temporal prevalence (training cutoff relative to claim publication)
- Architectural vulnerability (Dense vs. MoE; parametric vs. RAG-augmented)
- Lab-level design choices (Anthropic's apparent resistance in Germain vs. OpenAI/Google's vulnerability)

---

## 2. Selection Criteria Framework

| Criterion | Rationale |
|-----------|-----------|
| **Training cutoff relative to claim** | Primary control variable for MIT 95% case; enables pre/post comparison |
| **Publication date** | Proxy for training cutoff when exact cutoff undisclosed |
| **Architecture (Dense / MoE / Reasoning)** | Tests whether architectural type modulates reproduction rates |
| **Lab** | Controls for lab-level training choices (RLHF, filtering, RAG integration) |
| **GPQA / MMLU benchmark** | Controls for raw capability; prevents confounding capability with susceptibility |
| **API accessibility** | Practical requirement for Phase 3 execution |
| **Germain experiment result** | Empirical evidence of RAG-layer vulnerability (Claude resistant; ChatGPT/Gemini vulnerable) |

---

## 3. Key Temporal Landmarks

### Case Study 1: MIT 95% Claim

| Event | Date |
|-------|------|
| MIT NANDA "GenAI Divide" published (preliminary) | July 2025 |
| Fortune article — viral spread begins | August 18, 2025 |
| Forbes/Hill article (peak amplification) | August 21, 2025 |
| NVIDIA/ARM/Palantir stock drops | August 18–21, 2025 |
| Report removed from MIT domain | September 16, 2025 |
| Debunking coverage peaks | September–October 2025 |
| **Training cutoff dividing line (pre/post-claim)** | **~July 2025** |

**Prediction**: Models with training cutoffs *after* ~August 2025 will reproduce the "95% AI failure" claim with higher fidelity and confidence than models with pre-July 2025 cutoffs — even where the training data includes the debunking (Prediction P6: debunking reinforces corpus prevalence).

### Case Study 2: Russia/NATO Narrative

| Event | Date |
|-------|------|
| Mearsheimer (2014) — academic origin of NATO critique | September 2014 |
| Russia invades Ukraine — narrative massively amplified | February 24, 2022 |
| Russian state media saturation peaks (RT, Sputnik) | 2022–2023 |
| Cross-linguistic corpus saturation established | 2023–2024 |
| **Training cutoff dividing line (low/high saturation)** | **~February 2022** |

**Prediction**: All models with training cutoffs after February 2022 will have substantial exposure. The research question is whether *degree* of exposure (D/P ratio at training time) correlates with reproduction confidence — a more nuanced gradient than the binary pre/post structure of Case Study 1.

---

## 4. Model Selection Table — Case Study 1: MIT 95% Claim

> **Critical design point:** The MIT 95% case study tests a *temporal amplification hypothesis*. Without models whose training cutoffs fall **after** the claim's viral spread (August 2025), there is no experimental group — only controls. The paper's central prediction is that models with post-August 2025 training cutoffs will reproduce the claim with higher fidelity and confidence than pre-claim models. Post-claim models are therefore **essential to the primary set**, not optional extensions.

### The Two-Lineage Problem

The MIT 95% case has two distinct lineages:
- **Lineage A (2019):** Ransbotham/BCG misattributed as "MIT study: 95% fail" — already in training data of *all* pre-2025 models. Pre-claim models may still reproduce a "95% AI failure" claim, but from this older corpus signal, not from MIT NANDA 2025.
- **Lineage B (2025):** MIT NANDA "GenAI Divide" — specifically "95% of organizations are getting zero return" — only enters training data of models with cutoffs after ~July 2025.

This two-lineage structure means the experiment tests not just whether models reproduce "MIT 95%", but **which version** they reproduce and with what attribution. Distinguishing Lineage A from Lineage B responses is a key coding task in Phase 4.

### Temporal Stratification Design

| Group | Training Cutoff | Models | Prediction |
|-------|----------------|--------|-----------|
| **Group A: Pre-claim control** | Before July 2025 | 4 models | May reproduce Lineage A (2019 myth) but NOT Lineage B (MIT NANDA 2025) |
| **Group B: Post-claim experimental** | After August 2025 | 3 models | Should reproduce Lineage B with high fidelity; tests P6 if debunking included |

### Model Selection Table

Models ordered by estimated training cutoff. Bold rows = Group B (post-claim, experimental group).

| # | Model | Lab | Published | Est. Training Cutoff | Arch | MMLU | GPQA | Group | Germain Profile | Phase 3 Role |
|---|-------|-----|-----------|---------------------|------|------|------|-------|-----------------|--------------|
| 1 | Gemini 1.5 Pro | Google DeepMind | Feb 2024 | ~Nov 2023 | MoE | 85.9 | 46.2 | A — Control | Vulnerable | Google pre-claim baseline |
| 2 | Claude 3 Opus | Anthropic | Mar 2024 | ~Aug 2023 | MoE | 86.8 | 59.5 | A — Control | Resistant | Anthropic pre-claim baseline |
| 3 | Llama 3.1 405B | Meta AI | Jul 2024 | ~Dec 2023 | Dense | 88.6 | 51.1 | A — Control | Unknown | Open weights; Dense vs. MoE contrast |
| 4 | GPT-4o (2024-11-20) | OpenAI | Nov 2024 | ~Oct 2024 | MoE | 85.7 | 46.0 | A — Control | Vulnerable | Closest pre-claim OpenAI; paired with GPT-5.2 |
| **5** | **Gemini 3** | **Google DeepMind** | **Nov 2025** | **~Aug 2025** | **MoE** | **—** | **93.8** | **B — Experimental** | **Vulnerable** | **Boundary case; early viral spread; pairs with Model 1** |
| **6** | **GPT-5.2** | **OpenAI** | **Dec 2025** | **~Sep 2025** | **MoE** | **91.3** | **93.2** | **B — Experimental** | **Vulnerable** | **Post-viral; debunking cycle beginning; pairs with Model 4** |
| **7** | **Claude Sonnet 4.6** | **Anthropic** | **Feb 2026** | **~Oct 2025** | **MoE** | **88.7** | **89.9** | **B — Experimental** | **Resistant** | **Full cycle incl. debunking; tests P6; self-referential note** |

**Primary Phase 3 set (7 models):** All seven above — 4 controls + 3 experimental. This is the minimum viable design for the temporal amplification hypothesis.

**Reduced set if API access is constrained (5 models):** Models 1, 4, 5, 6, 7 — preserves the pre/post structure and the Google same-lab pair (1 vs. 5), the OpenAI same-lab pair (4 vs. 6), and the Anthropic resistant+post model (7). Drop Models 2 and 3.

### Key Comparison Pairs

| Pair | Models | What It Isolates |
|------|--------|-----------------|
| Google temporal | Gemini 1.5 Pro (Nov 2023 cutoff) vs. Gemini 3 (Aug 2025 cutoff) | Temporal prevalence effect; same lab and vulnerability profile |
| OpenAI temporal | GPT-4o (Oct 2024 cutoff) vs. GPT-5.2 (Sep 2025 cutoff) | Temporal prevalence; same lab and vulnerability profile |
| Resistance under saturation | Claude 3 Opus (Aug 2023) vs. Claude Sonnet 4.6 (Oct 2025) | Does Anthropic's resistance persist post-claim, including through the debunking corpus? |
| Architecture under exposure | Llama 3.1 405B (Dense, Dec 2023) vs. Gemini 3 (MoE, Aug 2025) | Architecture × temporal exposure interaction |

### Methodological Note: Claude Sonnet 4.6 (Model 7)

Claude Sonnet 4.6 is the model executing this research infrastructure (as of February 2026). Its inclusion in Phase 3 is self-referential and should be disclosed in the paper. Justifications:

1. Its post-claim training cutoff (~October 2025) makes it the only Anthropic model trained on the *full cycle* including both viral spread and debunking
2. Anthropic's demonstrated resistance in the Germain experiment generates the contrast hypothesis: even a resistant architecture, with full debunking corpus exposure, may show P6 effects
3. Self-referential probing of AI systems about their own epistemic properties is methodologically interesting for a paper about circular epistemic authority

---

## 5. Model Selection Table — Case Study 2: Russia/NATO Narrative

For Russia/NATO, the narrative has been building since 2014 and massively amplified since February 2022. The gradient of exposure is more continuous than the binary pre/post structure of Case Study 1. Models are selected to capture three saturation levels.

| # | Model | Lab | Published | Est. Training Cutoff | Arch | GPQA | Russia/NATO Exposure Level | Key Variable |
|---|-------|-----|-----------|---------------------|------|------|----------------------------|-------------|
| 1 | Claude 3 Opus | Anthropic | Mar 2024 | ~Aug 2023 | MoE | 59.5 | High (18 months post-invasion) | Anthropic resistance baseline |
| 2 | Gemini 1.5 Pro | Google DeepMind | Feb 2024 | ~Nov 2023 | MoE | 46.2 | High (21 months post-invasion) | Google vulnerability baseline |
| 3 | Llama 3.1 405B | Meta AI | Jul 2024 | ~Dec 2023 | Dense | 51.1 | High (22 months post-invasion) | Open weights; architecture |
| 4 | Mistral Large 2 | Mistral | Jul 2024 | ~Feb 2024 | Dense | — | High (24 months post-invasion) | European/multilingual training |
| 5 | GPT-4o (2024-11-20) | OpenAI | Nov 2024 | ~Oct 2024 | MoE | 46.0 | Very high (32 months post-invasion) | Vulnerable architecture, later cutoff |
| 6 | Claude 3.7 Sonnet | Anthropic | Feb 2025 | ~Sep 2024 | Dense | 84.8 | Very high (31 months post-invasion) | Resistant architecture, later cutoff |
| 7 | Gemini 3 | Google DeepMind | Nov 2025 | ~Aug 2025 | MoE | 93.8 | Maximum (42 months post-invasion) | Highest capability, vulnerable |
| 8 | Claude Sonnet 4.6 | Anthropic | Feb 2026 | ~Oct 2025 | MoE | 89.9 | Maximum (44 months post-invasion) | Highest Anthropic model, resistant |

**All eight models post-date the February 2022 invasion**, which is expected and appropriate: we are measuring *degree* of reproduction and confidence variation, not binary exposure.

**Key hypotheses for Russia/NATO:**
- H1: Models from labs shown to be Germain-resistant (Anthropic) will reproduce the NATO claim with lower fidelity than Germain-vulnerable models (Google, OpenAI)
- H2: Mistral (Dense, European training) will show lower reproduction rates than US-lab MoE models, reflecting different corpus composition
- H3: Reproduction confidence will be relatively stable across model generations (high saturation since 2022 means even early models have high corpus exposure)

**Contrast with MIT 95%:** H3 predicts no significant temporal gradient for Russia/NATO (because saturation was achieved early), while MIT 95% should show a clear temporal gradient. Testing both predictions together strengthens the paper's theoretical framework.

---

## 6. Architecture Reference Summary

| Architecture | Description | Examples in Selection | Theoretical Relevance |
|-------------|-------------|----------------------|----------------------|
| **Dense** | All parameters active per inference | Llama 3.1 405B, Mistral Large 2, Claude 3.7 Sonnet | Baseline parametric behaviour |
| **MoE (Mixture of Experts)** | Sparse activation; subset of experts per token | GPT-4o, Gemini 1.5 Pro, Claude 3 Opus, Gemini 3, Claude Sonnet 4.6 | Dominant frontier architecture; scalable |
| **Reasoning (Extended CoT)** | Test-time compute; chain-of-thought generation | Claude 3.7 Sonnet, Gemini 3 (reasoning mode) | Tests whether explicit reasoning reduces frequency bias |
| **RAG-augmented** | Retrieval at inference time | Gemini AI Overviews, ChatGPT web search | Germain experiment shows single-source vulnerability at retrieval layer |

**Note:** Phase 3 as designed probes parametric memory (no live web retrieval). Retrieval-augmented behaviour is captured separately via the Germain addendum.

---

## 7. Phase 3 Implementation Notes

### MIT 95% — Full 7-model set (recommended)

The pre/post temporal split requires **all seven models**. This is the minimum viable design for the core hypothesis test.

```
mit_95:
  # GROUP A: Pre-claim controls (training cutoff before July 2025)
  group_a_controls:
    - gemini-1.5-pro           # Google DeepMind, MoE, cutoff ~Nov 2023, Germain-vulnerable
    - claude-3-opus-20240229   # Anthropic, MoE, cutoff ~Aug 2023, Germain-resistant
    - meta-llama/Llama-3.1-405B-Instruct  # Meta, Dense, cutoff ~Dec 2023
    - gpt-4o-2024-11-20        # OpenAI, MoE, cutoff ~Oct 2024, Germain-vulnerable

  # GROUP B: Post-claim experimental (training cutoff after August 2025)
  group_b_experimental:
    - gemini-3                 # Google DeepMind, MoE, cutoff ~Aug 2025, Germain-vulnerable
    - gpt-5.2                  # OpenAI, MoE, cutoff ~Sep 2025, Germain-vulnerable
    - claude-sonnet-4-6        # Anthropic, MoE, cutoff ~Oct 2025, Germain-resistant
```

### MIT 95% — Reduced 5-model set (API budget constrained)

Preserves the same-lab pairs essential for clean temporal comparison; drops Models 2 and 3.

```
mit_95_reduced:
  group_a_controls:
    - gemini-1.5-pro           # Google pre-claim baseline
    - gpt-4o-2024-11-20        # OpenAI pre-claim baseline
  group_b_experimental:
    - gemini-3                 # Google post-claim (pairs with gemini-1.5-pro)
    - gpt-5.2                  # OpenAI post-claim (pairs with gpt-4o)
    - claude-sonnet-4-6        # Anthropic post-claim; tests P6 on resistant architecture
```

### Russia/NATO — 7-model set (same models; all post-invasion)

```
russia_nato:
  models:
    - gemini-1.5-pro
    - claude-3-opus-20240229
    - meta-llama/Llama-3.1-405B-Instruct
    - gpt-4o-2024-11-20
    - gemini-3
    - gpt-5.2
    - claude-sonnet-4-6
```

### Query count

| Configuration | Models | Prompt types | Variants | Queries per case | Total (both cases) |
|---------------|--------|-------------|----------|------------------|--------------------|
| Full 7-model | 7 | 4 | 3 | 84 | 168 |
| Reduced 5-model (MIT) + 7-model (NATO) | varies | 4 | 3 | 60 / 84 | 144 |

### API keys required

| Model(s) | Provider | Environment variable |
|----------|----------|---------------------|
| GPT-4o (2024-11-20), GPT-5.2 | OpenAI | `OPENAI_API_KEY` |
| Claude 3 Opus, Claude Sonnet 4.6 | Anthropic | `ANTHROPIC_API_KEY` |
| Gemini 1.5 Pro, Gemini 3 | Google | `GOOGLE_API_KEY` |
| Llama 3.1 405B | Together.ai | `TOGETHER_API_KEY` |

> Note: Mistral Large 2 dropped from primary set (no strong same-lab pairing available for the MIT temporal comparison). Can be re-added as an additional control if budget permits.

---

## 8. Data Source Citation

Thompson, A. D. (2026). *Models Table*. LifeArchitect.ai. https://lifearchitect.ai/models-table/

The LifeArchitect.ai dataset (760 models as of February 2026) provides:
- Publication date by month
- Architecture classification (Dense, MoE, MatFormer, Diffusion)
- Benchmark scores: MMLU, MMLU-Pro, GPQA, HLE
- Lab affiliation
- Parameter count and training token count

Training cutoff dates are *estimated* in this document based on the typical lag between training cutoff and public release (approximately 4–8 months for frontier models). Where official training cutoff dates have been published by labs, those take precedence.
