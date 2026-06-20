#!/usr/bin/env python3
"""Deterministic generator for the ch13 reliability diagram (fig:ch13-reliability).

Uses the fixed bin statistics from Example ex:ch13-ece-credit (no data/network).
Bins of width 0.2; mean predicted probability vs empirical accuracy per bin.
The gap between the bars and the diagonal is the per-bin calibration error that ECE
aggregates (ECE = 0.115 in the example).

Run:  python3 gen_reliability_diagram.py
Output: ../../book/chapters/13-llm-limitations-evaluation/figures/fig_reliability.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

# Fixed bins from ex:ch13-ece-credit.
CONF = np.array([0.08, 0.31, 0.50, 0.71, 0.88])   # mean predicted prob per bin
ACC = np.array([0.11, 0.28, 0.47, 0.55, 0.62])    # empirical accuracy per bin
COUNT = np.array([120, 180, 200, 300, 200])

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/13-llm-limitations-evaluation/figures/fig_reliability.pdf")


def main():
    ece = float(np.sum(COUNT / COUNT.sum() * np.abs(CONF - ACC)))

    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    ax.plot([0, 1], [0, 1], "--", color="gray", label="perfect calibration")
    ax.bar(CONF, ACC, width=0.16, color="#4c72b0", edgecolor="black",
           linewidth=0.5, alpha=0.85, label="model accuracy")
    # Mark the calibration gap for each bin.
    for c, a in zip(CONF, ACC):
        ax.plot([c, c], [a, c], color="#d62728", linewidth=1.2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Mean predicted probability (confidence)")
    ax.set_ylabel("Empirical accuracy")
    ax.set_title(f"Reliability diagram (ECE = {ece:.3f})")
    ax.legend(loc="upper left")
    ax.set_aspect("equal")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT} (ECE={ece:.3f})")


if __name__ == "__main__":
    main()
