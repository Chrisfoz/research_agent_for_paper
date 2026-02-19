# Test Documentation: AI Trust Paradox Research Agent

**Project:** AI Trust Paradox — Empirical Research Infrastructure  
**Paper:** "The AI Trust Paradox Revisited: Circular Epistemic Authority in Large Language Models"  
**Author:** Christopher Foster-McBride  
**Test suite created:** February 2026

---

## Overview

This document describes the complete test suite for the research agent codebase. All tests are located in the `tests/` directory and are run with `pytest`. No real API keys are required — all external LLM API calls are mocked.

### Running the Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_coding_framework.py -v

# Run with coverage report
pytest tests/ --cov=src --cov=simulation --cov-report=term-missing

# Run only fast tests (skip slow parameter sweep)
pytest tests/ -v -m "not slow"
```

---

## Test Files

### 1. `tests/conftest.py` — Shared Fixtures

Provides reusable pytest fixtures used across multiple test files. No tests are defined here.

| Fixture | Type | Description |
|---------|------|-------------|
| `mit_unhedged_response_text` | `str` | Typical unhedged MIT 95% claim reproduction (no hedging language) |
| `mit_hedged_response_text` | `str` | Hedged response mentioning 95% with qualifications |
| `mit_correct_attribution_text` | `str` | Response with correct attribution to Challapally / MIT NANDA |
| `russia_nato_prominent_text` | `str` | Response presenting NATO expansion as primary cause |
| `russia_info_ops_text` | `str` | Response noting coordinated amplification by Russian state media |
| `sample_coded_response_full` | `CodedResponse` | Fully coded response: FULL reproduction, MISATTRIBUTED, UNHEDGED, NONE |
| `sample_coded_response_correct` | `CodedResponse` | Correctly attributed response: PARTIAL, CORRECT, HEDGED, SPONTANEOUS |
| `sample_case_results` | `CaseResults` | 60-response CaseResults (5 models × 4 types × 3 admins) for MIT case |
| `raw_responses_mit` | `list[dict]` | Minimal raw Phase 3 response list for MIT case (2 responses) |
| `raw_responses_russia` | `list[dict]` | Minimal raw Phase 3 response list for Russia case (1 response) |
| `tmp_raw_responses_file` | `str` | Path to temp JSON file containing `raw_responses_mit` |
| `tmp_raw_responses_russia_file` | `str` | Path to temp JSON file containing `raw_responses_russia` |

---

### 2. `tests/test_coding_framework.py` — Coding Framework Unit Tests

**Module under test:** [`src/utils/coding_framework.py`](../src/utils/coding_framework.py)

Tests the four-dimensional response coding framework used in Phase 4.

#### `TestEnums` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_reproduction_fidelity_values` | `ReproductionFidelity` enum has correct string values: `full`, `partial`, `non`, `contradiction` |
| `test_attribution_accuracy_values` | `AttributionAccuracy` enum has correct string values: `correct`, `misattributed`, `fabricated`, `none` |
| `test_confidence_level_ordering` | `ConfidenceLevel` integer ordering: UNHEDGED(4) > HEDGED(3) > UNCERTAIN(2) > REFUSAL(1) |
| `test_confidence_level_int_values` | Exact integer values for each confidence level |
| `test_epistemic_awareness_values` | `EpistemicAwareness` enum has correct string values |

#### `TestCodedResponse` (9 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction_minimal` | Minimal construction with required fields; optional fields default to `None` |
| `test_construction_full` | Full construction with all coding dimensions set |
| `test_is_full_reproduction_true` | `is_full_reproduction()` returns `True` when fidelity is FULL |
| `test_is_full_reproduction_false` | `is_full_reproduction()` returns `False` when fidelity is PARTIAL |
| `test_is_confident_unhedged` | `is_confident()` returns `True` for UNHEDGED |
| `test_is_confident_hedged` | `is_confident()` returns `True` for HEDGED (both are "confident") |
| `test_is_not_confident_uncertain` | `is_confident()` returns `False` for UNCERTAIN |
| `test_to_dict_contains_required_keys` | `to_dict()` output contains all required keys |
| `test_to_dict_enum_serialisation` | `to_dict()` output is JSON-serialisable (no raw Enum objects) |

#### `TestCaseResults` (14 tests)

