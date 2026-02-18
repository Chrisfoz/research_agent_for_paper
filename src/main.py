"""
Main orchestration script for the AI Trust Paradox research protocol.

Usage:
  python src/main.py --case all              # Full protocol, both cases
  python src/main.py --case mit_95           # MIT 95% case only
  python src/main.py --case russia_nato      # Russia NATO case only
  python src/main.py --case all --phase 1    # Phase 1 only, both cases
  python src/main.py --case mit_95 --phase 3 # Phase 3, MIT case

Phases:
  1 = Claim Archaeology
  2 = Corpus Prevalence Estimation
  3 = Multi-Model Probing
  4 = Confidence Proxy Extraction
  5 = Amplification Chain Reconstruction
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

console = Console()


def run_phase1(cases: list):
    from src.agents.phase1_claim_archaeology import (
        build_mit_archaeology, build_russia_archaeology
    )
    console.print(Panel("[bold]Phase 1: Claim Archaeology[/bold]"))
    builders = {"mit_95": build_mit_archaeology, "russia_nato": build_russia_archaeology}
    for case in cases:
        arch = builders[case]()
        arch.print_chain()
        out = f"case_studies/{case}/results/phase1_claim_archaeology.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        arch.save(out)
        console.print(f"[green]Saved:[/green] {out}")


def run_phase2(cases: list, live_search: bool = False):
    from src.agents.phase2_corpus_prevalence import (
        build_mit_prevalence, build_russia_prevalence
    )
    console.print(Panel("[bold]Phase 2: Corpus Prevalence Estimation[/bold]"))
    builders = {"mit_95": build_mit_prevalence, "russia_nato": build_russia_prevalence}
    for case in cases:
        est = builders[case]()
        out = f"case_studies/{case}/results/phase2_corpus_prevalence.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        est.save(out)
        console.print(f"  {case}: D/P ratio = [bold]{est.derivative_to_primary_ratio}:1[/bold]")
        console.print(f"[green]Saved:[/green] {out}")


def run_phase3(cases: list, models=None, prompt_types=None):
    from src.agents.phase3_model_probing import run_probing
    console.print(Panel("[bold]Phase 3: Multi-Model Probing[/bold]"))
    for case in cases:
        run_probing(
            case_id=case,
            models=models,
            prompt_types=prompt_types,
        )


def run_phase4(cases: list):
    from src.agents.phase4_confidence_proxy import process_raw_responses, compute_summary_stats
    console.print(Panel("[bold]Phase 4: Confidence Proxy Extraction[/bold]"))
    for case in cases:
        raw_path = f"case_studies/{case}/results/phase3_raw_responses.json"
        if not Path(raw_path).exists():
            console.print(f"[yellow]Skipping {case}: Phase 3 results not found at {raw_path}[/yellow]")
            continue
        results = process_raw_responses(case)
        stats = compute_summary_stats(results)

        table = Table(title=f"Summary: {case}")
        table.add_column("Model")
        table.add_column("A: Full Repro")
        table.add_column("B: Full Repro")
        table.add_column("C: Hedged+")
        table.add_column("D: Correct Source")
        table.add_column("Mean Conf A/B")
        for model, row in stats.items():
            table.add_row(
                model,
                row["type_A_full_reproduction"],
                row["type_B_full_reproduction"],
                row["type_C_hedged_or_less"],
                row["type_D_correct_attribution"],
                row["mean_confidence_AB"],
            )
        console.print(table)


def run_phase5(cases: list):
    from src.agents.phase5_amplification_chain import (
        build_mit_chain, build_russia_chain, synthesise_cross_case_findings
    )
    console.print(Panel("[bold]Phase 5: Amplification Chain Reconstruction[/bold]"))
    chains = {}
    builders = {"mit_95": build_mit_chain, "russia_nato": build_russia_chain}
    for case in cases:
        chain = builders[case]()
        chain.print_chain()
        out = f"case_studies/{case}/results/phase5_amplification_chain.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        chain.save(out)
        chains[case] = chain
        console.print(f"[green]Saved:[/green] {out}")

    if len(chains) == 2:
        synthesis = synthesise_cross_case_findings(chains["mit_95"], chains["russia_nato"])
        out = "results/analysis/cross_case_synthesis.json"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(out, "w", encoding="utf-8") as f:
            json.dump(synthesis, f, indent=2)
        console.print(f"[green]Cross-case synthesis saved:[/green] {out}")


def run_simulation():
    from simulation.model import run_simulation as sim
    console.print(Panel("[bold]Dynamical Model Simulation[/bold]"))
    sim()


PHASE_RUNNERS = {
    1: run_phase1,
    2: run_phase2,
    3: run_phase3,
    4: run_phase4,
    5: run_phase5,
}


def main():
    parser = argparse.ArgumentParser(
        description="AI Trust Paradox — Empirical Protocol Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--case", required=True,
        choices=["mit_95", "russia_nato", "all"],
        help="Which case study to run",
    )
    parser.add_argument(
        "--phase", type=int, choices=[1, 2, 3, 4, 5],
        help="Run a specific phase only (default: all phases)",
    )
    parser.add_argument(
        "--models", nargs="+",
        choices=["claude", "gpt4", "gemini", "llama3", "mistral"],
        help="Models to probe in Phase 3 (default: all)",
    )
    parser.add_argument(
        "--prompt-types", nargs="+",
        choices=["A", "B", "C", "D"],
        help="Prompt types for Phase 3 (default: all)",
    )
    parser.add_argument(
        "--simulate", action="store_true",
        help="Run the dynamical model simulation",
    )
    args = parser.parse_args()

    cases = ["mit_95", "russia_nato"] if args.case == "all" else [args.case]
    phases = [args.phase] if args.phase else [1, 2, 3, 4, 5]

    console.print(Panel(
        f"[bold]AI Trust Paradox Research Protocol[/bold]\n"
        f"Cases: {cases}\n"
        f"Phases: {phases}",
        title="Research Agent"
    ))

    for phase in phases:
        runner = PHASE_RUNNERS[phase]
        if phase == 3:
            runner(cases, args.models, args.prompt_types)
        else:
            runner(cases)

    if args.simulate:
        run_simulation()

    console.print("\n[bold green]Protocol complete.[/bold green]")


if __name__ == "__main__":
    main()
