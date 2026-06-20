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

# Approximate token counts (billions) from tab:ch08-corpus-summary, with access type.
SOURCES = [
    ("General web / Pile", 800.0, "open"),
    ("Bloomberg News", 300.0, "proprietary"),
    ("SEC EDGAR", 50.0, "open"),
    ("Seeking Alpha", 10.0, "proprietary"),
    ("Earnings transcripts", 5.0, "proprietary"),
    ("Reuters TRC2", 2.0, "licensed"),
    ("SSRN / arXiv", 2.0, "open"),
    ("Financial PhraseBank", 0.005, "open"),
]

COLOR = {"open": "#2ca02c", "proprietary": "#d62728", "licensed": "#1f77b4"}

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/08-domain-specific-llms/figures/fig_corpus.pdf")


def main():
    items = sorted(SOURCES, key=lambda t: t[1])
    labels = [t[0] for t in items]
    counts = [t[1] for t in items]
    colors = [COLOR[t[2]] for t in items]

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.barh(range(len(counts)), counts, color=colors, edgecolor="black", linewidth=0.4)
    ax.set_xscale("log")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Approximate token count (billions, log scale)")
    ax.set_title("Corpus sources for financial LLM pre-training")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLOR.values()]
    ax.legend(handles, COLOR.keys(), loc="lower right", title="access")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