| Test | What it verifies |
|------|-----------------|
| `test_add_and_count` | `add()` appends to `responses` list |
| `test_reproduction_rate_all_full` | `reproduction_rate()` returns 1.0 when all responses are FULL |
| `test_reproduction_rate_none_full` | `reproduction_rate()` returns 0.0 when no responses are FULL |
| `test_reproduction_rate_mixed` | `reproduction_rate()` returns 0.5 for 1 FULL out of 2 |
| `test_reproduction_rate_empty_returns_zero` | `reproduction_rate()` returns 0.0 for empty results |
| `test_mean_confidence_unhedged` | `mean_confidence()` returns 4.0 for all UNHEDGED responses |
| `test_mean_confidence_mixed` | `mean_confidence()` returns 3.5 for UNHEDGED + HEDGED |
| `test_correct_attribution_rate` | `correct_attribution_rate()` returns 0.5 for 1 CORRECT out of 2 |
| `test_filter_by_model` | `_filter(model=...)` returns only responses for that model |
| `test_filter_by_prompt_type` | `_filter(prompt_type=...)` returns only responses for that type |
| `test_filter_combined` | `_filter(model=..., prompt_type=...)` applies both filters |
| `test_to_dict_structure` | `to_dict()` contains `case_id`, `n_responses`, `responses` |
| `test_save_and_load_roundtrip` | `save()` + `load()` preserves case_id and response count |
| `test_save_produces_valid_json` | `save()` writes valid JSON |

#### `TestSummaryTable` (3 tests)

| Test | What it verifies |
|------|-----------------|
| `test_summary_table_keys` | `summary_table()` returns dict with all 5 model keys |
| `test_summary_table_row_keys` | Each row has all 5 required metric keys |
| `test_summary_table_values_in_range` | All rate values in [0,1]; confidence in [0,4] |

**Total: 31 tests**

---

### 3. `tests/test_llm_client.py` — LLM Client Unit Tests

**Module under test:** [`src/utils/llm_client.py`](../src/utils/llm_client.py)

All external API calls are mocked. No API keys required.

#### `TestConstants` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_supported_models_contains_all_five` | `SUPPORTED_MODELS` contains exactly: `claude`, `gpt4`, `gemini`, `llama3`, `mistral` |
| `test_model_display_names_covers_all_supported` | `MODEL_DISPLAY_NAMES` has a non-empty string for every supported model |

#### `TestQueryModel` (10 tests)

| Test | What it verifies |
|------|-----------------|
| `test_unknown_model_raises` | `AssertionError` raised for unknown model name |
| `test_result_dict_structure` | Result dict contains all required keys |
| `test_successful_response` | Response text and metadata correctly populated |
| `test_system_prompt_passed_through` | System prompt forwarded to underlying query function |
| `test_error_captured_in_result` | API exception captured in `error` field; `response` is `None` |
| `test_retry_on_failure` | Retries exactly `retry` times on persistent failure |
| `test_retry_succeeds_on_second_attempt` | Returns response if a later attempt succeeds |
| `test_cache_hit_skips_api_call` | Cached response returned without calling API |
| `test_cache_write_on_success` | Successful response written to cache file |
| `test_timestamp_format` | Timestamp matches ISO 8601 UTC format |

#### `TestQueryFunctions` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_query_claude_calls_anthropic` | `query_claude()` uses Anthropic client and returns response text |
| `test_query_gpt4_calls_openai` | `query_gpt4()` uses OpenAI client and returns response text |
| `test_query_gemini_calls_google` | `query_gemini()` uses Google GenerativeAI and returns response text |
| `test_query_llama3_calls_together` | `query_llama3()` uses Together.ai client and returns response text |
| `test_query_mistral_calls_mistralai` | `query_mistral()` uses Mistral client and returns response text |

**Total: 17 tests**

---

### 4. `tests/test_phase1_claim_archaeology.py` — Phase 1 Unit Tests

**Module under test:** [`src/agents/phase1_claim_archaeology.py`](../src/agents/phase1_claim_archaeology.py)

Tests the claim archaeology data structures and pre-populated case study data.

#### `TestProvenanceNode` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction` | Minimal construction; `url` defaults to `None`, `notes` to `""` |
| `test_optional_url` | URL field correctly stored when provided |

#### `TestClaimArchaeology` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction` | Minimal construction; `provenance_chain` and `transformation_points` default to `[]` |
| `test_add_node` | `add_node()` appends to `provenance_chain` |
| `test_to_dict_is_json_serialisable` | `to_dict()` output is JSON-serialisable |
| `test_save_creates_file` | `save()` creates the output file |
| `test_save_produces_valid_json` | `save()` writes valid JSON with correct `case_id` |

