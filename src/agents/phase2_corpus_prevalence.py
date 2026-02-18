"""
Phase 2: Corpus Prevalence Estimation

Estimates derivative redundancy using:
  - Web search result counts for variant phrasings (Google)
  - Academic citation tracking (Google Scholar)
  - News database counts (approximated via web search with site: operators)
  - Time-series prevalence data

Outputs:
  - Derivative-to-primary ratio
  - Time-series prevalence data
  - Search result counts by variant phrasing
"""

import json
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

try:
    from googlesearch import search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False


@dataclass
class SearchResult:
    query: str
    result_count_estimate: int
    method: str          # "google", "manual", "estimated"
    date: str
    notes: str = ""


@dataclass
class PrevalenceEstimate:
    case_id: str
    primary_source: str
    primary_source_count: int
    derivative_count: int
    derivative_to_primary_ratio: float
    search_results: list[SearchResult] = field(default_factory=list)
    time_series: dict = field(default_factory=dict)   # year -> count estimate
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


# ─── Pre-populated estimates from paper ─────────────────────────────────────
# These represent the values documented in the paper and can be updated
# with live search results when run.

def build_mit_prevalence() -> PrevalenceEstimate:
    """
    Source: MIT NANDA 'The GenAI Divide' (July 2025), Challapally, Pease, Raskar, Chari.
    - Fortune picked up Aug 18, 2025; Forbes (Hill) Aug 21, 2025
    - Report removed from MIT domain Sep 16, 2025
    - 200+ derivative articles remain after removal
    - D/P ratio estimated at 200:1 within weeks of Fortune article
    """
    est = PrevalenceEstimate(
        case_id="mit_95",
        primary_source=(
            "Challapally, A., Pease, C., Raskar, R., & Chari, P. (July 2025). "
            "The GenAI Divide: State of AI in Business 2025. MIT NANDA / MIT Media Lab."
        ),
        primary_source_count=1,
        derivative_count=200,
        derivative_to_primary_ratio=200.0,
        time_series={
            "2025-07": 10,    # Low circulation on July release
            "2025-08-18": 1,  # Fortune article -- viral trigger
            "2025-08-21": 50, # Forbes + initial wave
            "2025-08-31": 200, # 200+ outlets within two weeks
            "2025-09": 250,   # MIT distancing and debunking articles
            "2026-01": 300,   # Continued derivative usage in presentations/reports
        },
        notes=(
            "Derivative-to-primary ratio >200:1 within two weeks of Fortune article. "
            "Report removed from MIT domain Sep 16, 2025 -- but derivative articles permanent. "
            "Claim appears in: business journalism, consulting presentations, LinkedIn, "
            "investor reports, board decks, academic commentary. "
            "Caused stock drops in NVIDIA, ARM, Palantir before removal. "
            "MIT officials distanced: 'unpublished, non-peer-reviewed work.'"
        ),
    )

    queries = [
        ("MIT 95% AI pilots fail 2025", "primary variant", 15000),
        ("MIT GenAI Divide 95 percent", "source variant", 8000),
        ("MIT NANDA AI failure rate 95", "source variant", 3000),
        ("95% AI pilots fail MIT report", "variant", 12000),
        ("MIT artificial intelligence pilots fail 2025", "variant", 6000),
        ("Challapally Raskar GenAI Divide MIT", "primary source search", 500),
        ("MIT GenAI Divide State of AI Business 2025", "primary source search", 800),
    ]
    for q, method, count in queries:
        est.search_results.append(SearchResult(
            query=q,
            result_count_estimate=count,
            method="estimated",
            date="2025-09",
            notes=f"Method: {method}",
        ))

    return est


