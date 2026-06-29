# Skeptical Review — Ch 09 Financial NLP and Sentiment Analysis (reading index 7)

Audit only — no edits applied. Date: 2026-06-20.
Format: `SEVERITY · dimension_key · file:line — issue`. Scope tagged local / book-wide.

## BLOCKER

(none — no factually wrong claims or broken refs found)

## MAJOR

- **MAJOR · citation_accuracy · book/chapters/09-financial-nlp-sentiment/chapter.tex:84,219,223,291,324 — [book-wide / citation]**
  Ten+ specific quantitative claims rest on `@unpublished` SSRN working papers that cannot
  be verified locally: `KirtacGermano2024` "Sharpe ratio of 3.05" (line 219), `Siano2025`
  "explain three times more return variation … double the R²" (line 291), `FatemiHu2023`
  "fine-tuned smaller LLMs match SOTA … no gain beyond a small few-shot set" (line 223),
  `ChiuHung2024` "LLaMA-2 … higher buy-and-hold abnormal returns than FinBERT" (line 324),
  `Lehner2024`, `XuBabaian2025`, `CookKazinnik2023`, `LopezLiraTang2023`. Each is precise
  enough to be wrong. → NEEDS_EXTERNAL_VERIFICATION. Caps `citation_accuracy` at 89.

- **MAJOR · non_repetition · chapter.tex:263,318–320,591 vs ch01-intro:168–256, ch16:415–467 — [book-repetition]**
  Tetlock 2007/2008 and Loughran–McDonald 2011 are *narratively re-derived* here (the
  "Abreast of the Market" regression, the WSJ negative-word result, the GI-vs-LM
  liability/tax argument) after being developed at length in ch01-intro (read 1st, lines
  168–256) and again in ch16 (read 2nd, lines 415–467). Ch09 never `\Cref`s ch01 or ch16
  for these founding results — only ch08/ch14/ch13 are cross-referenced (line 599). RUBRIC
  ground rule explicitly warns: "sentiment/lexicon material that overlaps ch01-intro
  (Loughran-McDonald, Tetlock) — should be cross-referenced, not re-derived." This is the
  single largest issue in the chapter.

- **MAJOR · non_repetition · chapter.tex:174–196 vs ch08:211–246 — [book-repetition]**
  FinBERT / SEC-BERT / Financial PhraseBank are introduced in detail in ch08 (read 5th,
  Domain-Specific LLMs, lines 211–246, incl. the Araci-2019 vs Yang-2020 FinBERT name
  collision). Ch09 re-introduces FinBERT (line 179–192) and SEC-BERT (194–196) from
  scratch. The end-of-chapter pointer to ch08 (line 599) exists but the *body* re-derives.
  Designate ch08 as single source of truth for the models; ch09 should `\Cref{ch:domain-specific-llms}`
  at first mention and keep only the sentiment-specific specialisation.

- **MAJOR · reproducibility · code/notebooks/09-financial-nlp-sentiment/demo.ipynb — [code-figure]**
  `demo.ipynb` is a 2-cell stub: imports numpy/pandas and prints `"Chapter 09 demo
  notebook"`. It demonstrates none of the chapter's concepts despite its own markdown
  claiming to "demonstrate the key concepts from Chapter 09." Either populate it or rely
  solely on `exercises.ipynb`.

## MINOR

- **MINOR · notation_crossref · chapter.tex:64 — [local]**
  "Chapter~\ref{sec:ch09-earnings-call-transcripts} returns to this source in detail" uses
  the word **Chapter** but `\ref`s a *section* label *within the same chapter*. Should read
  "Section~\ref{...}". Hard-coded-noun-vs-label mismatch (RUBRIC dim 12 anchor).

- **MINOR · code_figure_correctness · exercises.ipynb cell-3 (LM_POS/LM_NEG) — [code-figure]**
  The notebook hand-rolls ~20-word `LM_POS`/`LM_NEG` sets and the function is named
  `lm_sentiment`, implying these are the Loughran–McDonald lists. The real LM negative list
  has 2,355 words and positive 354 (per def:lm-dictionary, line 145). The toy wordlist
  should be labelled as an illustrative proxy, not "LM", to avoid contradicting the chapter.

- **MINOR · code_figure_correctness · exercises.ipynb cell-5 (net formula) — [code-figure]**
  Notebook computes `net = (p_cnt - n_cnt)/(p_cnt + n_cnt + 1e-9)` — a normalised polarity
  ratio — whereas the chapter's eq:lm-sentiment (line 136) divides by total word count
  `N_words(d)`. The notebook formula differs from the chapter's stated definition without
  comment.

- **MINOR · completeness · chapter.tex:101 — [local]**
  "[NUM]" number-handling and case-folding advice for "transformer models trained with case
  information" is sound, but the chapter never states that subword tokenizers (its own
  recommended models) largely make case-folding/number-token substitution unnecessary —
  a small inconsistency with the cross-ref to ch:llm-foundations tokenization.

- **MINOR · finance_examples · figures/ empty — [code-figure]**
  `book/chapters/09-financial-nlp-sentiment/figures/` contains only `.gitkeep`. The chapter
  has no `\includegraphics` (verified), so this is not a broken-figure issue, but the
  chapter would benefit pedagogically from at least one figure (e.g., CAR event-study plot
  the exercises notebook already produces).

## NIT

- **NIT · correctness · chapter.tex:499 — [local]** "hundreds of documents per second" for
  FinBERT-110M on A100 is plausible but vague; fine as illustrative ("exact figures depend…").
- **NIT · citation_hygiene · bibliography.bib (SSRN block) — [citation]** SSRN `@unpublished`
  entries lack `institution`/`type` fields; biber will render them as bare notes. Cosmetic.
