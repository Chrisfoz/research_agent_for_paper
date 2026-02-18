# Project Plan: AI Trust Paradox Research Agent

## Objective

Execute a methodical, reproducible empirical protocol to test and evidence the
**circular epistemic authority** mechanism described in the working paper
`docs/ai_trust_paradox_revisited_v2_1.docx`.

The outputs will:
1. Generate concrete evidence for both case studies
2. Validate or extend the paper's existing findings
3. Produce structured results for inclusion in the final paper
4. Support arXiv submission

---

## Phase-by-Phase Execution Plan

### Phase 1: Claim Archaeology (Ready to run)
**Status:** Pre-populated from paper. Ready to execute and save.

**Action:**
```bash
python src/main.py --case all --phase 1
```

**Outputs:**
- `case_studies/mit_95/results/phase1_claim_archaeology.json`
- `case_studies/russia_nato/results/phase1_claim_archaeology.json`

**What to verify:**
- [ ] MIT: Original source is MIT NANDA (Challapally et al. July 2025) -- confirmed
- [ ] MIT: Verify Fortune/Forbes amplification dates (Aug 18/21 2025) -- confirmed
- [ ] MIT: Confirm report removal date from MIT domain (Sep 16 2025) -- confirmed
- [ ] Russia: Confirm Mearsheimer (2014) Foreign Affairs article details
- [ ] Russia: Verify Stanford Internet Observatory (2022) report reference
- [ ] Both: Check any additional transformation points not yet documented

---

### Phase 2: Corpus Prevalence Estimation (Partially ready)
**Status:** Estimates from paper pre-populated. Live search optional.

**Action:**
```bash
# Use paper estimates (fast)
python src/main.py --case all --phase 2

# Run live Google search (slow, requires network)
python src/agents/phase2_corpus_prevalence.py --case all --live-search
```

**Outputs:**
- `case_studies/mit_95/results/phase2_corpus_prevalence.json`
- `case_studies/russia_nato/results/phase2_corpus_prevalence.json`

**What to verify/enhance:**
- [ ] MIT: Search Google for "MIT 95% AI pilots fail 2025" variants — count results
- [ ] MIT: Count derivative articles from Fortune/Forbes amplification (Aug-Sep 2025)
- [ ] MIT: Verify report removal from MIT domain (no longer accessible)
- [ ] Russia: Cross-check derivative-to-primary ratio estimate
- [ ] Both: Consider Factiva/GDELT for academic-grade corpus counts

**Key metric:** D/P ratio > 50:1 (MIT) and ~30:1 (Russia)

---

### Phase 3: Multi-Model Probing (Requires API keys)
**Status:** Prompts ready. Requires API keys in `.env`.

**Setup:**
```bash
cp .env.example .env
# Add API keys for: Anthropic, OpenAI, Google, Together, Mistral
pip install -r requirements.txt
```

**Action:**
```bash
# Full run: 60 responses per case (5 models × 4 types × 3 admin)
python src/main.py --case all --phase 3

# Test with one model first
python src/main.py --case mit_95 --phase 3 --models claude

# Run specific prompt types
python src/main.py --case russia_nato --phase 3 --types A B
```

**Outputs:**
- `case_studies/mit_95/results/phase3_raw_responses.json`
- `case_studies/russia_nato/results/phase3_raw_responses.json`

**Expected findings (from paper to replicate):**
- MIT case: 87% unhedged assertion on Type A/B
- MIT case: Only 5% correct attribution (3/60 responses)
- MIT case: 93% consistency across rephrasings
- Russia case: No unhedged assertion; all models show NATO as "prominent framework"
- Russia case: Only 1/60 responses notes coordinated amplification

**Total API calls:** 120 (2 cases × 60 responses each)

---

### Phase 4: Confidence Proxy Extraction (Requires Phase 3)
**Status:** Automated coder implemented. Requires Phase 3 outputs.

**Action:**
```bash
python src/main.py --case all --phase 4
```

**Outputs:**
- `case_studies/mit_95/results/phase4_coded_responses.json`
- `case_studies/russia_nato/results/phase4_coded_responses.json`

**Four coding dimensions:**
1. Reproduction Fidelity (Full / Partial / Non / Contradiction)
2. Attribution Accuracy (Correct / Misattributed / Fabricated / None)
3. Confidence Level (4=Unhedged, 3=Hedged, 2=Uncertain, 1=Refusal)
4. Epistemic Self-Awareness (Spontaneous / Probed / None / Reinforcement)