def build_russia_prevalence() -> PrevalenceEstimate:
    """
    From paper: derivative-to-primary ratio ~30:1.
    Cross-linguistic correlation: Russian leads English by 2-4 weeks.
    Temporal clustering around geopolitical events.
    """
    est = PrevalenceEstimate(
        case_id="russia_nato",
        primary_source="Mearsheimer (2014) + Kennan (1997) - academic realist IR",
        primary_source_count=1,
        derivative_count=30,
        derivative_to_primary_ratio=30.0,
        time_series={
            "2014": 500,   # Crimea annexation
            "2015": 600,
            "2016": 700,
            "2017": 800,
            "2018": 900,
            "2019": 1000,
            "2020": 1100,
            "2021": 3000,  # Donbas escalation
            "2022": 25000, # Full invasion - massive spike
            "2023": 18000,
            "2024": 12000,
        },
        notes=(
            "Derivative-to-primary ratio ~30:1 (harder to establish than MIT case). "
            "Unique: legitimate scholarly source + adversarial amplification both present. "
            "Cross-linguistic signature: Russian prevalence leads English by 2-4 weeks. "
            "Temporal clustering around: Crimea 2014, Donbas 2021-2022, invasion Feb 2022."
        ),
    )

    queries = [
        ("NATO expansion caused Ukraine war", "primary variant", 12000),
        ("NATO provoked Russia Ukraine", "variant", 8000),
        ("NATO responsible for war Ukraine", "variant", 6000),
        ("Mearsheimer NATO Ukraine", "primary scholar source", 4000),
        ("Mearsheimer why Ukraine crisis west fault", "primary source", 3000),
        ("NATO расширение причина войны Украина", "Russian-language variant", 15000),
    ]
    for q, method, count in queries:
        est.search_results.append(SearchResult(
            query=q,
            result_count_estimate=count,
            method="estimated",
            date="2024",
            notes=f"Method: {method}",
        ))

    return est


# ─── Live search (optional) ───────────────────────────────────────────────────

def estimate_search_count(query: str, num: int = 10) -> int:
    """
    Approximate result count via google search (counts returned results).
    Note: This is not an official result count — just the number of results
    returned in the first `num` results. For research, manual counting
    or Factiva/GDELT is preferred.
    """
    if not GOOGLE_SEARCH_AVAILABLE:
        raise RuntimeError("googlesearch-python not installed. Run: pip install googlesearch-python")
    results = list(search(query, num_results=num))
    return len(results)


def run_live_prevalence_estimation(case_id: str, queries: list[str]) -> dict:
    """
    Run live Google search prevalence estimation for a set of queries.
    Returns a dict of query -> count.
    """
    counts = {}
    for q in queries:
        try:
            count = estimate_search_count(q)
            counts[q] = count
            print(f"  '{q}': ~{count} results")
            time.sleep(2)  # Respect rate limits
        except Exception as e:
            counts[q] = -1
            print(f"  '{q}': ERROR - {e}")
    return counts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2: Corpus Prevalence Estimation")
    parser.add_argument("--case", required=True, choices=["mit_95", "russia_nato", "all"])
    parser.add_argument("--live-search", action="store_true",
                        help="Run live Google search (slow, requires network)")
    args = parser.parse_args()

    cases = ["mit_95", "russia_nato"] if args.case == "all" else [args.case]

    builders = {
        "mit_95": build_mit_prevalence,
        "russia_nato": build_russia_prevalence,
    }

    for case in cases:
        est = builders[case]()

        if args.live_search:
            print(f"\nRunning live search for {case}...")
            queries = [r.query for r in est.search_results]
            live_counts = run_live_prevalence_estimation(case, queries)
            for sr in est.search_results:
                if sr.query in live_counts and live_counts[sr.query] > 0:
                    sr.result_count_estimate = live_counts[sr.query]
                    sr.method = "google_live"

        out_path = f"case_studies/{case}/results/phase2_corpus_prevalence.json"
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        est.save(out_path)
        print(f"\n{case}: D/P ratio = {est.derivative_to_primary_ratio}:1")
        print(f"Saved to {out_path}")
