#!/usr/bin/env python3
"""
Generate embedding-arithmetic figures for ch01 of the LLM Finance book.

Uses REAL pre-trained GloVe vectors (glove-wiki-gigaword-300, loaded locally via
gensim's download cache -- no API key) to test, honestly, the word-analogy idea

    vec(a) - vec(b) + vec(c)  ?=  vec(d)

for two cases:
  * the classic   king - man + woman  ~= queen      (works cleanly)
  * the financial call option - upside + downside  ?= put option

The financial case is reported faithfully: general-purpose GloVe does NOT encode
this as a clean linear analogy (the polysemous senses of call/put/option dominate),
which is itself the pedagogical point and motivates finance-specific embeddings.

Figures produced (PDF + PNG, written to book/chapters/01-intro/figures/):
  1. fig_embedding_analogy        -- two-panel 2D PCA: king case vs. finance case.
  2. fig_embedding_pca_vocab      -- 2D PCA scatter of 30 financial terms by group.

Run inside the project env:
    conda run -n llm-finance python gen_embedding_analogy.py
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

print("Script started", flush=True)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIGURES_DIR = REPO_ROOT / "book" / "chapters" / "01-intro" / "figures"
CACHE_FILE = SCRIPT_DIR / "embedding_analogy_cache.json"
MODEL_NAME = "glove-wiki-gigaword-300"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_model():
    import gensim.downloader as api

    print(f"Loading {MODEL_NAME} (downloads & caches on first run)…", flush=True)
    kv = api.load(MODEL_NAME)
    print(f"  vocab size: {len(kv.index_to_key):,}  dim: {kv.vector_size}", flush=True)
    return kv


def unit(v):
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(np.dot(unit(a), unit(b)))


def phrase_vec(kv, phrase):
    """Embed a (possibly multi-word) phrase as the mean of its in-vocab tokens."""
    toks = [t for t in phrase.lower().split() if t in kv]
    if not toks:
        raise KeyError(f"no in-vocab tokens for phrase {phrase!r}")
    return np.mean([kv[t] for t in toks], axis=0)


def full_vocab_neighbours(kv, target, topn=10, exclude=()):
    """Nearest words in the WHOLE vocabulary to a target vector (honest ranking)."""
    sims = kv.cosine_similarities(target, kv.vectors)
    order = np.argsort(-sims)
    out, ex = [], {e.lower() for e in exclude}
    for i in order:
        w = kv.index_to_key[i]
        if w in ex:
            continue
        out.append((w, float(sims[i])))
        if len(out) >= topn:
            break
    return out


def draw_analogy_panel(ax, vecs, labels, src_idx, tgt_idx, result_idx, title,
                       neighbour_text):
    """PCA the given vectors to 2D and draw the analogy arithmetic on `ax`."""
    pca = PCA(n_components=2, random_state=0)
    xy = pca.fit_transform(np.vstack(vecs))
    evr = pca.explained_variance_ratio_

    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]
    markers = ["o", "o", "s", "s", "*"]
    for i, ((x, y), lab) in enumerate(zip(xy, labels)):
        size = 360 if markers[i] == "*" else 130
        ax.scatter(x, y, c=colors[i], marker=markers[i], s=size, zorder=3,
                   edgecolors="black", linewidths=0.6)
        dy = -16 if i == 3 else 7
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(8, dy),
                    fontsize=9.5,
                    fontweight="bold" if i == result_idx else "normal")

    # Orange arrow: the full arithmetic, from source term to the result point.
    ax.annotate("", xy=xy[result_idx], xytext=xy[src_idx],
                arrowprops=dict(arrowstyle="-|>", color="#ff7f0e", lw=2.0), zorder=2)
    # Dotted black link from result to the intended target word.
    ax.plot([xy[result_idx, 0], xy[tgt_idx, 0]],
            [xy[result_idx, 1], xy[tgt_idx, 1]], ":", color="black", lw=1.3, zorder=1)

    # Honest nearest-neighbour box (placed BELOW the axes, clear of the points):
    # what the result vector is ACTUALLY closest to.
    ax.text(0.5, -0.30, neighbour_text, transform=ax.transAxes, fontsize=8.2,
            va="top", ha="center", family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="grey", lw=0.7))

    ax.axhline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.axvline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.set_xlabel(f"PC 1  ({evr[0]*100:.0f}%)", fontsize=10)
    ax.set_ylabel(f"PC 2  ({evr[1]*100:.0f}%)", fontsize=10)
    ax.set_title(title, fontsize=10.5)
    ax.margins(0.22)


def main():
    kv = load_model()
    results = {"model": MODEL_NAME, "dim": int(kv.vector_size)}

    # ── Case 1: classic analogy (validates the method) ───────────────────────
    k, m, w, q = (unit(kv["king"]), unit(kv["man"]),
                  unit(kv["woman"]), unit(kv["queen"]))
    r1 = k - m + w
    king_para = cos(kv["king"] - kv["queen"], kv["man"] - kv["woman"])
    king_top = full_vocab_neighbours(kv, r1, topn=5, exclude=("king", "man", "woman"))
    print("\n[1] king - man + woman ≈ ?", flush=True)
    for x, s in king_top:
        print(f"    {x:<12} {s:.3f}", flush=True)
    print(f"    parallelogram cos(king-queen, man-woman) = {king_para:.3f}", flush=True)
    results.update(
        king_neighbours=[[x, round(s, 4)] for x, s in king_top],
        king_parallelogram=round(king_para, 4),
        cos_king_result_queen=round(cos(r1, q), 4),
    )

    # ── Case 2: financial analogy (reported honestly) ────────────────────────
    call = unit(phrase_vec(kv, "call option"))
    put = unit(phrase_vec(kv, "put option"))
    up = unit(phrase_vec(kv, "upside"))
    down = unit(phrase_vec(kv, "downside"))
    r2 = call - up + down
    fin_para = cos(phrase_vec(kv, "call option") - phrase_vec(kv, "put option"),
                   phrase_vec(kv, "upside") - phrase_vec(kv, "downside"))
    fin_full = full_vocab_neighbours(
        kv, r2, topn=10, exclude=("call", "put", "option", "upside", "downside"))
    # Restricted finance shortlist (best case for the analogy).
    shortlist = ["put option", "warrant", "futures", "forward", "swap", "hedge",
                 "derivative", "premium", "strike", "volatility", "collateral", "bond"]
    fin_short = sorted(((c, cos(r2, phrase_vec(kv, c))) for c in shortlist),
                       key=lambda x: -x[1])[:6]
    print("\n[2] call option - upside + downside ≈ ?", flush=True)
    print("    full-vocab nearest:", flush=True)
    for x, s in fin_full[:6]:
        print(f"      {x:<12} {s:.3f}", flush=True)
    print("    finance shortlist nearest:", flush=True)
    for x, s in fin_short:
        tag = "  <-- 'put option'" if x == "put option" else ""
        print(f"      {x:<12} {s:.3f}{tag}", flush=True)
    print(f"    cos(result, put option) = {cos(r2, put):.3f}", flush=True)
    print(f"    cos(result, call option)= {cos(r2, call):.3f}  (source bleed-through)",
          flush=True)
    print(f"    parallelogram cos(call-put, upside-downside) = {fin_para:.3f}",
          flush=True)
    results.update(
        fin_full_vocab=[[x, round(s, 4)] for x, s in fin_full],
        fin_shortlist=[[x, round(s, 4)] for x, s in fin_short],
        cos_result_put_option=round(cos(r2, put), 4),
        cos_result_call_option=round(cos(r2, call), 4),
        fin_parallelogram=round(fin_para, 4),
    )

    # ── Figure 1: two-panel comparison ───────────────────────────────────────
    king_box = ("nearest words to result:\n"
                + "\n".join(f"  {x:<9}{s:.2f}" for x, s in king_top[:3])
                + f"\nparallelogram cos = {king_para:+.2f}")
    fin_box = ("nearest words to result:\n"
               + "\n".join(f"  {x:<9}{s:.2f}" for x, s in fin_full[:3])
               + f"\n'put option' = {cos(r2, put):.2f} (shortlist only)"
               + f"\nparallelogram cos = {fin_para:+.2f}")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.6, 5.1))
    draw_analogy_panel(
        axL,
        [k, q, m, w, r1],
        ["king", "queen", "man", "woman", "king - man\n+ woman"],
        src_idx=0, tgt_idx=1, result_idx=4,
        title=("(a) Classic analogy holds: nearest word is "
               r"$\mathit{queen}$" + "\n"
               rf"$king-man+woman\approx queen$  (cos $={cos(r1, q):.2f}$)"),
        neighbour_text=king_box,
    )
    draw_analogy_panel(
        axR,
        [call, put, up, down, r2],
        ["call option", "put option", "upside", "downside",
         "call opt. - upside\n+ downside"],
        src_idx=0, tgt_idx=1, result_idx=4,
        title=("(b) Finance analogy fails: nearest words are generic\n"
               r"$call-upside+downside$ does not give $put$ in GloVe"),
        neighbour_text=fin_box,
    )
    fig.suptitle("Word-vector arithmetic in pre-trained GloVe (300d), "
                 "projected to 2D by PCA", fontsize=12, y=1.0)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.83, bottom=0.30, wspace=0.22)
    out1 = FIGURES_DIR / "fig_embedding_analogy"
    fig.savefig(out1.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out1.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out1.with_suffix('.pdf')}", flush=True)

    # ── Figure 2: 30-term financial vocabulary PCA scatter ───────────────────
    vocab_groups = {
        "Rates & macro": ["yield", "spread", "inflation", "central bank",
                          "interest rate"],
        "Equities & returns": ["equity", "dividend", "earnings", "revenue",
                              "profit", "loss", "alpha", "beta", "factor",
                              "return", "sentiment"],
        "Risk concepts": ["volatility", "risk", "default", "credit", "liquidity",
                         "leverage", "portfolio", "hedge"],
        "Corp. actions & derivatives": ["option", "futures", "derivative",
                                      "merger", "acquisition"],
    }
    terms, term_group, vecs = [], [], []
    for g, ws in vocab_groups.items():
        for token in ws:
            try:
                vecs.append(phrase_vec(kv, token))
                terms.append(token)
                term_group.append(g)
            except KeyError:
                print(f"  skip OOV term: {token}", flush=True)
    V = np.vstack(vecs)
    V = V - V.mean(axis=0, keepdims=True)
    pca2 = PCA(n_components=2, random_state=0)
    xy2 = pca2.fit_transform(V)
    evr2 = pca2.explained_variance_ratio_

    palette = {
        "Rates & macro": "#1f77b4",
        "Equities & returns": "#2ca02c",
        "Risk concepts": "#d62728",
        "Corp. actions & derivatives": "#ff7f0e",
    }
    fig2, ax2 = plt.subplots(figsize=(7.4, 5.6))
    for g in vocab_groups:
        idx = [i for i, tg in enumerate(term_group) if tg == g]
        ax2.scatter(xy2[idx, 0], xy2[idx, 1], c=palette[g], s=90, label=g,
                    edgecolors="black", linewidths=0.4, zorder=3)
    for (x, y), t in zip(xy2, terms):
        ax2.annotate(t, (x, y), textcoords="offset points", xytext=(5, 3),
                     fontsize=8.5)
    ax2.set_xlabel(f"PC 1  ({evr2[0]*100:.0f}% var.)", fontsize=11)
    ax2.set_ylabel(f"PC 2  ({evr2[1]*100:.0f}% var.)", fontsize=11)
    ax2.set_title("PCA of 30 financial terms (GloVe 300d), coloured by group",
                  fontsize=11)
    ax2.legend(fontsize=8.5, loc="best", framealpha=0.9)
    fig2.tight_layout()
    out2 = FIGURES_DIR / "fig_embedding_pca_vocab"
    fig2.savefig(out2.with_suffix(".pdf"), bbox_inches="tight")
    fig2.savefig(out2.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig2)
    print(f"Wrote {out2.with_suffix('.pdf')}", flush=True)
    results["explained_var_vocab"] = [round(float(e), 4) for e in evr2]

    CACHE_FILE.write_text(json.dumps(results, indent=2))
    print(f"Wrote {CACHE_FILE}", flush=True)
    print("\nDone.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
