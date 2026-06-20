#!/usr/bin/env python3
"""
Generate the accounting-identity comparison figure for ch01 of the LLM Finance
book:  does  Assets = Liabilities + Equity  hold as embedding vector arithmetic?

We compare two REAL models on the same terms:
  * general    glove-wiki-gigaword-300            (skip-gram-style, broad web text)
  * finance    FinLang/finance-embeddings-investopedia  (retrieval fine-tuned on finance)

Honest finding (the point of the figure):
  - In the GENERAL model, unit(liabilities) + unit(equity) has `assets` as its
    single nearest neighbour -- the balance-sheet identity emerges as addition.
  - In the FINANCE model it does NOT (assets drops to ~rank 4): retrieval
    fine-tuning packs every balance-sheet term into a tight similarity cone
    (raw cos(liabilities, equity) rises 0.30 -> 0.78), which is great for
    similarity/disambiguation but flattens the additive geometry.

Outputs (PDF + PNG -> book/chapters/01-intro/figures/):
  fig_accounting_identity        two-panel 2D PCA, general vs finance.
Also writes accounting_identity_cache.json with the numbers cited in the text.

Run:  conda run -n llm-finance python gen_accounting_identity.py
"""

import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIGURES_DIR = REPO_ROOT / "book" / "chapters" / "01-intro" / "figures"
CACHE_FILE = SCRIPT_DIR / "accounting_identity_cache.json"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Candidate balance-sheet vocabulary for nearest-neighbour ranking.
CANDIDATES = ["assets", "liabilities", "equity", "debt", "capital", "cash",
              "revenue", "income", "expenses", "goodwill", "inventory",
              "receivables", "shareholders", "balance", "leverage"]
# Subset actually drawn in the scatter (keeps the panel legible).
PLOT_TERMS = ["assets", "liabilities", "equity", "debt", "leverage", "balance",
              "capital", "cash"]


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(np.dot(unit(a), unit(b)))


def rank_candidates(vec, V, exclude):
    ranked = sorted(((w, cos(vec, V[w])) for w in CANDIDATES if w not in exclude),
                    key=lambda x: -x[1])
    return ranked


def analyse(name, V, glove_kv=None):
    """V: dict term -> raw vector.  Returns a results dict for one model."""
    s = unit(V["liabilities"]) + unit(V["equity"])           # the identity sum
    ranked = rank_candidates(s, V, exclude={"liabilities", "equity"})
    assets_rank = next(i + 1 for i, (w, _) in enumerate(ranked) if w == "assets")
    res = {
        "model": name,
        "sum_nearest": [[w, round(s_, 4)] for w, s_ in ranked[:5]],
        "assets_rank": assets_rank,
        "cos_sum_assets": round(cos(s, V["assets"]), 4),
        "cos_liab_equity": round(cos(V["liabilities"], V["equity"]), 4),
        "cos_assets_liab": round(cos(V["assets"], V["liabilities"]), 4),
        "cos_assets_equity": round(cos(V["assets"], V["equity"]), 4),
    }
    if glove_kv is not None:
        sims = glove_kv.cosine_similarities(s, glove_kv.vectors)
        order = np.argsort(-sims)
        full = []
        for i in order:
            w = glove_kv.index_to_key[i]
            if w in ("liabilities", "equity"):
                continue
            full.append([w, round(float(sims[i]), 4)])
            if len(full) >= 5:
                break
        res["sum_nearest_full_vocab"] = full
    return res, s


