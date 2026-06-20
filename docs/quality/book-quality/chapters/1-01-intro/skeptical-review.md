# Skeptical Review — 1 (reading index) · 01-intro · "Introduction"

Reading order: `01 → 16 → 02 → 03 → 08 → 04 → 09 → 14 → 05 → 06 → 10 → 11 → 12 → 13 → 07 → 15`.
This is the **first** chapter read. Anything it "defines later" or "covers in another chapter"
is judged against that order. All citation keys used in the chapter resolve in the active
`bibliography.bib` (verified). Build not run here; label-collision findings are from static scan.

---

## Issues (ranked)

### BLOCKER

[BLOCKER · notation_crossref · book-repetition] `book/chapters/01-intro/chapter.tex` §LSTM/Multi-Head + `book/chapters/02-llm-foundations/chapter.tex` — **Nine duplicate `\label{}` keys shared with ch02.** Verified collisions: `def:lstm` (ch01:1584 / ch02:455), `eq:lstm-forget` (1587/460), `eq:lstm-input` (1589/462), `eq:lstm-candidate` (1591/464), `eq:lstm-cell` (1593/466), `eq:lstm-output` (1595/468), `eq:lstm-hidden` (1597/469), `eq:multihead` (1710/854), `eq:rnn-jacobian` (1532/402). Plus `def:mlm` is duplicated in ch01:1786 and ch03:389. With biblatex/hyperref, duplicate labels emit "multiply defined" warnings and every `\ref`/`\eqref` to these keys resolves to the *last-defined* instance (ch02/ch03), so any in-ch01 reference silently points into another chapter. Rubric §2 lists "no known duplicate labels" as a book-pass condition.
  Fix: Rename all ch01 instances with a chapter prefix (e.g. `def:lstm-ch01`, `eq:lstm-cell-ch01`, `eq:multihead-ch01`, `eq:rnn-jacobian-ch01`, `def:mlm-ch01`) and update the in-chapter `\ref`s, OR — preferred, see the non_repetition BLOCKER — delete ch01's re-derivations so ch02/ch03 remain the single source of truth and the labels live in exactly one place.

[BLOCKER · non_repetition · book-repetition] `chapter.tex:1473–1736` (RNN/vanishing-gradient §, LSTM cell, scaled dot-product attention + √d_k proof, multi-head attention) vs `02-llm-foundations/chapter.tex:341–880`. ch02 owns: vanilla-RNN recurrence (`def:rnn`), the vanishing/exploding-gradient theorem (`thm:vanish-explode`, `eq:vanish-bound`), the LSTM cell (`def:lstm`), scaled dot-product attention (`def:scaled-dot-product-attn`, `eq:scaled-dot-product`), the √d_k scaling theorem (`thm:sqrt-dk-scaling`), and multi-head attention (`eq:multihead`). ch01 re-derives every one of these *from scratch* with near-identical equations and its own duplicate proof of the √d_k result (`prop:sqrt-dk`, 1662–1685) — not a cross-reference. Rubric `non_repetition` ≥90 requires "overlap is intentional and cross-referenced … not re-derived; one designated single source of truth per concept." This is verbatim-level re-derivation of four concepts ch02 owns.
  Fix: Demote ch01's §6 (RNN/LSTM) and §7 (attention/Transformer) to short intuition-only `context` boxes that *forward-reference* ch02 (`see \Cref{sec:transformer} for the derivation"), and delete the duplicated `theorem`/`proposition`/`definition` blocks and their proofs. Keep at most the one-sentence motivation ("vanishing gradient is why we needed attention"). This simultaneously removes the label collisions above.

### MAJOR

[MAJOR · citation_accuracy · citation] `chapter.tex:1726–1734` (`rem:attention-finance`). The remark says \citet{ke2019predicting} "applied **attention-based models** to financial news and found that the **attention weights** provide an interpretable signal … up-weights sentences containing forward-looking language." The resolved key `ke2019predicting` = Ke, Kelly & Xiu, *Predicting Returns with Text Data* (NBER WP 26186) — a **SESTM / screened-sentiment + topic-weighting** model, **not** an attention/Transformer model; it has no "attention weights." The same key is described *correctly* earlier (1320–1323) as "a supervised text-mining framework … sentiment-term screening … topic-model weighting." The 1728 description misattributes an attention mechanism to a non-attention paper.
  Fix: Replace the misdescription with a genuinely attention-based finance reference, or rewrite the remark to describe SESTM's interpretable screened-word weights (consistent with the 1320 description), or drop the remark.

[MAJOR · citation_accuracy · citation] `chapter.tex:2010–2011` — the inline `% [CITE: ...]` annotation for `\citet{didisheim2025memory}` reads "Didisheim, A., **Ke, Z., Kelly, B., & Vorsatz, B. (2024). Machines vs. Markets: The Power of Human-Aligned AI in Financial Forecasting**." The resolved bib entry is Didisheim, **Fraschini & Somoza (2025), "AI's Predictable Memory in Financial Analysis"** (SSRN 5331177). The annotation names different authors, a different title, and a different year than the key it documents — a stale/incorrect citation note that will mislead a fact-checker. (The prose claim about memorised asset returns does match the bib title, so the body text is OK.)
  Fix: Correct the `[CITE:]` comment at 2010–2011 to match the actual `didisheim2025memory` entry (Didisheim, Fraschini, Somoza, 2025).

