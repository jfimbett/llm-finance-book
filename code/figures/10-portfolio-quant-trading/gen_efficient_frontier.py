#!/usr/bin/env python3
"""Deterministic generator for the ch10 mean-variance efficient frontier figure
(fig:ch10-frontier). Fixed 4-asset mu/Sigma; no data/network.

Solves the unconstrained mean-variance frontier in closed form and marks the
maximum-Sharpe (tangency) portfolio and the 1/N equal-weight portfolio, illustrating
the efficient frontier and the 1/N-vs-optimal comparison discussed in the chapter.

Run:  python3 gen_efficient_frontier.py
Output: ../../book/chapters/10-portfolio-quant-trading/figures/fig_frontier.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

# Fixed monthly excess-return assumptions (illustrative), 4 assets.
MU = np.array([0.008, 0.010, 0.006, 0.012])
SIGMA = np.array([
    [0.0040, 0.0010, 0.0008, 0.0015],
    [0.0010, 0.0055, 0.0012, 0.0020],
    [0.0008, 0.0012, 0.0030, 0.0009],
    [0.0015, 0.0020, 0.0009, 0.0070],
])
RF = 0.0
OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/10-portfolio-quant-trading/figures/fig_frontier.pdf")


def main():
    inv = np.linalg.inv(SIGMA)
    ones = np.ones(len(MU))
    A = ones @ inv @ ones
    B = ones @ inv @ MU
    C = MU @ inv @ MU
    D = A * C - B * B

    targets = np.linspace(MU.min() - 0.001, MU.max() + 0.002, 200)
    # Frontier variance for each target mean (closed form).
    var = (A * targets**2 - 2 * B * targets + C) / D
    std = np.sqrt(np.maximum(var, 0))

    # Tangency (max-Sharpe) portfolio.
    w_tan = inv @ (MU - RF) / (ones @ inv @ (MU - RF))
    mu_tan, sd_tan = w_tan @ MU, np.sqrt(w_tan @ SIGMA @ w_tan)
    # Equal-weight 1/N portfolio.
    w_eq = ones / len(MU)
    mu_eq, sd_eq = w_eq @ MU, np.sqrt(w_eq @ SIGMA @ w_eq)

    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.plot(std * 100, targets * 100, color="#4c72b0", label="efficient frontier")
    ax.scatter([sd_tan * 100], [mu_tan * 100], color="#d62728", zorder=5,
               label="max-Sharpe (tangency)")
    ax.scatter([sd_eq * 100], [mu_eq * 100], color="#2ca02c", zorder=5,
               marker="s", label="1/N equal weight")
    ax.set_xlabel("Portfolio volatility (%/month)")
    ax.set_ylabel("Expected excess return (%/month)")
    ax.set_title("Mean-variance efficient frontier (4 assets, illustrative)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT} (tangency Sharpe={mu_tan/sd_tan:.3f}, 1/N Sharpe={mu_eq/sd_eq:.3f})")


if __name__ == "__main__":
    main()
