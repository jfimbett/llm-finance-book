# Editor Plan — Ch 09 Financial NLP and Sentiment Analysis (reading index 7)

Audit only — no edits applied. Date: 2026-06-20.
Derived from constructive-review.md + skeptical-review.md. Edits must be targeted/minimal.

## MUST_FIX (blocks a ≥90 on a non-N/A dimension)

1. **[non_repetition] Cross-reference, do not re-derive, the founding sentiment results.**
   At first mention of Tetlock (line 263, sec:ch09-news-wire-services) and Loughran–McDonald
   (lines 129–148, 318–320), add `\Cref{ch:intro}` (and `\Cref{ch:ai-ml-finance-text}` where
   apt) and compress the re-derived narrative to a one-line recap + pointer. ch01-intro is
   the single source of truth for the Tetlock 2007 "Abreast of the Market" story and the
   GI-vs-LM origin. Target dim 6.

2. **[non_repetition] Cross-reference ch08 for FinBERT/SEC-BERT at first use.**
   Insert `\Cref{ch:domain-specific-llms}` at the head of sec:ch09-finetuned-classifiers
   (line 174) and trim the model-introduction prose (lines 179–196) to the sentiment-specific
   delta, since ch08 (read 5th) already establishes these models. Target dim 6.

3. **[citation_accuracy] Mark unverifiable SSRN claims.**
   For each precise quantitative claim sourced only to an SSRN `@unpublished` paper
   (KirtacGermano2024 Sharpe 3.05 @219; Siano2025 3×/2× @291; FatemiHu2023 @223;
   ChiuHung2024 @324; Lehner2024 @324; XuBabaian2025 @84; CookKazinnik2023 @291;
   LopezLiraTang2023 @219), either verify against the source and add page/exhibit anchors,
   or soften to attributed-claim phrasing ("the authors report …"). Until verified the
   dimension is capped at 89. Target dim 10.

4. **[reproducibility] Fix or remove the demo stub.**
   `demo.ipynb` is a 2-cell placeholder. Either populate it with a runnable LM-vs-FinBERT
   sentiment demo, or delete it and update any references so `exercises.ipynb` is the sole
   notebook. Target dim 13.

## SHOULD_FIX (raises score; not strictly blocking)

5. **[notation_crossref] line 64** — change "Chapter~\ref{sec:ch09-earnings-call-transcripts}"
   to "Section~\ref{...}" (same-chapter section reference).

6. **[code_figure_correctness] exercises.ipynb** — rename `LM_POS`/`LM_NEG` to an explicit
   "illustrative proxy wordlist" and add a comment that the real LM dictionary has 2,355/354
   words; reconcile the notebook `net` formula (cell-5) with chapter eq:lm-sentiment (line
   136) or note the deliberate difference.

7. **[finance_examples] figures/** — consider committing one generated figure (CAR event
   study from exercises.ipynb [A], or an LM-vs-GI score-distortion bar chart) and `\input`
   it, to give the chapter a visual anchor. Optional but improves dim 8/13.

## OPTIONAL

8. **[completeness] line 101** — one sentence noting subword tokenizers reduce the need for
   case-folding/[NUM] substitution, consistent with the ch:llm-foundations cross-ref.
9. **[citation_hygiene]** — add `type`/`institution` to SSRN `@unpublished` entries (cosmetic).

## DO_NOT_CHANGE (protect — see constructive-review.md)

- Sources taxonomy (lines 39–86) — single source of truth for financial text sources.
- LM-vs-GI explanation + worked MD&A example (lines 141–171); arithmetic verified correct.
- FinBERT classifier-head math (eq:finbert-classifier) and Krippendorff α (eq:krippendorff-alpha,
  nominal + ordinal); both correct.
- CAR definition / SUE predictive regression / z-score standardisation (eqs car, zscore,
  sentiment-predictive-regression).
- Short- vs long-horizon synthesis + closing remark (lines 433–448).
- Fine-tuning FinBERT worked example (ex:finbert-finetuning) — honest "illustrative" framing.
- Production batch/streaming engineering (lines 492–513).
- Macro-F1-vs-neutral-class argument (lines 552–563).

## BOOK_WIDE_ITEMS

- **BW1 [non_repetition]** Establish single-source-of-truth ownership for the Tetlock 2007/2008
  and Loughran–McDonald 2011 founding results. Candidate owner: ch01-intro. ch09 and ch16
  must `\Cref` rather than re-narrate. (Spans ch01, ch16, ch09.)
- **BW2 [non_repetition]** FinBERT / SEC-BERT / Financial PhraseBank model descriptions
  duplicated across ch08 (owner) and ch09. Trim ch09 body to the sentiment-specific delta.
- **BW3 [citation_accuracy]** Book-wide policy needed for the ~10 SSRN `@unpublished` claims
  cited in ch09 (and likely elsewhere): require either source-verified anchors or
  attributed-claim phrasing before any chapter citing them can exceed 89 on dim 10.