[MAJOR · reproducibility · code-figure] `code/notebooks/01-intro/gen_edgar_text_growth.py:42` hard-codes a personal User-Agent — `{"User-Agent": "Finance Research jfimbett@gmail.com"}` — and lines 53–95, 141–151 perform **live SEC EDGAR HTTP fetches** at run time (random sample of 25 filings/year, `random.seed(42)` set but the *sampling pool* depends on whatever the live index returns). Figure~\ref{fig:edgar-text-growth} (chapter.tex:411–420) is therefore not deterministically regenerable by a third party: it depends on a cached `edgar_text_stats_cache.json`, a personal email in the request header, and SEC endpoint availability/rate-limits. Rubric `reproducibility` ≥90 requires "figures regenerable; deterministic or clearly documented." Neither the script nor the caption documents the dependence on the shipped cache, and the embedded email is a privacy/portability leak.
  Fix: Parameterise the User-Agent via an env var (`SEC_EDGAR_UA`) with a generic default; document in the caption/notebook that the figure is generated from the committed `edgar_text_stats_cache.json` and that live regeneration requires network access + a valid UA; state that the random sample is seed-fixed *given the cache*. Strip the personal email from the committed source.

[MAJOR · concept_ordering · local] `chapter.tex:576` (inside `def:textual-signal`) forward-references `Definition~\ref{def:corpus-vocab}` for the terms "documents/tokens/vocabulary," but `def:corpus-vocab` is not defined until line 680 (§Classical Text Representations), 104 lines later. The very first formal definition in the chapter depends on a not-yet-introduced definition. Rubric `concept_ordering` ≥90 = "every concept defined before first use in reading order; zero forward-dependency."
  Fix: Either move the corpus/vocabulary definition (`def:corpus-vocab`) ahead of `def:textual-signal`, or make `def:textual-signal` self-contained by inlining the one-line "documents are finite token sequences over a vocabulary $\mathcal{V}$" so no forward `\ref` is needed.

### MINOR

[MINOR · non_repetition · book-repetition] `chapter.tex` Tetlock (`tetlock2007giving`, lines 176/205/504/542) and Loughran–McDonald (`loughran2011liability`, 233/500/548) sentiment exemplars recur as primary worked examples in ch09 (`09-financial-nlp-sentiment`, 6 hits) and ch16 (`16-ai-ml-finance-text`, 4 hits). ch01 legitimately owns the *historical* framing, but the LM-dictionary mechanics and Tetlock's empirical findings are restated at depth in both later chapters without a designated single source of truth. Acceptable as motivation here, but flag for the editor to ensure ch09 is the one place the *method* is derived and ch01/ch16 cross-reference it rather than re-explaining the six tone categories.
  Fix: Keep ch01's narrative; add `\Cref{}` pointers ("the dictionary is treated in detail in the sentiment chapter") and ensure ch09 is the single source of truth for LM mechanics.

[MINOR · concept_ordering · local] `chapter.tex:1786` `def:mlm` (Masked Language Modelling) and the FinBERT/BERT exposition (350–362, 1801–1816) repeat material also defined in ch02 (`sec:transformer-pretrain`, `eq:mlm-loss`) and ch03 (`def:mlm`). As reading-index 1 the chapter is allowed to *introduce* MLM, but the full `\mathcal{L}_{\mathrm{MLM}}` objective is re-stated identically downstream — same single-source-of-truth concern as the BLOCKER, lower severity because it is a definition not a multi-equation derivation.
  Fix: Reduce ch01's MLM to a one-line intuition + forward reference to ch02/ch03; remove the duplicated `def:mlm` label (see BLOCKER fix).

[MINOR · correctness · local] `chapter.tex:402–409` claims "the mean word count of a 10-K filing roughly tripled between 1993 and 2023 \citep{loughran2020textual}." `loughran2020textual` is a 2020 Annual Review survey; a 2020 source cannot itself document a "1993–2023" trend ending in 2023. The magnitude ("tripled") is plausible and broadly supported in the LM literature, but the cited source's coverage window does not extend to 2023.
  Fix: Either soften to the window the survey actually covers, or add a source whose data run to 2023. Tag `NEEDS_EXTERNAL_VERIFICATION` for the exact "tripled, 1993–2023" magnitude.

### NIT