#### `TestBuildMitArchaeology` (14 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"mit_95"` |
| `test_canonical_claim_contains_95` | Canonical claim contains "95%" |
| `test_original_source_cites_challapally` | Original source cites Challapally et al. |
| `test_original_source_cites_mit_nanda` | Original source cites MIT NANDA |
| `test_provenance_chain_has_six_stages` | Exactly 6 provenance nodes |
| `test_stages_are_sequential` | Stage numbers are 1–6 in order |
| `test_stage_1_is_mit_nanda` | Stage 1 actor is MIT NANDA |
| `test_stage_2_is_fortune` | Stage 2 actor/document is Fortune magazine |
| `test_stage_2_date_august_2025` | Stage 2 date is August 2025 |
| `test_stage_4_mentions_mit_removal` | Stage 4 documents MIT report removal |
| `test_derivative_to_primary_ratio_200` | D/P ratio is 200.0 |
| `test_transformation_points_not_empty` | At least 5 transformation points documented |
| `test_transformation_points_mention_fortune` | Fortune mentioned in transformation points |
| `test_notes_mention_toby_stuart` | Notes reference Toby Stuart (UC Berkeley-Haas) corroboration |

#### `TestBuildRussiaArchaeology` (9 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"russia_nato"` |
| `test_canonical_claim_mentions_nato` | Canonical claim mentions NATO |
| `test_original_source_cites_mearsheimer` | Original source cites Mearsheimer (2014) |
| `test_provenance_chain_has_six_stages` | Exactly 6 provenance nodes |
| `test_stages_are_sequential` | Stage numbers are 1–6 in order |
| `test_stage_1_is_realist_scholars` | Stage 1 is realist IR scholars |
| `test_stage_2_is_russian_state_media` | Stage 2 is Russian state media (RT/Sputnik) |
| `test_derivative_to_primary_ratio_30` | D/P ratio is 30.0 |
| `test_notes_mention_adversarial` | Notes acknowledge adversarial amplification |

**Total: 30 tests**

---

### 5. `tests/test_phase2_corpus_prevalence.py` — Phase 2 Unit Tests

**Module under test:** [`src/agents/phase2_corpus_prevalence.py`](../src/agents/phase2_corpus_prevalence.py)

Tests corpus prevalence estimation data structures and pre-populated estimates.

#### `TestSearchResult` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction` | Minimal construction; `notes` defaults to `""` |
| `test_with_notes` | Notes field correctly stored |

#### `TestPrevalenceEstimate` (4 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction` | Minimal construction; `search_results` and `time_series` default to empty |
| `test_to_dict_is_json_serialisable` | `to_dict()` output is JSON-serialisable |
| `test_save_creates_file` | `save()` creates the output file |
| `test_save_produces_valid_json` | `save()` writes valid JSON with correct fields |

#### `TestBuildMitPrevalence` (11 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"mit_95"` |
| `test_primary_source_count_is_one` | Primary source count is 1 |
| `test_derivative_count_at_least_200` | Derivative count ≥ 200 |
| `test_dp_ratio_at_least_200` | D/P ratio ≥ 200.0 |
| `test_time_series_not_empty` | Time series has at least one entry |
| `test_time_series_has_august_2025` | Time series includes August 2025 (Fortune article date) |
| `test_time_series_values_increase_after_fortune` | Count increases after Fortune article |
| `test_search_results_not_empty` | At least one search result documented |
| `test_search_results_contain_mit_queries` | Search queries reference MIT or 95% |
| `test_primary_source_mentions_challapally` | Primary source cites Challapally |
| `test_notes_mention_removal` | Notes document MIT report removal |

#### `TestBuildRussiaPrevalence` (7 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"russia_nato"` |
| `test_primary_source_count_is_one` | Primary source count is 1 |
| `test_dp_ratio_around_30` | D/P ratio ≈ 30.0 |
| `test_time_series_has_2022_spike` | 2022 (full invasion) has highest count |
| `test_search_results_contain_nato_queries` | Search queries reference NATO |
| `test_search_results_contain_russian_language_query` | At least one Russian-language query |
| `test_notes_mention_adversarial` | Notes acknowledge adversarial/coordinated amplification |

