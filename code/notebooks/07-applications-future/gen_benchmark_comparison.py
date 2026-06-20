#!/usr/bin/env python3
"""Deterministic generator for the ch07 benchmark-comparison figure
(fig:ch07-illustration). Pure constants (published benchmark scores); no network.

Run:  python3 gen_benchmark_comparison.py
Output: ../../book/chapters/07-applications-future/figures/fig_illustration.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

BENCHMARKS = ["FinQA\n(exact match)", "FPB\n(accuracy)", "FiQA-SA\n(F1)"]
# Approximate scores from the original papers / FinBench survey (illustrative).
MODELS = {
    "BERT-base":    [0.11, 0.73, 0.64],
    "FinBERT":      [0.13, 0.87, 0.76],
    "GPT-3.5":      [0.52, 0.78, 0.79],
    "GPT-4":        [0.68, 0.83, 0.84],
    "BloombergGPT": [0.23, 0.85, 0.75],
}

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/07-applications-future/figures/fig_illustration.pdf")


def main():
    n_models = len(MODELS)
    x = np.arange(len(BENCHMARKS))
    width = 0.15

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    for i, (name, scores) in enumerate(MODELS.items()):
        ax.bar(x + (i - (n_models - 1) / 2) * width, scores, width, label=name,
               edgecolor="black", linewidth=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS)
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.0)
    ax.set_title("LLM families on three financial NLP benchmarks")
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=8)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
