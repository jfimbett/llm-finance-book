#!/usr/bin/env python3
"""Deterministic generator for the ch01 TF-IDF heatmap (fig:ch01-illustration).

Uses a FIXED set of representative headlines per ticker (committed below), not a live
yfinance fetch, so the figure regenerates identically with no data or network dependence.

Run:  python3 gen_tfidf_headlines.py
Output: ../../book/chapters/01-intro/figures/fig_illustration.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Fixed, representative headlines (illustrative; not a live feed).
HEADLINES = {
    "AAPL": [
        "Apple unveils new iPhone with faster chip and improved camera",
        "Apple services revenue hits record as iPhone sales steady",
        "Analysts raise Apple price target on strong iPhone demand",
        "Apple expands App Store and Mac lineup ahead of holidays",
    ],
    "MSFT": [
        "Microsoft Azure cloud growth accelerates on AI demand",
        "Microsoft integrates Copilot AI across Windows and Office",
        "Microsoft raises dividend as cloud and software revenue climbs",
        "Microsoft data centre expansion boosts Azure capacity",
    ],
    "JPM": [
        "JPMorgan profit rises on higher net interest income",
        "JPMorgan boosts loan loss reserves amid credit caution",
        "JPMorgan trading revenue strong as deposits stabilise",
        "JPMorgan raises guidance on net interest income outlook",
    ],
}

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/01-intro/figures/fig_illustration.pdf")


def main():
    tickers = list(HEADLINES)
    docs = [" ".join(HEADLINES[t]) for t in tickers]  # one document per ticker
    vec = TfidfVectorizer(stop_words="english", max_features=12)
    X = vec.fit_transform(docs).toarray()
    terms = vec.get_feature_names_out()

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    im = ax.imshow(X, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(terms)))
    ax.set_xticklabels(terms, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(tickers)))
    ax.set_yticklabels(tickers)
    ax.set_title("Mean TF-IDF weight by term and ticker (fixed headline set)")
    fig.colorbar(im, ax=ax, label="TF-IDF weight")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT} ({len(terms)} terms x {len(tickers)} tickers)")


if __name__ == "__main__":
    main()