#### `TestEstimateSearchCount` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_raises_when_googlesearch_unavailable` | `RuntimeError` raised when `googlesearch-python` not installed |
| `test_returns_count_when_available` | Returns correct count when search is available (mocked) |

#### `TestRunLivePrevalenceEstimation` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_returns_dict_with_query_keys` | Returns dict keyed by query strings |
| `test_handles_search_error_gracefully` | Returns `-1` for failed queries without raising |

**Total: 28 tests**

---

### 6. `tests/test_phase3_model_probing.py` — Phase 3 Unit Tests

**Module under test:** [`src/agents/phase3_model_probing.py`](../src/agents/phase3_model_probing.py)

All LLM API calls are mocked. Tests the prompt structure and probing runner.

#### `TestPromptStructure` (9 tests)

| Test | What it verifies |
|------|-----------------|
| `test_mit_prompts_has_four_types` | MIT prompts has exactly types A, B, C, D |
| `test_russia_prompts_has_four_types` | Russia prompts has exactly types A, B, C, D |
| `test_each_type_has_three_variants` | Every prompt type has exactly 3 variants (administrations) |
| `test_prompts_dict_contains_both_cases` | `PROMPTS` dict has both `mit_95` and `russia_nato` |
| `test_mit_type_a_mentions_ai_failure` | Type A MIT prompts ask about AI failure/investment |
| `test_mit_type_d_asks_for_source` | Type D MIT prompts ask for source/citation |
| `test_russia_type_a_asks_about_ukraine` | Type A Russia prompts ask about Ukraine |
| `test_russia_type_c_challenges_nato_claim` | Type C Russia prompts challenge the NATO claim |
| `test_system_prompt_is_non_empty` | System prompt is not empty |

#### `TestRunProbing` (11 tests)

| Test | What it verifies |
|------|-----------------|
| `test_returns_correct_number_of_responses_all_models_all_types` | 5 × 4 × 3 = 60 responses for full run |
| `test_returns_correct_number_single_model` | 1 × 4 × 3 = 12 responses for single model |
| `test_returns_correct_number_single_type` | 5 × 1 × 3 = 15 responses for single type |
| `test_each_response_has_required_keys` | Each response dict has `model`, `response`, `case_id`, `prompt_type`, `administration` |
| `test_case_id_set_on_each_response` | `case_id` correctly set on all responses |
| `test_administration_index_1_to_3` | Administration indices are 1, 2, 3 |
| `test_saves_json_file` | `phase3_raw_responses.json` created in output directory |
| `test_saved_json_is_valid` | Saved JSON is valid and contains correct number of responses |
| `test_api_error_captured_not_raised` | API errors captured in response dict; `run_probing` does not raise |
| `test_unknown_case_raises` | `AssertionError` raised for unknown case ID |

#### `TestSummariseResponses` (3 tests)

| Test | What it verifies |
|------|-----------------|
| `test_counts_ok_responses` | Correctly counts successful vs error responses |
| `test_groups_by_model_and_type` | Groups responses by (model, prompt_type) tuple |
| `test_empty_responses` | Returns empty dict for empty input |

**Total: 23 tests**

---

### 7. `tests/test_phase4_confidence_proxy.py` — Phase 4 Unit Tests

**Module under test:** [`src/agents/phase4_confidence_proxy.py`](../src/agents/phase4_confidence_proxy.py)

Tests the automated response coding logic.

#### `TestCountPatternMatches` (11 tests)

| Test | What it verifies |
|------|-----------------|
| `test_no_matches` | Returns 0 for unrelated text |
| `test_single_match` | Returns ≥ 1 for text with one hedging phrase |
| `test_multiple_matches` | Returns ≥ 2 for text with multiple hedging phrases |
| `test_case_insensitive` | Pattern matching is case-insensitive |
| `test_mit_claim_pattern_matches_95_percent` | Detects "95%" in text |
| `test_mit_claim_pattern_matches_ninety_five` | Detects "ninety-five percent" in text |
| `test_correct_source_matches_challapally` | Detects "Challapally" as correct source |
| `test_correct_source_matches_mit_nanda` | Detects "MIT NANDA" as correct source |
| `test_russia_claim_pattern_matches_nato_expansion` | Detects "NATO expansion caused" pattern |
| `test_info_ops_pattern_matches_rt` | Detects "RT and Sputnik" as info ops markers |
| `test_info_ops_pattern_matches_coordinated` | Detects "coordinated amplification" as info ops marker |

#### `TestExtractConfidenceLevel` (4 tests)

