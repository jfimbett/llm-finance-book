#!/usr/bin/env python3
"""Deterministic generator for the ch09 Loughran-McDonald lexicon figure
(fig:ch09-lm-lexicon). Pure constants from def:lm-dictionary; no data/network.

Run:  python3 gen_lm_lexicon.py
Output: ../../book/chapters/09-financial-nlp-sentiment/figures/fig_lm_lexicon.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt

# Word-list sizes from the Loughran-McDonald Finance dictionary (def:lm-dictionary).
LISTS = [
    ("Negative", 2355),
    ("Litigious", 903),
    ("Positive", 354),
    ("Uncertainty", 297),
    ("Weak modal", 27),
    ("Strong modal", 19),
]

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/09-financial-nlp-sentiment/figures/fig_lm_lexicon.pdf")


def main():
    items = sorted(LISTS, key=lambda t: t[1])
    labels = [t[0] for t in items]
    counts = [t[1] for t in items]

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    bars = ax.barh(range(len(counts)), counts, color="#4c72b0", edgecolor="black",
                   linewidth=0.4)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Number of words")
    ax.set_title("Loughran--McDonald finance dictionary: word-list sizes")
    for i, c in enumerate(counts):
        ax.text(c + 20, i, f"{c:,}", va="center", fontsize=8)
    ax.margins(x=0.12)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
