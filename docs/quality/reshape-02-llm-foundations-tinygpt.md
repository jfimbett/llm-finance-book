# Reshape Report: 02-llm-foundations — Tiny-GPT numerical walk-through

## User Request

> For the transformers architecture it would be good to show, in a sequence of
> matrices, a tiny example (small vocabulary and embedding dimension) in which a
> text is transformed into embeddings, positional encodings, then matrices,
> neural networks (a picture of a neural network), etc., all the way to the end.
> Start with a decoder like GPT; user will review.

## Main Changes Applied

- **Added §3.3.5 "A Numerical Walk-Through: One Forward Pass of a Tiny GPT"**
  (`sec:transformer-walkthrough`), a complete numeric trace of a decoder-only
  (GPT-style) forward pass, inserted as the capstone of the Transformer
  Architecture section (after Encoder–Decoder Structure, before Pre-training).
- The trace runs the prefix `<s> revenue fell` end to end, matrix by matrix:
  1. tokenise + embedding lookup (`E`, 6×4);
  2. sinusoidal positional encoding → block input `X⁽⁰⁾`;
  3. Q/K/V projections (with `W^Q=W^K=I` so scores are token similarities);
  4. scaled scores, **causal mask**, softmax → attention weights `A`;
  5. attention output `A V`, residual + LayerNorm → `Z`;
  6. position-wise FFN (widen → ReLU → project), residual + LayerNorm → `X⁽¹⁾`;
  7. tied un-embedding `X⁽¹⁾Eᵀ` → logits → softmax → next-token distribution.
- **Added Figure 3.2** (`fig:ch02-tinygpt-ffn`): a TikZ "picture of a neural
  network" for the FFN sub-layer (4→6→4, ReLU), with the two hidden units that
  ReLU clips to zero drawn in grey — a concrete instance of ReLU sparsity.
- The model predicts **`sharply`** (probability 0.66), completing "revenue fell
  sharply" and tying back to the running phrase in Figure 3.1.
- **Added a closing remark** (`rem:tinygpt-scale`) on what separates the toy from
  a real GPT: depth/width (stacked blocks, multiple heads), training via the CLM
  loss, and the parallel teacher-forced scoring the RNNs of §3.2 could not exploit.
- **Configuration remark** (`rem:tinygpt-config`) states all dimensions and the
  three deliberate simplifications (hand-picked illustrative weights, `W^Q=W^K=I`,
  reduced `d_ff`).

## Sections Modified

- §3.3 The Transformer Architecture — new subsection 3.3.5 (the worked example)
  and new Figure 3.2. Positional-encoding illustration auto-renumbered to Fig 3.3.

## New References Added

- None.

## Math Checker

VERIFIED NUMERICALLY (not the agent). Every matrix in the walk-through was
produced by a numpy script that implements the exact forward pass (embeddings,
sinusoidal PE, single-head causal attention, post-LayerNorm, ReLU FFN, tied
un-embedding, softmax). The printed values are transcriptions of that script's
output rounded to two decimals; spot-checks (X⁽⁰⁾, A, logits, P) match. No
existing definitions, propositions, or proofs were altered.

## Score Summary

Not re-scored via `/score-content` in this pass.

## Build / Reference Checks

- Full book builds: `main.pdf`, no LaTeX errors.
- No duplicate or undefined labels/citations introduced.
- Cross-references resolve; figures renumber automatically (3.1 architecture,
  3.2 tiny-GPT FFN, 3.3 positional-encoding illustration).
- One residual 4.5pt overfull hbox on the masked-softmax line (cosmetic, on par
  with existing book equations).
- Rendered pages inspected visually (print pp. 75–79): every matrix fits the text
  width; the FFN figure and final distribution display correctly.

## Open Questions for the User (review)

- **Predicted token chosen for narrative.** Weights are hand-picked so the toy
  predicts `sharply`. If you'd prefer the example be visibly "untrained" (an
  arbitrary winner) or predict a different continuation, say so.
- **LayerNorm shown as a labelled step** (γ=1, β=0) rather than with its own
  mean/variance arithmetic, to keep the trace legible. Can expand if wanted.
- **Single head / single block.** Multi-head and stacking are described in the
  closing remark but not traced numerically. Can add a two-head variant if useful.

## Remaining Issues

- None blocking.

---

## Revision Round 2 (user review feedback)

User feedback: (1) references not compiling; (2) one-hot encoding of tokens not
shown; (3) `<s>` unexplained — add a special-tokens section; (4) highlight
rows/columns to show movement between matrices.

### Changes

- **References fixed.** Root cause was a **corrupt biber cache** (an environment
  issue, not the chapter or `.bib`, which is git-clean): biber crashed silently
  mid-parse, leaving a 0-byte `main.bbl`, and `set -e` in `build-book.sh` aborted
  the remaining pdflatex passes, so every citation rendered undefined. Fixed by
  `rm -rf "$(biber --cache)"`. Build now resolves 0 undefined citations/refs.
- **One-hot lookup shown.** Step 1 now presents embedding lookup as the explicit
  matrix product `O E = X^{(emb)}`, with `O` the 3x6 one-hot matrix, tying back to
  Proposition `thm:mean-embed-is-bow`.
- **Special Tokens subsection added** (§3.3.5, `sec:special-tokens`): `<s>/<bos>`,
  `</s>/<eos>`, `[CLS]`, `[SEP]`, `[MASK]`, `<pad>`, `<unk>`, with finance framing.
  The walk-through is now §3.3.6.
- **Row/column highlighting** via `colortbl` (added to preamble). A blue band
  follows the `fell` query row (position 3) from the one-hot through `O E`,
  `X^{(0)}`, `A`, `Att`, `Z`, `X^{(1)}`; an orange column marks the `sharply`
  logit, with the winning cell bold + darker. `colortbl` was chosen over
  `nicematrix` because it shades during table construction in a **single pass** —
  `nicematrix` color panels need 3+ passes to converge and render as giant blocks
  under the book's fixed-pass build.

### Build / checks (round 2)

- Full book builds clean (exit 0), 0 undefined citations/references.
- Figures still 3.1 / 3.2 / 3.3; no hardcoded figure numbers.
- One residual ~11pt overfull on the masked-softmax chain line (cosmetic).
- Rendered pages inspected (print pp. 76–81): one-hot product, blue thread,
  orange logits column + bold winning cell, and Special Tokens all display
  correctly.

### Open question for the user

- The highlight thread follows the `fell` row and the `sharply` column. If you'd
  prefer a different colour scheme, or highlighting at fewer/more transitions,
  say so.