| Test | What it verifies |
|------|-----------------|
| `test_unhedged_no_hedging_words` | Unhedged assertion → `UNHEDGED` |
| `test_hedged_with_some_research` | "some research suggests" → `HEDGED` or `UNCERTAIN` |
| `test_uncertain_many_hedges` | Many hedging phrases → `UNCERTAIN` |
| `test_plain_assertion_is_unhedged` | Plain factual statement → `UNHEDGED` |

#### `TestExtractEpistemicAwareness` (4 tests)

| Test | What it verifies |
|------|-----------------|
| `test_spontaneous_caveat_on_type_a` | Caveat in Type A response → `SPONTANEOUS` |
| `test_probed_caveat_on_type_c` | Caveat in Type C response → `PROBED` |
| `test_none_when_no_caveat` | No caveat → `NONE` or `REINFORCEMENT` |
| `test_reinforcement_when_strong_assertion` | "MIT confirmed... well-established" → `REINFORCEMENT` |

#### `TestAnalyseMitResponse` (6 tests)

| Test | What it verifies |
|------|-----------------|
| `test_full_reproduction_with_misattribution` | "MIT research, 95%" → FULL + MISATTRIBUTED |
| `test_correct_attribution_with_challapally` | Challapally citation → CORRECT attribution |
| `test_non_reproduction_when_no_95` | No 95% figure → NON reproduction |
| `test_returns_four_tuple` | Returns (fidelity, attribution, confidence, awareness) |
| `test_confidence_unhedged_for_plain_assertion` | Plain assertion → UNHEDGED |
| `test_hedged_response_gives_hedged_confidence` | Hedged text → HEDGED or UNCERTAIN |

#### `TestAnalyseRussiaResponse` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_full_reproduction_nato_prominent` | "primary cause... NATO" → FULL reproduction |
| `test_correct_attribution_with_info_ops` | Info ops noted → CORRECT attribution |
| `test_spontaneous_info_ops_awareness_on_type_a` | Info ops in Type A → SPONTANEOUS |
| `test_non_reproduction_when_no_nato` | No NATO mention → NON reproduction |
| `test_returns_four_tuple` | Returns (fidelity, attribution, confidence, awareness) |

#### `TestProcessRawResponses` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_processes_mit_responses` | Loads raw JSON, returns `CaseResults` with responses |
| `test_saves_output_file` | Output JSON file created |
| `test_output_is_valid_json` | Output is valid JSON with `case_id` and `responses` |
| `test_skips_null_responses` | Responses with `response: null` are skipped |
| `test_processes_russia_responses` | Russia case correctly processed |

#### `TestComputeSummaryStats` (3 tests)

| Test | What it verifies |
|------|-----------------|
| `test_returns_dict_with_all_models` | Returns dict with all 5 model keys |
| `test_each_row_has_required_keys` | Each row has all 5 metric keys |
| `test_values_are_strings_with_percent_or_fraction` | Percentage fields end with `%`; confidence field contains `/4` |

**Total: 38 tests**

---

### 8. `tests/test_phase5_amplification_chain.py` — Phase 5 Unit Tests

**Module under test:** [`src/agents/phase5_amplification_chain.py`](../src/agents/phase5_amplification_chain.py)

Tests the amplification chain data structures and cross-case synthesis.

#### `TestChainStage` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction_minimal` | Minimal construction; `evidence` and `key_finding` default to `""` |
| `test_construction_full` | Full construction with all fields |

#### `TestAmplificationChain` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_construction` | Minimal construction; `stages` and `key_observations` default to `[]` |
| `test_add_stage` | `add_stage()` appends to `stages` list |
| `test_to_dict_is_json_serialisable` | `to_dict()` output is JSON-serialisable |
| `test_save_creates_file` | `save()` creates the output file |
| `test_save_produces_valid_json` | `save()` writes valid JSON with correct `case_id` |

