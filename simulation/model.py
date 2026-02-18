"""
Dynamical model of Circular Epistemic Authority (CEA).

From paper Section 10: Dynamical Model and Simulation.

Core equations:
  P_c(t+1) = P_c(t) + alpha * A(t) * T_hat_c(t) - sum_i(gamma_i * K^i_c(t))
  T_hat_c(t) = sigma(beta * P_c(t) - theta)

Where:
  P_c(t)     : corpus prevalence of claim c at time t
  T_hat_c(t) : model confidence proxy
  A(t)       : delegated autonomy (fraction of knowledge tasks mediated by LLMs)
  alpha      : amplification rate (proportion of model output reingested per cycle)
  beta       : sensitivity to prevalence in confidence sigmoid
  theta      : confidence threshold for unhedged assertion
  gamma_i    : correction efficacy coefficients
  K^i_c(t)   : correction mechanisms {fact-check, credibility, re-ranking, human}

Three regimes:
  1. Correction-dominant: sum(gamma_i) > alpha * A * max(dT/dP) — false claims decay
  2. Oscillatory (balanced): claims fluctuate around non-zero prevalence
  3. Amplification-dominant: alpha * A > sum(gamma_i) — false claims converge to high prevalence
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class SimParams:
    """Simulation parameters — from paper Table 8."""
    alpha: float = 0.1        # amplification rate [0.01, 0.5]
    A_initial: float = 0.2    # initial delegated autonomy (2024 baseline) [0.05, 0.8]
    A_growth: float = 0.03    # annual growth in A(t)
    A_max: float = 0.8
    beta: float = 5.0         # sigmoid sensitivity [2, 10]
    theta: float = 2.5        # confidence threshold [1, 5]
    gamma_factcheck: float = 0.05   # fact-checking correction efficacy [0, 0.3]
    gamma_credibility: float = 0.05  # credibility scoring
    gamma_reranking: float = 0.05   # search re-ranking
    gamma_human: float = 0.05       # human editorial
    P_initial: float = 0.1    # initial prevalence of false claim
    T_steps: int = 100         # number of time steps


@dataclass
class SimResult:
    params: SimParams
    prevalence: list[float] = field(default_factory=list)
    confidence: list[float] = field(default_factory=list)
    autonomy: list[float] = field(default_factory=list)
    regime: str = ""

    def final_prevalence(self) -> float:
        return self.prevalence[-1] if self.prevalence else 0.0

    def regime_label(self) -> str:
        if self.final_prevalence() < 0.05:
            return "correction_dominant"
        elif self.final_prevalence() > 0.8:
            return "amplification_dominant"
        else:
            return "oscillatory"


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def simulate(params: SimParams) -> SimResult:
    """Run one simulation trajectory."""
    result = SimResult(params=params)
    P = params.P_initial
    A = params.A_initial

    gamma_total = (
        params.gamma_factcheck
        + params.gamma_credibility
        + params.gamma_reranking
        + params.gamma_human
    )

    for t in range(params.T_steps):
        T_hat = sigmoid(params.beta * P - params.theta)

        # Correction saturation: effectiveness decreases at high prevalence
        correction_saturation = 1.0 - P * 0.5
        effective_correction = gamma_total * correction_saturation * P

        P_new = P + params.alpha * A * T_hat - effective_correction
        P_new = np.clip(P_new, 0.0, 1.0)

        result.prevalence.append(float(P))
        result.confidence.append(float(T_hat))
        result.autonomy.append(float(A))

        P = P_new
        A = min(params.A_max, A + params.A_growth / params.T_steps)

    result.regime = result.regime_label()
    return result


def run_parameter_sweep() -> dict:
    """
    Sweep alpha and A to identify regime boundaries.
    Returns a grid of final prevalence values.
    """
    alphas = np.linspace(0.01, 0.5, 20)
    autonomies = np.linspace(0.05, 0.8, 20)
    grid = np.zeros((len(alphas), len(autonomies)))

    for i, alpha in enumerate(alphas):
        for j, A in enumerate(autonomies):
            p = SimParams(alpha=alpha, A_initial=A, A_growth=0.0)  # fixed A
            result = simulate(p)
            grid[i, j] = result.final_prevalence()

    return {"alphas": alphas.tolist(), "autonomies": autonomies.tolist(), "grid": grid.tolist()}


def plot_regimes(results: list[SimResult], output_path: str = None):
    """Plot three regime trajectories."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for result in results:
        label = f"alpha={result.params.alpha}, A0={result.params.A_initial} ({result.regime})"
        axes[0].plot(result.prevalence, label=label)
        axes[1].plot(result.confidence, label=label)

    axes[0].set_title("Corpus Prevalence P(t)")
    axes[0].set_xlabel("Time steps (training-deployment cycles)")
    axes[0].set_ylabel("Prevalence (normalised)")
    axes[0].legend(fontsize=7)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title("Model Confidence T̂(t)")
    axes[1].set_xlabel("Time steps")
    axes[1].set_ylabel("Confidence proxy")
    axes[1].legend(fontsize=7)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Plot saved to {output_path}")
    else:
        plt.show()
    plt.close()


