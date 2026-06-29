# Constructive Review — Chapter 2 (reading order) · 16-ai-ml-finance-text

Audit only. File: `book/chapters/16-ai-ml-finance-text/chapter.tex`.

This chapter is a strong, well-written conceptual on-ramp. It reads cleanly, is
finance-first, and defines its key terms locally before use. Below is what to KEEP.

## Genuinely strong content

- **`chapter.tex:4-21` — Learning Objectives (KEEP / GOOD_BIG_PICTURE_EXPLANATION).**
  Six concrete, verb-led objectives that map exactly onto the section structure.
  Lines 20-21 helpfully forward-point to where token/vocabulary/attention are
  defined *within this chapter*, pre-empting use-before-definition concerns.

- **`chapter.tex:38-49` — expert-systems history (KEEP / GOOD_BIG_PICTURE_EXPLANATION).**
  Crisp, accurate account of the symbolic-to-statistical shift, anchored in a
  finance example (loan-risk if-then rules). No overclaiming.

- **`chapter.tex:62-75` — Remark "The shifting definition of AI" (KEEP).**
  The AI-effect framing is correct and the remark closes by pinning down the
  working definitions used in the book, with a forward pointer to the formal
  definitions below (line 74).

- **`chapter.tex:89-103` — Definitions of Symbolic AI / Statistical AI (KEEP_AS_SINGLE_SOURCE_OF_TRUTH).**
  Clean, parallel definitions. This is the natural SSOT for the symbolic vs.
  statistical distinction for the whole book.

- **`chapter.tex:137-146` — Definition of Supervised Learning (KEEP_AS_SINGLE_SOURCE_OF_TRUTH / GOOD_TECHNICAL_EXPLANATION).**
  Notation is fully introduced (input/output spaces, parameters, per-sample loss)
  before the empirical-risk expression; math is re-derivable. Strong candidate to
  be cited (`\Cref{def:supervised-learning}`) from later ML chapters rather than
  re-derived.

- **`chapter.tex:186-197` — `context` box (markets ↔ deep nets) (KEEP / GOOD_BIG_PICTURE_EXPLANATION).**
  Exactly the right use of a `context` box: an interpretive analogy that enriches
  without blocking the technical thread.

- **`chapter.tex:208-223` — Definition of Large Language Model (KEEP_AS_SINGLE_SOURCE_OF_TRUTH / GOOD_TECHNICAL_EXPLANATION).**
  Defines token and vocabulary inline, then gives the next-token NLL objective.
  Correct and re-derivable. Good SSOT for the LM objective at book scope; later
  chapters should `\Cref` this rather than restate it.

- **`chapter.tex:413-418, 440-450` — Loughran–McDonald framing + EPS-beat example (GOOD_FINANCE_EXAMPLE / KEEP).**
  The "EPS beats but Risk Factors grew 30%, 'challenging' used 11 times" example
  (440-450) is realistic, integrated, and motivates the whole text-signal thesis.
  Reader can act on it (it mirrors the EDGAR exercises in the paired notebook).

- **`chapter.tex:572-592` — `deepdive` box: scaled dot-product attention (KEEP / GOOD_TECHNICAL_EXPLANATION).**
  Correctly states the attention formula, defines softmax inline, explains the
  $\sqrt{d_k}$ scaling, and is honest about the single-head $d_v=d_k$ simplification
  (582-584). Defers the full derivation to Chapter 2 — correct concept_separation.

- **`chapter.tex:646-659` — Remark "LLMs are not a panacea" (KEEP / GOOD_BIG_PICTURE_EXPLANATION).**
  Balanced caveat list (hallucination, prompt sensitivity, opacity, tail
  calibration). Good completeness signal; forward-points to Chapter 13.

- **Concept separation overall (KEEP).** The chapter uses `context` for the bigger
  picture (186, 491), `deepdive` for internals (572), `definition`/`example`/
  `remark` consistently. Either layer can be read alone.

## Notebook (paired)

- **`code/notebooks/16-ai-ml-finance-text/exercises.ipynb` (GOOD_FINANCE_EXAMPLE / KEEP).**
  Real, runnable EDGAR pipeline: live CIK lookup, MD&A extraction, LM-style
  uncertainty/negative word lists, Gunning Fog readability, and a 6-feature
  text+ratio return predictor with LOO-CV. Honest overfitting caveat
  (`"n=10 -- interpret with extreme caution"`). This is not a stub.
