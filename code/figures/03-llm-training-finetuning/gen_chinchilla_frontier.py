#!/usr/bin/env python3
"""Deterministic generator for the ch03 Chinchilla frontier (fig:ch03-illustration).

Plots the Hoffmann et al. (2022) compute-optimal frontier (parameters vs. tokens)
and overlays a fixed set of public model checkpoints to show which were over- or
under-trained relative to their compute budget. Network-free and deterministic.

Run:  python3 gen_chinchilla_frontier.py
Output: ../../book/chapters/03-llm-training-finetuning/figures/fig_illustration.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

# Chinchilla coefficients (Hoffmann et al. 2022, Table A3).
COMPUTE = np.logspace(20, 26, 400)          # FLOPs
N_OPT = 0.1192 * COMPUTE ** 0.4937          # optimal parameters
D_OPT = 2.1714 * COMPUTE ** 0.4977          # optimal tokens

# Public model checkpoints: (parameters, training tokens).
MODELS = {
    "GPT-3":      (175e9,  300e9),
    "PaLM":       (540e9,  780e9),
    "Gopher":     (280e9,  300e9),
    "Chinchilla": ( 70e9,  1.4e12),
    "LLaMA-7B":   (  7e9,  1.0e12),
    "LLaMA-65B":  ( 65e9,  1.4e12),
}
COLORS = ["#e41a1c", "#377eb8", "#ff7f00", "#4daf4a", "#984ea3", "#a65628"]

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/03-llm-training-finetuning/figures/fig_illustration.pdf")


def main():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(N_OPT / 1e9, D_OPT / 1e9, "k-", lw=2,
              label="Chinchilla optimal frontier")
    for (name, (n, d)), c in zip(MODELS.items(), COLORS):
        ax.scatter(n / 1e9, d / 1e9, color=c, s=90, zorder=5)
        ax.annotate(name, xy=(n / 1e9, d / 1e9), xytext=(5, 4),
                    textcoords="offset points", fontsize=8, color=c)
    ax.set_xlabel("Model Parameters (B)")
    ax.set_ylabel("Training Tokens (B)")
    ax.set_title("Chinchilla Scaling Law: Compute-Optimal Frontier\n"
                 "(Hoffmann et al. 2022)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight", dpi=150)
    print(f"wrote {OUT} ({len(MODELS)} models)")


if __name__ == "__main__":
    main()