#### `TestBuildMitChain` (13 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"mit_95"` |
| `test_has_six_stages` | Exactly 6 chain stages |
| `test_stages_are_sequential` | Stage numbers are 1–6 in order |
| `test_stage_1_is_mit_nanda` | Stage 1 actor is MIT NANDA |
| `test_stage_2_is_fortune` | Stage 2 actor is Fortune magazine |
| `test_stage_3_mentions_200_outlets` | Stage 3 documents 200+ derivative articles |
| `test_stage_4_mentions_mit_removal` | Stage 4 documents MIT report removal |
| `test_stage_6_mentions_circular_authority` | Stage 6 describes circular authority loop closure |
| `test_key_observations_not_empty` | At least 5 key observations |
| `test_key_observations_mention_87_percent` | Key observations reference 87% unhedged assertion rate |
| `test_cross_case_comparison_not_empty` | Cross-case comparison text is non-empty |
| `test_cross_case_mentions_russia` | Cross-case comparison references Russia/adversarial case |
| `test_save_and_reload` | `save()` produces reloadable JSON with 6 stages |

#### `TestBuildRussiaChain` (9 tests)

| Test | What it verifies |
|------|-----------------|
| `test_case_id` | `case_id` is `"russia_nato"` |
| `test_has_six_stages` | Exactly 6 chain stages |
| `test_stages_are_sequential` | Stage numbers are 1–6 in order |
| `test_stage_1_is_realist_scholars` | Stage 1 is realist IR scholars (Mearsheimer) |
| `test_stage_2_is_russian_state_media` | Stage 2 is Russian state media |
| `test_stage_3_mentions_coordinated_networks` | Stage 3 documents coordinated inauthentic networks |
| `test_stage_4_mentions_debunking_paradox` | Stage 4 documents debunking paradox |
| `test_key_observations_mention_1_in_60` | Key observations reference 1/60 info ops detection rate |
| `test_key_observations_mention_pfisterer` | Key observations cite Pfisterer et al. (2025) |

#### `TestSynthesiseCrossCaseFindings` (10 tests)

| Test | What it verifies |
|------|-----------------|
| `test_returns_dict` | Returns a dict |
| `test_has_structural_unity_key` | Contains `structural_unity` key |
| `test_has_key_difference_key` | Contains `key_difference` key |
| `test_has_debunking_paradox_key` | Contains `debunking_paradox` key |
| `test_has_provenance_blindness_key` | Contains `provenance_blindness` key |
| `test_has_governance_implication_key` | Contains `governance_implication` key |
| `test_key_difference_has_both_cases` | `key_difference` has entries for both `mit_95` and `russia_nato` |
| `test_structural_unity_mentions_frequency_bias` | Structural unity text mentions frequency bias |
| `test_governance_mentions_corpus` | Governance implication mentions corpus |
| `test_is_json_serialisable` | Synthesis output is JSON-serialisable |

**Total: 39 tests**

---

### 9. `tests/test_simulation.py` — Simulation Model Unit Tests

**Module under test:** [`simulation/model.py`](../simulation/model.py)

Tests the dynamical model of Circular Epistemic Authority (CEA). No API keys required.

#### `TestSimParams` (9 tests)

| Test | What it verifies |
|------|-----------------|
| `test_default_alpha` | Default `alpha` = 0.1 (paper Table 8) |
| `test_default_a_initial` | Default `A_initial` = 0.2 (2024 baseline) |
| `test_default_beta` | Default `beta` = 5.0 |
| `test_default_theta` | Default `theta` = 2.5 |
| `test_default_gamma_sum` | Sum of all gamma values = 0.20 |
| `test_default_p_initial` | Default `P_initial` = 0.1 |
| `test_default_t_steps` | Default `T_steps` = 100 |
| `test_custom_params` | Custom parameters correctly stored |

#### `TestSimResult` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_final_prevalence_empty` | Returns 0.0 for empty prevalence list |
| `test_final_prevalence_returns_last` | Returns last element of prevalence list |
| `test_regime_label_correction_dominant` | Final prevalence < 0.05 → `correction_dominant` |
| `test_regime_label_amplification_dominant` | Final prevalence > 0.8 → `amplification_dominant` |
| `test_regime_label_oscillatory` | Final prevalence in (0.05, 0.8) → `oscillatory` |

#### `TestSigmoid` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_sigmoid_zero_is_half` | `sigmoid(0) = 0.5` |
| `test_sigmoid_large_positive_approaches_one` | `sigmoid(100) > 0.999` |
| `test_sigmoid_large_negative_approaches_zero` | `sigmoid(-100) < 0.001` |
| `test_sigmoid_is_monotonically_increasing` | Strictly increasing over [-5, 5] |
| `test_sigmoid_output_in_zero_one` | Output always in (0, 1) |

#### `TestSimulate` (8 tests)

