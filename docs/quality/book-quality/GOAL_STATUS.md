# GOAL_STATUS.md — Release-Quality Pass

> Goal: bring *Large Language Models in Finance* to release quality — every chapter and
> book-level dimension ≥90/100, the book compiles, and no duplicate labels, broken refs,
> unresolved citations, known wrong-paper citations, major concept-ordering failures,
> unnecessary repeated derivations, or orphaned finance examples.
>
> **Date:** 2026-06-20 · **Mode:** targeted, auditable edits (chapter order from
> `book/main.tex`), each verified by an independent re-audit and a clean compile.
>
> ## GOAL PASSED: **YES** — 16/16 chapters ≥90 on every dimension; all book-level gates green.

---

## 1. Result

| Metric | Start (iteration-0 audit) | End |
|--------|---------------------------|-----|
| Chapters passing (all 14 dims ≥90) | 0 / 16 | **16 / 16** |
| Book compiles | unverified | ✅ 626 pp |
| Duplicate labels | 10+ collisions | ✅ 0 |
| Broken refs | ≥4 (`ch:responsible-llms`, `fig:ch11-rag-pipeline`, …) | ✅ 0 |
| Undefined citations | unverified | ✅ 0 |
| Known wrong-paper citations | 5 (C1–C5) | ✅ 0 |
| Duplicate bib key | `wei2022emergent` | ✅ removed |
| Orphaned finance example | `valuation_example` | ✅ wired into ch05 |

Each chapter's pass was confirmed by an **independent re-audit subagent** scoring against
`RUBRIC.md`; the per-chapter closing edits are listed in `BOOK_SCORE.md`.

## 2. What was done (by cluster)

**Book-wide structural blockers (cleared first).** Collapsed all cross-chapter
`\label` collisions to one SSOT each + `\Cref` reminders (`eq:cosine-sim`, `def`/`eq:lora`
incl. a formula reconciliation, `def:rag`, `def:calibration`, `def:hallucination`,
`eq:rrf`, `rem:eu-ai-act`, `sec:rag-finance`, `tab:api-costs`, AppC `eq:lora`); removed the
duplicate `wei2022emergent` bib key; fixed every broken ref; converted **all** hard-coded
`Chapter~N` / `Chapter~\ref` prose to `\Cref`; rebuilt the two stale book-map tables; added
`cleveref` + `arrows.meta`.

**Citations.** Fixed all 5 wrong-paper citations (Integrated Gradients→`sundararajan2017axiomatic`,
FF3→`fama1993common`, Llama 2→`touvron2023llama2`, FINER-139→`loukas2022finer`, GPT-4
arithmetic→`frieder2023mathematical`); removed print-leaking "Needs verification" notes;
completed the `shah2022flue` stub; flagged/de-load-beared the unverifiable `chen2025aml`.
Throughout, **unverified working-paper point-numerics were hedged** to attributed-qualitative
claims (the goal's "never assert unverifiable numbers" rule) rather than asserted.

**Reproducibility / figures.** Authored **eleven committed, deterministic, network-free
figure generators** (`gen_*.py`, matplotlib `Agg`) for ch01, ch02, ch05, ch07, ch08, ch09,
ch10, ch11, ch12, ch13, ch15 — each reproducing a figure from fixed/published numbers in
the prose; replaced stub `demo.ipynb` files with real runnable notebooks; repointed prose
from stub `demo.ipynb` to the real `exercises.ipynb`; removed personal emails from SEC
User-Agents (env-var); fixed a raw-byte UTF-8 break in ch06's notebook; all generators wired
into `run_illustrations.sh`.

**Content.** ch05 WACC/CAPM derivation + `valuation_example` companion box; ch06 fairness
metric (disparate-impact ratio) + deepdive layering; ch10 Almgren-Chriss & MinTRL formula
corrections; ch14 dual-mode boxes; ch07 deepdive boxes + tagged exercises; ch01 inline API
listings (OpenAI/Anthropic/HuggingFace); SSOT bridges (SHAP, calibration, GDPR, FinBERT,
Tetlock); numerous concept-ordering and progressive-learning lifts.

## 3. Files modified

~30 `book/chapters/**` and `book/appendices/**` `.tex` files, `book/preamble.tex`,
`book/bibliography.bib`, 11 new `code/notebooks/**/gen_*.py`, 6 rewritten `demo.ipynb`,
`code/run_illustrations.sh`, and the `docs/quality/book-quality/` scorecards. Delivered
across ~55 commits, each verified against a clean compile.

## 4. Human decisions deferred (non-blocking; flagged, not silently changed)

These do **not** block the gate but are surfaced for the author:
- **`chen2025aml`** (future-dated arXiv id `2602.23373`): could not be verified; the
  Adverse Media Index is now presented as the book's own construct and the entry is
  uncited + marked `NEEDS_EXTERNAL_VERIFICATION`. Verify or delete the entry.
- **Working-paper numerics** were hedged rather than asserted; if the author can verify
  specific figures (BloombergGPT totals, KirtacGermano/Siano/VidalSSRN/Hampole numbers,
  etc.) they may be restored with precise values and `citation_accuracy` would only rise.
- **Stale `.bib` files** (`bibliography_bibertool.bib`, `bibliography_test.bib`) are not
  loaded by `preamble.tex` and can be deleted.
- The **`gen_king_analogy.py`** figure regenerates from the pinned `glove-wiki-gigaword-300`
  release (a one-time download, then cached); a committed pruned-vector snapshot would make
  it offline-deterministic like the others.

## 5. Verification

`/book-quality-regression`-equivalent checks all green (run this turn): clean
`pdflatex`×3 + `biber`, 0 duplicate labels, 0 multiply-defined, 0 undefined refs, 0
undefined cites, 0 biber-missing, 0 fatal errors, 626 pages. Per-chapter ≥90 confirmed by
independent re-audits recorded in `BOOK_SCORE.md`.

**The goal is met.**
