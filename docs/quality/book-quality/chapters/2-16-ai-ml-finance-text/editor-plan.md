# Editor Plan — Chapter 2 (reading order) · 16-ai-ml-finance-text

Audit only — no edits applied in this pass. This is the merged, prioritized plan.

## MUST_FIX (blocks ≥90)

1. **Replace all 5 hard-coded "Chapter~N" prose refs with `\Cref{ch:...}`.**
   - chapter.tex:114 "Chapter~12" → `\Cref{ch:xai-explainability}` (or whatever label `12-xai-explainability` defines)
   - chapter.tex:196 "Chapter~12" → same
   - chapter.tex:338 "Chapter~11" → `\Cref{ch:regtech...}`
   - chapter.tex:591 "Chapter~2" → `\Cref{ch:llm-foundations}`
   - chapter.tex:658 "Chapter~13" → `\Cref{ch:llm-limitations-evaluation}`
   Dimension: notation_crossref. This is the single biggest score lever.

2. **Fix the broken sentence at chapter.tex:526-529.** "...over time.  These\nResearchers applied these approaches..." Rewrite as one grammatical sentence, e.g. "Researchers applied these approaches to financial filings as early as the 1990s to measure changes in management tone and document readability \parencite{kearney2014textual}." Dimension: correctness.

3. **De-duplicate `wei2022emergent` in bibliography.bib (lines 1727 and 3175).**
   Keep one `@article` entry, delete the other. Dimension: citation_hygiene
   (BOOK-WIDE; affects this chapter because it cites the key twice).

## SHOULD_FIX

4. **Remove the leftover `% [CITE: ...]` TODO at chapter.tex:284** and either add the
   intended market-impact/HFT citation to Example `ex:algo-trading` or drop the
   marker. Dimension: correctness / citation_accuracy.

5. **Add a one-clause caveat to the universal-approximation sentence (chapter.tex:173-176)**:
   approximability is an existence result, not a learnability/trainability guarantee.
   Dimension: correctness / completeness.

6. **Verify the "as early as the 1990s" historical claim against `kearney2014textual`**
   (chapter.tex:529). If the survey does not support the 1990s date, re-attribute or
   soften. Mark NEEDS_EXTERNAL_VERIFICATION until checked. Dimension: citation_accuracy.

7. **Rework the inline gloss at chapter.tex:277** ("A deep reinforcement learning (...)
   agent") so the definition does not split the noun phrase. Dimension: pedagogy.

## OPTIONAL

8. Expand "VaR" on first use at chapter.tex:313. (pedagogy)
9. Reconcile the roadmap's exercises promise (chapter.tex:708-712) with the decision to
   remove book-body exercises (commit 1092660): soften to "exercises in the companion
   notebooks" or similar. (pedagogy)
10. Convert the bare `\ref{...}` section pointers at chapter.tex:20,74 to `\Cref`.

## DO_NOT_CHANGE (protect)

- Definitions: Symbolic/Statistical AI (89-103), Supervised Learning (137-146),
  LLM (208-223), Structured/Unstructured Data (364-380) — SSOT-grade, keep verbatim.
- `context` box markets↔nets (186-197); `deepdive` attention box (572-592);
  remark "LLMs are not a panacea" (646-659).
- EPS-beat finance example (440-450) and the Loughran–McDonald framing (413-418).
- Learning Objectives block (4-21) including the in-chapter forward pointers.

## BOOK_WIDE_ITEMS (feed the book backlog)

- **citation_hygiene — DUPLICATE KEY `wei2022emergent`.** SSOT: `book/bibliography.bib`
  (lines 1727 & 3175). Action: collapse to one `@article` entry; re-run
  `/audit-bibliography` to confirm no other dupes. Affects every chapter that cites it.
- **reproducibility — placeholder `demo.ipynb`.** SSOT: `code/notebooks/16-ai-ml-finance-text/demo.ipynb`.
  Action: either develop the demo notebook or remove it so the only paired notebook is
  the real `exercises.ipynb`; align with the book-wide notebook-completeness policy.
- **notation_crossref / cross-chapter-ordering — attention SSOT.** Owning chapter:
  `02-llm-foundations` (reading index 3). Action: ensure Chapter 2 defines the attention
  formula as the labelled single source of truth, and this chapter's `deepdive` box
  (chapter.tex:572) `\Cref`s it as an explicit preview rather than pointing by number.
- **reproducibility — live-EDGAR exercises notebook.** SSOT:
  `code/notebooks/16-ai-ml-finance-text/exercises.ipynb`. Action: decide book-wide policy
  on cached fixtures vs. live SEC API calls; pin filing accessions or ship a cache so
  results are deterministic offline.
