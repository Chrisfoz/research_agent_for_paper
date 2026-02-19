# AI Trust Paradox Research Summary

## Project: Circular Epistemic Authority in Large Language Models

**Author:** Christopher Foster-McBride (Independent Researcher)
**Date:** February 2026
**Status:** Draft for arXiv submission

---

## Executive Summary

This research investigates the **Circular Epistemic Authority** mechanism in Large Language Models (LLMs) — where LLMs treat corpus frequency as a proxy for truth, creating self-reinforcing feedback loops that can cause false or misleading claims to gain credibility through sheer repetition.

### Key Findings

1. **Both case studies show high derivative-to-primary ratios:**
   - MIT 95% AI Failure Claim: D/P ratio >200:1
   - Russia/NATO Narrative: D/P ratio ~30:1

2. **Simulation confirms three distinct regime behaviors:**
   - Correction-dominant: High autonomy + low prevalence → claims can be corrected
   - Amplification-dominant: Low autonomy + high prevalence → claims become self-perpetuating
   - Critical threshold: Parameter region where system tips toward amplification

---

## Case Study Results

### Case Study 1: MIT 95% AI Failure Claim (Non-Adversarial)

| Metric | Value |
|--------|-------|
| Primary Source | MIT NANDA "The GenAI Divide" (July 2025) |
| Derivative Count | 200+ articles |
| D/P Ratio | >200:1 |
| Peak Prevalence | August 2025 (Fortune, Forbes coverage) |
| Outcome | Report removed Sep 16, 2025 but claim persists |

**Amplification Chain:**
1. MIT NANDA releases internal report (July 2025)
2. Fortune picks up story (Aug 18, 2025) → stock drops in NVIDIA, ARM, Palantir
3. Forbes, Axios, 200+ outlets replicate within 72 hours
4. MIT distances: "unpublished, non-peer-reviewed work"
5. Debunking articles restate claim → further corpus prevalence increase
6. Claim outlives its source

### Case Study 2: Russia/NATO Narrative (Adversarial)

| Metric | Value |
|--------|-------|
| Primary Sources | Mearsheimer (2014) + Russian state amplification |
| Derivative Count | ~30x primary |
| D/P Ratio | ~30:1 |
| Cross-linguistic Pattern | Russian leads English by 2-4 weeks |
| Temporal Clustering | Crimea 2014, Donbas 2021-2022, Feb 2022 invasion |

**Key Distinction:** Unlike MIT case, this narrative has legitimate scholarly roots (Mearsheimer's realist IR theory) combined with deliberate adversarial amplification (RT, Sputnik, coordinated social media).

---

## Simulation Results

### Regime Analysis

The dynamical model identifies three behavioral regimes based on two key parameters:

- **α (alpha):** Prevalence multiplier — how much a claim's current prevalence increases reproduction probability
- **A (autonomy):** Model autonomy — tendency to rely on external verification vs. corpus frequency

| Regime | Parameters | Outcome |
|--------|------------|---------|
| Correction-dominant | α=0.05, A=0.1 | Prevalence → 0.001 (claim decays) |
| Equilibrium | α=0.1, A=0.2 | Prevalence → 0.008 (stable, low) |
| Amplification-dominant | α=0.3, A=0.5 | Prevalence → 1.0 (claim saturates) |

### Critical Threshold

The regime map (see `regime_map.png`) reveals a **critical threshold** where:
- Below threshold: Correction mechanisms dominant
- Above threshold: Amplification feedback takes over

This threshold corresponds to the point where LLM reliance on corpus frequency overwhelms verification mechanisms.

---

## Methodology Notes

### Data Sources for Corpus Prevalence

Three complementary data sources are used:

| Source | Coverage | Strengths | Limitations |
|--------|----------|-----------|-------------|
| **Google** | General web | Broad coverage, easy API | Includes low-quality sources |
| **Factiva** | Professional news (30k+ sources) | High-quality journalism, verified sources | Requires subscription |
| **GDELT** | 100+ languages, global | Multilingual, includes translations | API rate limits |

### Phase Protocol

1. **Claim Archaeology** — Source provenance chain
2. **Corpus Prevalence** — D/P ratio estimation (Google + Factiva + GDELT)
3. **Multi-Model Probing** — Test reproduction across 5+ LLMs
4. **Confidence Proxy** — Extract confidence scores
5. **Amplification Chain** — Reconstruct spread mechanism

---

## Conclusions

1. **Circular epistemic authority is empirically verifiable** — Both case studies demonstrate the mechanism
2. **The feedback loop is robust** — Debunking often increases claim prevalence (illusory truth effect)
3. **Critical threshold exists** — Below certain prevalence/autonomy parameters, correction is possible
4. **Adversarial narratives are harder to counter** — Legitimate academic sources mixed with amplification

### Implications for AI Development

- Corpus frequency should not be treated as truth proxy
- Verification mechanisms must be integrated into LLM training
- Awareness of circular epistemic authority is crucial for AI literacy

---

## Files in This Directory

| File | Description |
|------|-------------|
| `regime_trajectories.json` | Time-series outputs for different parameter regimes |
| `parameter_sweep.json` | Grid of (α, A) → final prevalence values |
| `regime_trajectories.png` | Visualization of regime dynamics |
| `regime_map.png` | 2D parameter sweep heatmap |
| `SUMMARY.md` | This file |

---

## References

- McKenna et al. (2023) — Corpus-term-frequency heuristics in LLMs
- Pfisterer et al. (2025) — Illusory truth effect in LLMs
- Challapally et al. (2025) — MIT NANDA "The GenAI Divide"
- Mearsheimer (2014) — Why the West is losing the Ukraine war
- Shumailov et al. (2024) — Model collapse

---

*Generated: February 2026*
