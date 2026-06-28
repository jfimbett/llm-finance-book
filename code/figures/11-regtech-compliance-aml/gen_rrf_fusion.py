#!/usr/bin/env python3
"""Deterministic generator for the ch11 reciprocal rank fusion figure
(fig:ch11-rrf). Illustrates eq:rrf-fusion on a small fixed example; no data/network.

RRF(d) = sum_r 1 / (kappa + rank_r(d)),  kappa = 60.

Run:  python3 gen_rrf_fusion.py
Output: ../../book/chapters/11-regtech-compliance-aml/figures/fig_rrf.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

KAPPA = 60

# Illustrative ranks (1-based) of five candidate passages under a dense and a
# sparse retriever. A passage relevant on both signals should rise after fusion.
DOCS = ["court filing", "news article", "press release", "blog post", "registry record"]
DENSE_RANK = [1, 3, 2, 5, 4]
SPARSE_RANK = [2, 1, 4, 3, 5]


def rrf(ranks):
    return sum(1.0 / (KAPPA + r) for r in ranks)


def main():
    fused = [rrf([d, s]) for d, s in zip(DENSE_RANK, SPARSE_RANK)]
    order = np.argsort(fused)[::-1]
    labels = [DOCS[i] for i in order]
    scores = [fused[i] for i in order]

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.barh(range(len(scores))[::-1], scores, color="#4c72b0", edgecolor="black",
            linewidth=0.4)
    ax.set_yticks(range(len(scores))[::-1])
    ax.set_yticklabels(labels)
    ax.set_xlabel(r"Reciprocal rank fusion score ($\kappa = 60$)")
    ax.set_title("Hybrid retrieval: reciprocal rank fusion of dense + sparse ranks")
    for y, (i, sc) in enumerate(zip(order, scores)):
        ax.text(sc + 0.0002, len(scores) - 1 - y,
                f"dense #{DENSE_RANK[i]}, sparse #{SPARSE_RANK[i]}",
                va="center", fontsize=7)
    ax.margins(x=0.30)
    fig.tight_layout()
    OUT = (Path(__file__).resolve().parents[3]
           / "book/chapters/11-regtech-compliance-aml/figures/fig_rrf.pdf")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