[NIT · correctness · local] `chapter.tex:1399, 1417` state the king−man+woman analogy nearest neighbour is *queen* at cosine **0.67** "ahead of *princess* and *throne*." For the standard `glove-wiki-gigaword-300` release the top hit (after excluding the three input words) is typically *queen* but reported similarities vary by normalisation; value is checkable from the shipped `gen_king_analogy.py`.
  Fix: Confirm 0.67 matches the committed script output; if so no change. Tag `NEEDS_EXTERNAL_VERIFICATION` only if the figure cannot be regenerated.

[NIT · citation_hygiene · citation] Three bib files coexist — `bibliography.bib` (active, per `preamble.tex:141`), `bibliography_test.bib`, `bibliography_bibertool.bib` — each defining the same keys. Not a ch01 defect per se (only the active file is loaded), but the stale duplicates are a book-level hygiene hazard if `\addbibresource` is ever switched.
  Fix: Remove or clearly mark the non-active `.bib` files; out of scope for ch01 surgery but worth a book-level note.

[NIT · notation_crossref · local] `chapter.tex:2128` uses `Chapter~\ref{ch:llm-foundations}` (good, label-based) but the surrounding prose at 2133–2138 refers to "the chapters on domain adaptation" and "the chapter on evaluation" by description rather than `\Cref`. Not hard-coded numbers (so not a violation), but unresolvable pointers reduce navigability.
  Fix: Replace descriptive chapter references with `\Cref{ch:...}` where the target labels exist.

---

## Per-dimension risk (which dimensions this chapter likely FAILS, with the blocking issue)

- `correctness`: **AT-RISK (≈85)** — body claims sound; "tripled 1993–2023 \citep{loughran2020textual}" window mismatch (MINOR) and unverified 0.67 (NIT) keep it under 90 pending check.
- `concept_separation`: **OK (≈90)** — clean `context`/`deepdive` usage throughout; intuition vs internals well delineated.
- `code_figure_correctness`: **AT-RISK (≈85)** — figures match prose, but EDGAR figure correctness is contingent on a live fetch / shipped cache (see reproducibility).
- `concept_ordering`: **FAIL (<90)** — `def:textual-signal` forward-refs `def:corpus-vocab` (576→680), defined 104 lines later (MAJOR).
- `progressive_learning`: **OK (≈88)** — good arc and an explicit "Looking Ahead" bridge; minor friction from over-deep RNN/attention detail this early.
- `non_repetition`: **FAIL (<90)** — RNN/LSTM/attention/√d_k re-derived from scratch (BLOCKER); Tetlock/LM/MLM restated downstream (MINOR).
- `finance_orientation`: **OK (≈92)** — finance-first framing (task-based labour model, EDGAR, earnings calls) is strong.
- `finance_examples`: **OK (≈90)** — TF-IDF worked example, risk-neighbours table, EDGAR growth are grounded and integrated.
- `citation_hygiene`: **OK (≈90)** — all used keys resolve in the active bib; multi-bib coexistence is a NIT.
- `citation_accuracy`: **FAIL (<90)** — `ke2019predicting` misdescribed as attention-based (MAJOR) + stale `didisheim2025memory` `[CITE:]` annotation (MAJOR).
- `completeness`: **OK (≈90)** — limitations, regulation, identification caveats all present.
- `notation_crossref`: **FAIL (<90)** — 9 duplicate labels shared with ch02 + `def:mlm` dup with ch03 (BLOCKER); in-ch01 `\ref`s silently resolve into later chapters.
- `reproducibility`: **FAIL (<90)** — EDGAR figure depends on live SEC fetch + hard-coded personal UA + undocumented shipped cache (MAJOR).
- `pedagogy`: **OK (≈88)** — clear objectives and scaffolding; the early full √d_k proof and BPTT Jacobian may overshoot a "first chapter" difficulty curve, but defensible.

**Dimensions judged < 90:** `concept_ordering`, `non_repetition`, `citation_accuracy`, `notation_crossref`, `reproducibility` (firmly failing); `correctness` and `code_figure_correctness` at-risk and likely <90 until the magnitude/figure claims are verified.

---

## One-paragraph assessment

The chapter is well written and finance-first, but it cannot pass as the book's opening chapter for four structural reasons. (1) It re-derives, from scratch and with its own proofs, four concepts ch02 owns (vanilla RNN, LSTM cell, scaled dot-product attention, the √d_k variance result) and a fifth ch03 owns (MLM) — violating the single-source-of-truth rule and, worse, creating **nine duplicate `\label`s with ch02 plus one with ch03**, so in-chapter `\ref`s silently resolve into later chapters. The fix for both the non_repetition and notation_crossref failures is the same: collapse ch01's §6–§7 into intuition-only `context` boxes that forward-reference ch02. (2) The first formal definition forward-references a definition introduced 100 lines later. (3) Two citation_accuracy defects: `ke2019predicting` is described as an attention model it is not, and the `didisheim2025memory` inline annotation names a different paper than the key resolves to. (4) The EDGAR growth figure is not reproducibly regenerable — live SEC fetch, hard-coded personal email in the User-Agent, and an undocumented shipped cache. Resolve these five and the chapter is close to release on the remaining dimensions.
