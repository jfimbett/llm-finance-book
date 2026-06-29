#!/usr/bin/env python3
"""
Generate the word-analogy figure for ch01 of the LLM Finance book:
the classic  king - man + woman  ~=  queen,  using REAL pre-trained GloVe
vectors (glove-wiki-gigaword-300), projected to 2D with PCA.

Loaded locally via gensim's download cache; no API key required.
Run inside the project env:  conda run -n llm-finance python gen_king_analogy.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIGURES_DIR = REPO_ROOT / "book" / "chapters" / "01-intro" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "glove-wiki-gigaword-300"


def unit(v):
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(np.dot(unit(a), unit(b)))


def main():
    import gensim.downloader as api

    print(f"Loading {MODEL_NAME} (downloads & caches on first run)…", flush=True)
    kv = api.load(MODEL_NAME)

    king, man, woman, queen = (unit(kv["king"]), unit(kv["man"]),
                               unit(kv["woman"]), unit(kv["queen"]))
    result = king - man + woman

    nearest = kv.most_similar(positive=["king", "woman"], negative=["man"], topn=3)
    print("king - man + woman ≈", nearest, flush=True)

    labels = ["king", "queen", "man", "woman", "king - man\n+ woman"]
    xy = PCA(n_components=2, random_state=0).fit_transform(
        np.vstack([king, queen, man, woman, result]))
    p_king, p_queen, p_man, p_woman, p_res = xy

    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    styles = [("#1f77b4", "o", 150), ("#d62728", "o", 150),
              ("#2ca02c", "s", 130), ("#9467bd", "s", 130),
              ("#ff7f0e", "*", 420)]
    for (x, y), lab, (c, m, s) in zip(xy, labels, styles):
        ax.scatter(x, y, c=c, marker=m, s=s, zorder=4,
                   edgecolors="black", linewidths=0.7)

    # The arithmetic: arrow from king to the computed result.
    ax.annotate("", xy=p_res, xytext=p_king,
                arrowprops=dict(arrowstyle="-|>", color="#ff7f0e", lw=2.2), zorder=3)
    # The result lands next to queen.
    ax.plot([p_res[0], p_queen[0]], [p_res[1], p_queen[1]], ":", color="black",
            lw=1.6, zorder=3)

    offsets = {"king": (9, 6), "queen": (9, 6), "man": (9, 6),
               "woman": (9, 6), "king - man\n+ woman": (10, -24)}
    for (x, y), lab in zip(xy, labels):
        dx, dy = offsets[lab]
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(dx, dy),
                    fontsize=11,
                    fontweight="bold" if lab.startswith("king -") else "normal")

    box = ("nearest words to king - man + woman:\n"
           + "\n".join(f"  {w:<9}{s:.2f}" for w, s in nearest))
    ax.text(0.46, 0.04, box, transform=ax.transAxes, fontsize=9,
            va="bottom", ha="left", family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="grey", lw=0.7))

    ax.axhline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.axvline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.set_xlabel("PC 1", fontsize=11)
    ax.set_ylabel("PC 2", fontsize=11)
    ax.set_title(r"Word analogy in GloVe (300d): "
                 r"$king - man + woman \approx queen$", fontsize=12)
    ax.margins(0.20)
    fig.tight_layout()

    out = FIGURES_DIR / "fig_king_analogy"
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.with_suffix('.pdf')}  (cos to queen = {cos(result, queen):.3f})",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
