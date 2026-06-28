#!/usr/bin/env python3
"""Deterministic generator for the ch15 DP privacy-utility tradeoff figure
(fig:ch15-privacy-utility). Illustrative schematic, no data/network.

It plots an illustrative differentially-private fine-tuning utility curve: test
accuracy as a function of the privacy budget epsilon, holding delta fixed. Smaller
epsilon (stronger privacy) costs more utility; as epsilon grows the curve saturates
toward the non-private baseline. The functional form is a saturating exponential chosen
only to illustrate the qualitative tradeoff described in the chapter (it is NOT measured
data); the marked points at epsilon=1 and epsilon=10 match the text's discussion.

Run:  python3 gen_dp_privacy_utility.py
Output: ../../book/chapters/15-privacy-local-models/figures/fig_privacy_utility.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

NONPRIVATE = 0.90   # illustrative non-private test accuracy
FLOOR = 0.55        # illustrative accuracy at very strong privacy
RATE = 0.45         # saturation rate

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/15-privacy-local-models/figures/fig_privacy_utility.pdf")


def main():
    eps = np.linspace(0.1, 10.0, 200)
    acc = NONPRIVATE - (NONPRIVATE - FLOOR) * np.exp(-RATE * eps)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(eps, acc, color="#4c72b0", linewidth=2, label="DP-SGD (illustrative)")
    ax.axhline(NONPRIVATE, ls="--", color="gray", label="non-private baseline")
    for e in (1.0, 10.0):
        a = NONPRIVATE - (NONPRIVATE - FLOOR) * np.exp(-RATE * e)
        ax.scatter([e], [a], color="#d62728", zorder=5)
        ax.annotate(f"$\\varepsilon={e:.0f}$", (e, a), textcoords="offset points",
                    xytext=(6, -10), fontsize=9)
    ax.set_xlabel("Privacy budget $\\varepsilon$ (smaller = stronger privacy)")
    ax.set_ylabel("Test accuracy")
    ax.set_title("Privacy--utility tradeoff for DP fine-tuning (illustrative)")
    ax.set_ylim(0.5, 0.95)
    ax.legend(loc="lower right")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
