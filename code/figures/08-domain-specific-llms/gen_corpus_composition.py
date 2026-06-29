#!/usr/bin/env python3
"""Deterministic generator for the ch08 pre-training corpus figure
(fig:ch08-corpus). Pure constants from the chapter's corpus-summary table; no network.

Run:  python3 gen_corpus_composition.py
Output: ../../book/chapters/08-domain-specific-llms/figures/fig_corpus.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

# Approximate token counts (billions) from tab:ch08-corpus-summary.
SOURCES = [
    ("General web / Pile", 800.0),
    ("Bloomberg News", 300.0),
    ("SEC EDGAR", 50.0),
    ("Seeking Alpha", 10.0),
    ("Earnings transcripts", 5.0),
    ("Reuters TRC2", 2.0),
    ("SSRN / arXiv", 2.0),
    ("Financial PhraseBank", 0.005),
]

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/08-domain-specific-llms/figures/fig_corpus.pdf")


def main():
    items = sorted(SOURCES, key=lambda t: t[1])
    labels = [t[0] for t in items]
    counts = [t[1] for t in items]

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.barh(range(len(counts)), counts, color="#4c72b0", edgecolor="black", linewidth=0.4)
    ax.set_xscale("log")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Approximate token count (billions, log scale)")
    ax.set_title("Corpus sources for financial LLM pre-training")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
