# Skeptical Review — Chapter 2 (reading order) · 16-ai-ml-finance-text

Audit only. Adversarial defect list. `SEVERITY · dimension_key · file:line — issue`.

## LOCAL defects

### notation_crossref (the main blocker cluster)
- **MAJOR · notation_crossref · chapter.tex:114 — hard-coded prose ref** "interpretability (Chapter~12)". RUBRIC §1.12 forbids hard-coded "Chapter N" prose refs; must be `\Cref{ch:...}`. With reading order 12 = `12-xai-explainability` this is also a forward dependency stated by absolute number, which is brittle.
- **MAJOR · notation_crossref · chapter.tex:196 — hard-coded prose ref** "Chapter~12" (explainability). Same issue.
- **MAJOR · notation_crossref · chapter.tex:338 — hard-coded prose ref** "Chapter~11 treats these applications in depth."
- **MAJOR · notation_crossref · chapter.tex:591 — hard-coded prose ref** "developed in Chapter~2." (This is the *next* chapter in reading order, folder `02-llm-foundations`; should be `\Cref{ch:llm-foundations}`.)
- **MAJOR · notation_crossref · chapter.tex:658 — hard-coded prose ref** "Chapter~13 is dedicated to these issues."
- **MINOR · notation_crossref · chapter.tex:20, 74 — `\ref{...}` for sections in prose** uses bare `\ref` ("Sections~\ref{...}") rather than `\Cref`; produces a bare number with manual "Sections" word. Cosmetic but inconsistent with the `\Cref` convention.

### correctness / completeness (prose artifacts)
- **MAJOR · correctness · chapter.tex:526-529 — broken sentence / grammar artifact.** "...over time.  These\nResearchers applied these approaches to financial filings as early as the 1990s..." The word "These" is a dangling fragment ("These [models? techniques?]") fused to a new sentence beginning "Researchers applied these approaches". Reads as an editing scar; the sentence is ungrammatical as written.
- **MINOR · citation_accuracy · chapter.tex:529 — citation placement.** The 1990s BoW-tone claim is attributed to `\parencite{kearney2014textual}` (a 2014 survey). The survey is a defensible secondary source for the historical claim, but the sentence reads as if Kearney & Liu did the 1990s work. NEEDS_EXTERNAL_VERIFICATION that the survey supports "as early as the 1990s." (caps citation_accuracy at 89).
- **MINOR · correctness · chapter.tex:284 — leftover authoring TODO in source.** `% [CITE: high-frequency trading AI applications, market impact models]` — a commented-out citation placeholder left in the example. Signals an intended-but-missing citation for the market-impact/feedback-loop claim in Example `ex:algo-trading` (273-285).
- **NIT · correctness · chapter.tex:277 — awkward inline gloss.** "A deep reinforcement learning (an agent trained via reinforcement learning with a deep neural network policy to maximise cumulative reward) agent..." The parenthetical is inserted mid-noun-phrase ("A deep reinforcement learning (...) agent"), which is clumsy. Define the term before the sentence or in a footnote.

### completeness (minor gaps)
- **MINOR · completeness · chapter.tex:173-176 — universal approximation overstated by omission.** "the universal approximation theorem ... hierarchical compositions ... can represent arbitrarily complex mappings given sufficient width or depth" cites `goodfellow2016deep`. The UAT is a *representation* (existence) result, not a *learnability* guarantee; the sentence does not flag that approximability ≠ trainability. A one-clause caveat would prevent overclaiming. (Borderline MAJOR for correctness.)
- **NIT · completeness · chapter.tex:313 — "variance-covariance VaR".** Phrase is used without expanding VaR (Value at Risk) on first use; mixed academic/industry audience mostly knows it, but the chapter otherwise defines terms.

### pedagogy
- **MINOR · pedagogy · chapter.tex:708-712 — exercises promised, none in book.** The roadmap states "Exercises at the end of each chapter are tagged by difficulty [B]/[I]/[A]" but this chapter.tex contains no exercises section (consistent with the project's decision to remove student exercises — see commit 1092660). The promise is now stale relative to the book body; either soften the wording or rely on the notebook.

## BOOK-WIDE defects (route to backlog)

- **MAJOR · citation [hygiene] · book/bibliography.bib:1727 & 3175 — DUPLICATE bib key `wei2022emergent`.** The same key `@article{wei2022emergent,...}` is defined twice (identical title/journal/year, author list reformatted). This is a duplicate-key hygiene defect in the shared `.bib`; biber will warn/error or silently take one. Cited from this chapter at chapter.tex:229,631 — so it affects this chapter's citation_hygiene. SSOT = bibliography.bib. Owning fix: de-duplicate to a single entry.
- **MINOR · code-figure [reproducibility] · code/notebooks/16-ai-ml-finance-text/demo.ipynb — placeholder stub.** Single markdown cell ending "> **Status:** Placeholder — content to be developed alongside `/draft-chapter`." No demo code. The chapter does not `\includegraphics` anything, so it does not block code_figure_correctness, but the paired *demo* notebook is a stub while the *exercises* notebook is real. Book-wide reproducibility consistency item.
- **MINOR · book-repetition / cross-chapter-ordering — attention formula appears here (deepdive, chapter.tex:572) and is "developed in Chapter 2".** Intentional preview, acceptable, BUT the forward reference must become a `\Cref` (see notation_crossref above) and Chapter 2 should be the SSOT (`\Cref{def/eq:attention}`), with this box explicitly labelled a preview. Route to backlog to confirm Chapter 2 owns the attention SSOT and this box cross-refs it.
- **INFO · finance-example — EDGAR exercises notebook hits live SEC endpoints** (`requests.get(...sec.gov...)`). Reproducible only with network + stable EDGAR API; no cached fixtures or pinned filing accessions. Book-wide reproducibility policy item (cache vs. live).

## Non-defects (checked, clean)
- All 9 distinct `\cite` keys resolve in bibliography.bib (goodfellow2016deep, kearney2014textual, lopezdeprado2018advances, loughran2020textual, wei2022emergent, wu2023bloomberggpt, loughran2011liability, tetlock2007giving, vaswani2017attention).
- No `\includegraphics` and no figures referenced; `figures/` holds only `.gitkeep`. No figure↔text contradiction possible.
- No duplicate `\label` within the chapter (33 labels, all distinct).
- `\ref` targets (sec:ai-ml-dl-hierarchy, subsec:llms-special-case, subsec:transformer-revolution) all resolve to labels defined in-chapter.
- attention formula (572-584) and supervised-learning ERM (137-146) are mathematically correct and re-derivable.
- Concept ordering: token/vocabulary/attention all defined in-chapter before/at first substantive use; only `01-intro` precedes this chapter and nothing later is *used* (only previewed).