def plot_regime_map(sweep_data: dict, output_path: str = None):
    """Plot phase diagram of regimes."""
    import numpy as np
    grid = np.array(sweep_data["grid"])
    alphas = sweep_data["alphas"]
    autonomies = sweep_data["autonomies"]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(
        grid, origin="lower", aspect="auto",
        extent=[autonomies[0], autonomies[-1], alphas[0], alphas[-1]],
        cmap="RdYlGn_r", vmin=0, vmax=1
    )
    plt.colorbar(im, ax=ax, label="Final Prevalence P(T)")
    ax.set_xlabel("Delegated Autonomy A")
    ax.set_ylabel("Amplification Rate α")
    ax.set_title("CEA Phase Diagram: Regime Map\n(Green=Correction dominant, Red=Amplification dominant)")

    # Add critical threshold annotation
    ax.axvline(x=0.4, color="white", linestyle="--", linewidth=2, label="Critical threshold (A≈0.4)")
    ax.legend(fontsize=9)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Regime map saved to {output_path}")
    else:
        plt.show()
    plt.close()


def run_simulation():
    """Run all simulations and save results."""
    print("\n=== CEA Dynamical Model Simulation ===\n")

    # Three representative regimes from paper
    regime_params = [
        SimParams(alpha=0.05, A_initial=0.1, A_growth=0.0,
                  gamma_factcheck=0.1, gamma_credibility=0.1,
                  gamma_reranking=0.1, gamma_human=0.1),   # Correction-dominant
        SimParams(alpha=0.1, A_initial=0.2, A_growth=0.01),   # Oscillatory (baseline)
        SimParams(alpha=0.3, A_initial=0.5, A_growth=0.02,
                  gamma_factcheck=0.02, gamma_credibility=0.02,
                  gamma_reranking=0.02, gamma_human=0.02),  # Amplification-dominant
    ]

    results = [simulate(p) for p in regime_params]
    for r in results:
        print(f"  Regime: {r.regime:30s} | Final prevalence: {r.final_prevalence():.3f}")

    # Save trajectory data
    trajectory_data = []
    for r in results:
        trajectory_data.append({
            "regime": r.regime,
            "params": {
                "alpha": r.params.alpha,
                "A_initial": r.params.A_initial,
                "gamma_total": (r.params.gamma_factcheck + r.params.gamma_credibility
                                + r.params.gamma_reranking + r.params.gamma_human),
            },
            "final_prevalence": r.final_prevalence(),
            "prevalence": r.prevalence,
            "confidence": r.confidence,
        })

    out_dir = Path("simulation/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "regime_trajectories.json", "w") as f:
        json.dump(trajectory_data, f, indent=2)
    print(f"  Trajectories saved to simulation/results/regime_trajectories.json")

    plot_regimes(results, str(out_dir / "regime_trajectories.png"))

    # Parameter sweep
    print("\nRunning parameter sweep...")
    sweep = run_parameter_sweep()
    with open(out_dir / "parameter_sweep.json", "w") as f:
        json.dump(sweep, f, indent=2)
    plot_regime_map(sweep, str(out_dir / "regime_map.png"))
    print("  Parameter sweep complete.")

    # Critical threshold analysis (from paper)
    print("\nCritical threshold analysis:")
    for A in [0.2, 0.3, 0.4, 0.5, 0.6]:
        p = SimParams(alpha=0.1, A_initial=A, A_growth=0.0)
        r = simulate(p)
        print(f"  A={A:.1f}: {r.regime:30s} | P(final)={r.final_prevalence():.3f}")

    print("\nSimulation complete. Results in simulation/results/")


if __name__ == "__main__":
    run_simulation()