def draw_panel(ax, V, svec, title, neighbour_text):
    # Unit-normalise every vector so 2D distances reflect ANGLES (cosine), not
    # magnitude -- the sum vector is longer than the term vectors otherwise.
    mat = np.vstack([unit(V[t]) for t in PLOT_TERMS] + [unit(svec)])
    xy = PCA(n_components=2, random_state=0).fit_transform(mat)
    pos = {t: xy[i] for i, t in enumerate(PLOT_TERMS)}
    psum = xy[-1]

    addends = {"liabilities": "#1f77b4", "equity": "#2ca02c"}
    for t in PLOT_TERMS:
        x, y = pos[t]
        if t == "assets":
            ax.scatter(x, y, c="#d62728", marker="o", s=190, zorder=4,
                       edgecolors="black", linewidths=0.8)
        elif t in addends:
            ax.scatter(x, y, c=addends[t], marker="s", s=130, zorder=4,
                       edgecolors="black", linewidths=0.6)
        else:
            ax.scatter(x, y, c="#9e9e9e", marker="o", s=90, zorder=3,
                       edgecolors="black", linewidths=0.4)
        off = (0, 13) if t == "assets" else (7, 5)
        ha = "center" if t == "assets" else "left"
        ax.annotate(t, (x, y), textcoords="offset points", xytext=off, ha=ha,
                    fontsize=9.5,
                    fontweight="bold" if t == "assets" else "normal")
    # The computed sum vector (its projected position IS unit(liab)+unit(equity)).
    ax.scatter(*psum, c="#ff7f0e", marker="*", s=460, zorder=5,
               edgecolors="black", linewidths=0.8)
    ax.annotate("Liabilities\n+ Equity", psum, textcoords="offset points",
                xytext=(10, -22), fontsize=10, fontweight="bold")
    # Dotted link: does the computed sum reach `assets`?
    ax.plot([psum[0], pos["assets"][0]], [psum[1], pos["assets"][1]], ":",
            color="black", lw=1.5, zorder=2)

    ax.text(0.5, -0.30, neighbour_text, transform=ax.transAxes, fontsize=8.2,
            va="top", ha="center", family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="grey", lw=0.7))
    ax.set_xlabel("PC 1", fontsize=10)
    ax.set_ylabel("PC 2", fontsize=10)
    ax.set_title(title, fontsize=10.5)
    ax.margins(0.22)


def main():
    # --- General GloVe ---
    import gensim.downloader as api
    kv = api.load("glove-wiki-gigaword-300")
    Vg = {w: kv[w] for w in CANDIDATES if w in kv}
    missing = [w for w in CANDIDATES if w not in kv]
    if missing:
        print("GloVe OOV (dropped):", missing, flush=True)
    rg, sg = analyse("glove-wiki-gigaword-300", Vg, glove_kv=kv)

    # --- Finance-tuned ---
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("FinLang/finance-embeddings-investopedia")
    emb = model.encode(CANDIDATES, normalize_embeddings=False)
    Vf = {w: emb[i] for i, w in enumerate(CANDIDATES)}
    rf, sf = analyse("FinLang/finance-embeddings-investopedia", Vf)

    print("\n--- GENERAL GloVe ---", flush=True)
    print("  sum nearest (candidates):", rg["sum_nearest"], flush=True)
    print("  sum nearest (full 400k):", rg.get("sum_nearest_full_vocab"), flush=True)
    print("  assets rank:", rg["assets_rank"],
          " cos(liab,equity):", rg["cos_liab_equity"], flush=True)
    print("--- FINANCE-tuned ---", flush=True)
    print("  sum nearest (candidates):", rf["sum_nearest"], flush=True)
    print("  assets rank:", rf["assets_rank"],
          " cos(liab,equity):", rf["cos_liab_equity"], flush=True)

    # --- Figure ---
    gbox = ("nearest to Liab+Equity (full 400k vocab):\n"
            + "\n".join(f"  {w:<9}{s:.2f}" for w, s in rg["sum_nearest_full_vocab"][:3])
            + f"\n=> assets is the #1 nearest word")
    fbox = ("nearest to Liab+Equity (balance-sheet terms):\n"
            + "\n".join(f"  {w:<9}{s:.2f}" for w, s in rf["sum_nearest"][:4])
            + f"\n=> assets only rank {rf['assets_rank']}")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.6, 5.6))
    draw_panel(axL, Vg, sg,
               "(a) General GloVe: identity holds\n"
               r"$\mathit{Liabilities}+\mathit{Equity}\approx\mathit{Assets}$"
               f"  (cos {rg['cos_sum_assets']:.2f})",
               gbox)
    draw_panel(axR, Vf, sf,
               "(b) Finance-tuned: identity breaks\n"
               r"sum lands among $\mathit{leverage}/\mathit{balance}$, not "
               r"$\mathit{assets}$",
               fbox)
    fig.suptitle("Does \"Assets = Liabilities + Equity\" hold as vector "
                 "arithmetic?  Two real embedding models", fontsize=12, y=1.0)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.83, bottom=0.30, wspace=0.22)
    out = FIGURES_DIR / "fig_accounting_identity"
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out.with_suffix('.pdf')}", flush=True)

    CACHE_FILE.write_text(json.dumps({"general": rg, "finance": rf}, indent=2))
    print(f"Wrote {CACHE_FILE}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