| Test | What it verifies |
|------|-----------------|
| `test_output_length_matches_t_steps` | `prevalence`, `confidence`, `autonomy` lists have length `T_steps` |
| `test_prevalence_bounded_zero_one` | All prevalence values in [0, 1] |
| `test_confidence_bounded_zero_one` | All confidence values in [0, 1] |
| `test_regime_label_set` | `regime` is one of the three valid labels |
| `test_correction_dominant_regime` | High gamma, low alpha/A → correction dominant |
| `test_amplification_dominant_regime` | High alpha/A, low gamma → amplification dominant |
| `test_initial_prevalence_respected` | First prevalence value equals `P_initial` |
| `test_autonomy_does_not_exceed_a_max` | Autonomy never exceeds `A_max` |

#### `TestCriticalThreshold` (3 tests)

| Test | What it verifies |
|------|-----------------|
| `test_low_autonomy_correction_dominant` | A=0.2 → not amplification-dominant |
| `test_high_autonomy_amplification_dominant` | A=0.6 → not correction-dominant |
| `test_threshold_around_0_4` | A=0.2 not amplification-dominant; A=0.6 not correction-dominant |

#### `TestRunParameterSweep` (5 tests)

| Test | What it verifies |
|------|-----------------|
| `test_output_has_required_keys` | Output has `alphas`, `autonomies`, `grid` |
| `test_grid_dimensions` | Grid shape matches `len(alphas) × len(autonomies)` |
| `test_grid_values_bounded` | All grid values in [0, 1] |
| `test_alphas_range` | Alpha values in [0, 1] |
| `test_is_json_serialisable` | Sweep output is JSON-serialisable |

#### `TestPlotFunctions` (2 tests)

| Test | What it verifies |
|------|-----------------|
| `test_plot_regimes_runs_without_error` | `plot_regimes()` completes without exception (matplotlib mocked) |
| `test_plot_regime_map_runs_without_error` | `plot_regime_map()` completes without exception (matplotlib mocked) |

#### `TestRunSimulation` (1 test)

| Test | What it verifies |
|------|-----------------|
| `test_saves_trajectory_json` | Three regime trajectories produced: correction-dominant, oscillatory, amplification-dominant |

**Total: 38 tests**

---

## Test Summary

| File | Test Classes | Tests | API Mocked | Requires API Keys |
|------|-------------|-------|------------|-------------------|
| `test_coding_framework.py` | 4 | 31 | N/A | No |
| `test_llm_client.py` | 3 | 17 | Yes | No |
| `test_phase1_claim_archaeology.py` | 4 | 30 | N/A | No |
| `test_phase2_corpus_prevalence.py` | 6 | 28 | Yes (search) | No |
| `test_phase3_model_probing.py` | 3 | 23 | Yes (LLMs) | No |
| `test_phase4_confidence_proxy.py` | 7 | 38 | N/A | No |
| `test_phase5_amplification_chain.py` | 5 | 39 | N/A | No |
| `test_simulation.py` | 8 | 38 | Yes (matplotlib) | No |
| **Total** | **40** | **244** | | **None** |

---

## What the Tests Do NOT Cover

The following require live API keys and are intentionally excluded from the automated test suite:

1. **Live LLM responses** — Phase 3 actual model outputs (GPT-4, Claude, Gemini, Llama 3, Mistral)
2. **Live Google search** — Phase 2 live corpus prevalence estimation
3. **Phase 4 human review** — Inter-rater reliability (Cohen's κ ≥ 0.82 target)
4. **End-to-end integration** — Full `python src/main.py --case all` run

These are covered by the empirical protocol itself, documented in `PROJECT_PLAN.md`.

---

## Design Principles

1. **No API keys required** — All external calls mocked with `unittest.mock`
2. **Empirical facts as tests** — Key paper claims (D/P ratio 200:1, 6-stage chains, 87% unhedged rate) are encoded as assertions
3. **Serialisation coverage** — Every data class tested for JSON round-trip fidelity
4. **Boundary conditions** — Simulation tests cover all three regimes and the critical threshold
5. **Error handling** — API failures, missing files, and unknown inputs all tested
6. **Fixture reuse** — `conftest.py` provides shared fixtures to avoid duplication

---

## Adding New Tests

When adding new functionality:

1. Add fixtures to `conftest.py` if they will be reused across test files
2. Follow the naming convention: `test_{module_name}.py`
3. Group tests into classes by the function/class under test
4. Mock all external API calls — tests must run without network access
5. Encode any new empirical claims from the paper as assertions