**Human review:** The automated coder flags ambiguous cases. A second coder
should review a sample (40 responses) to establish inter-rater reliability.
Target: Cohen's κ ≥ 0.82 (as reported in paper).

---

### Phase 5: Amplification Chain Reconstruction (Ready to run)
**Status:** Pre-populated from paper. Ready to execute and save.

**Action:**
```bash
python src/main.py --case all --phase 5
```

**Outputs:**
- `case_studies/mit_95/results/phase5_amplification_chain.json`
- `case_studies/russia_nato/results/phase5_amplification_chain.json`
- `results/analysis/cross_case_synthesis.json`

---

### Simulation (Independent)
**Status:** Ready to run. No API keys required.

**Action:**
```bash
python simulation/model.py
```

**Outputs:**
- `simulation/results/regime_trajectories.json`
- `simulation/results/regime_trajectories.png`
- `simulation/results/parameter_sweep.json`
- `simulation/results/regime_map.png`

**Key finding to replicate:** Critical threshold at A(t) ≈ 0.4 where
amplification-dominant regime becomes stable.

---

## Sub-Agent Strategy

Claude Code sub-agents will be deployed for parallel workstreams:

| Agent | Task | When |
|-------|------|------|
| `Explore` | Verify literature references (Challapally et al. 2025, Mearsheimer 2014, etc.) | Phase 1 |
| `general-purpose` | Web search for corpus prevalence estimates | Phase 2 |
| `Bash` | Execute Phase 3 API calls in parallel per model | Phase 3 |
| `Explore` | Analyse Phase 4 coded results for patterns | Phase 4 |
| `Plan` | Review Phase 5 chain for completeness | Phase 5 |

---

## Priority Order

1. **Immediate:** Run Phases 1, 2, 5 (no API keys needed) — generate baseline results
2. **Next:** Set up API keys, run Phase 3 (core evidence generation)
3. **After Phase 3:** Run Phase 4 coding + human review
4. **Parallel:** Run simulation at any point
5. **Final:** Analysis notebooks + paper update

---

## Success Criteria

### MIT Case Study
- [ ] D/P ratio confirmed > 10:1 (paper claims > 50:1)
- [ ] Type A/B reproduction rate ≥ 80% across models
- [ ] Correct attribution (Challapally et al. / MIT NANDA + scope caveat) ≤ 10% of responses
- [ ] Response consistency ≥ 85% within models

### Russia Case Study
- [ ] NATO expansion appears as "prominent framework" in ≥ 80% Type A/B responses
- [ ] Fewer than 5% responses spontaneously note adversarial amplification
- [ ] Cross-model consistency in framing

### Simulation
- [ ] Three regimes reproduced (correction-dominant, oscillatory, amplification-dominant)
- [ ] Critical threshold at A(t) ≈ 0.4 confirmed
- [ ] Correction requirement: sum(gamma_i) > 0.08 for correction-dominant regime

---

## Timeline

| Task | Estimated effort |
|------|-----------------|
| Phase 1 run + verify | 1-2 hours |
| Phase 2 run + web search | 2-3 hours |
| Phase 3 API setup + run | 3-4 hours |
| Phase 4 coding + human review | 4-6 hours |
| Phase 5 + synthesis | 1-2 hours |
| Simulation | 30 min |
| Analysis notebooks | 4-8 hours |
| Paper update from results | 4-8 hours |

---

## File Naming Convention

```
case_studies/{case}/results/phase{N}_{description}.json
results/analysis/{description}.json
simulation/results/{description}.{json|png}
```

Cases: `mit_95`, `russia_nato`

---

## Notes

- All model responses cached in `case_studies/{case}/results/cache/` — re-running won't duplicate API calls
- Automated coding in Phase 4 is `v1` — human review is essential for academic quality
- The MIT NANDA report (2025) in `docs/` is itself a potential new data point: it found 95% zero ROI, consistent with the circular epistemic authority loop being in operation
- The LinkedIn screenshot (`Screenshot 2026-02-18 085913.png`) shows Toby Stuart (UC Berkeley-Haas) independently questioning the "MIT 95%" claim — useful qualitative corroboration for Phase 1
