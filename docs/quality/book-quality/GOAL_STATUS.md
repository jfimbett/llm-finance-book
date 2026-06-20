# GOAL_STATUS.md — Release-Quality Pass

> Goal: bring *Large Language Models in Finance* to release quality — every chapter and
> book-level dimension ≥ 90/100, the book compiles, and no duplicate labels, broken refs,
> unresolved cites, known wrong-paper citations, major concept-ordering failures,
> unnecessary repeated derivations, or orphaned finance examples.
>
> **Date:** 2026-06-20 · **Mode:** targeted, auditable edits (chapter order from
> `book/main.tex`) · **Goal passed:** **NO (1/16 chapters pass)** — every
> structural/citation/correctness blocker is cleared, the book compiles cleanly (620 pp),
> and **ch05 is the first chapter to clear all 14 dimensions** after its figure was made
> deterministic. Independent re-audits (ch02/05/11/12) show 9–14 of 14 dimensions now pass
> per chapter. The residual gap is **deterministic figures for ch01–07 + figure creation
> for ch08–16 + non-stub notebooks + external numeric verification** (see §5).
>
> **Demonstrated path to passing (ch05):** replace a live-data figure with a committed,
> deterministic, network-free generator. `gen_dcf_sensitivity.py` regenerates the DCF
> heatmap from a fixed documented FCF (no `yfinance`), lifting reproducibility 78→96 and
> code_figure 89→95. The same method applies to the other figure-having chapters; ch08–16
> additionally need figures authored.

---

## 1. Summary

This pass cleared **every book-wide structural blocker** in `IMPLEMENTATION_BACKLOG.md`
(items 1, 3–10) and a batch of citation/correctness defects, verifying after each change
with a full LaTeX + biber build. The book now compiles **clean**:

| Mechanical gate | Result |
|-----------------|--------|
| Book compiles (`pdflatex`×3 + `biber`) | ✅ 620 pages, `main.pdf` 2.56 MB |
| Duplicate `\label`s (chapters + appendices) | ✅ none |
| "multiply defined" warnings | ✅ 0 |
| Undefined references (`??`) | ✅ 0 |
| Undefined citations | ✅ 0 |
| biber "didn't find a database entry" | ✅ 0 |
| Fatal errors | ✅ 0 |

What is **not** yet met: per-chapter ≥90 on **all** 14 dimensions. The binding constraint
is `reproducibility` (book-level 52) and `code_figure_correctness` (70), both gated by the
notebook/figure work in §5, plus several per-chapter `non_repetition` trims still
recommended (§4).

---

## 2. Blockers fixed (verified by clean compile)

| # | Blocker | Fix |
|---|---------|-----|
| 1 | 10+ duplicate `\label`s from re-derived concepts | Collapsed each to one SSOT + `\Cref`: `eq:cosine-sim`→ch01; `def:lora`/`eq:lora`→ch03 (ch02/ch06/AppC defer; **formula reconciled** on the scaled `α/r` form); `def:rag`→ch02 pipeline (ch04 recast as `def:rag-marginal`); `def:calibration`→ch07 renamed `def:fairness-calibration`; `def:hallucination`→ch01; `eq:rrf`→ch02; `rem:eu-ai-act`→ch01 (ch03 `-highrisk`); `sec:rag-finance`→ch04 (ch02 `-foundations`); `tab:api-costs`→ch01 (ch02 `tab:api-pricing`) |
| 3 | Duplicate bib key `wei2022emergent` | Removed redundant block |
| 4 | ch05 WACC used 36×, never derived | Added `def:wacc` (`eq:wacc`, `eq:capm`) deriving WACC weights + CAPM cost of equity before first DCF use |
| 5 | `\ref{ch:responsible-llms}` undefined (ch12) | Repointed → `\Cref{ch:applications-future}` (owns the fairness/ECOA material) |
| 6 | Dangling `\ref{fig:ch11-rag-pipeline}` | Created a self-contained TikZ dataflow figure (added `arrows.meta`) |
| 7 | 5 wrong-paper citations | C1 `frieder2023mathematical` (GPT-4 arithmetic); C2 `sundararajan2017axiomatic` (Integrated Gradients); C3 `fama1993common` (FF3); C4 `touvron2023llama2` (Llama 2); C5 `loukas2022finer` (FINER-139 XBRL) |
| 8 | ch01 re-derived ch02's RNN/LSTM/attention/MLM | Resolved by the prior committed SSOT trim + new reminder edits |
| 9 | Orphaned `exercises/valuation_example/` | Added `rem:valuation-companion` linking the real AAPL DCF, quoting its committed CAPM (`r_E≈9.0%`), WACC (8.84%), triangulated \$221.04 vs \$226.84, + reader exercise + EDGAR/yfinance FCF reconciliation |
| 10 | 22 hard-coded `Chapter~N` refs + 2 stale book-map tables | All prose `Chapter~N`→`\Cref{ch:...}` (reading-order-correct); `tab:roadmap` (ch02) replaced with `\Cref` prose; `tab:chapter-map` (ch07) rebuilt to the true 16-chapter order using `\ref{ch:...}` numbering |

Also fixed: enabled `cleveref` (`\Cref`) — the SSOT-reminder pattern depends on it.

## 2b. Smaller correctness / citation / hygiene fixes

- **B5** ch06 SR 11-7 "In 2012"→"In 2011" (matches bib `sr117`).
- **B8** ch16 repaired fused "These Researchers" sentence.
- **B9** ch09 LM example: formula already matches `eq:lm-sentiment`; corrected the
  uncertainty bullet (had non-LM words) and framed assignments as illustrative.
- **B10** ch13 ECE example factor `0.012`→`0.12` (product unchanged).
- **B12** ch01 "10-K word count roughly tripled"→"rose markedly" (was inconsistent with
  the chapter's own figure).
- **B13** ch01 `ke2019predicting` — already correctly described after the SSOT trim.
- **A9** ch05 ReAct → recall + `\Cref{ch:llm-agents}`.
- **A3/A4/A5/A6** cosine / LoRA / RAG / calibration repetitions reduced to reminders.
- **Bib hygiene (D1–D5 partial):** removed print-leaking "Needs verification before final
  release" notes from real papers (ECTSum, FLUE, Li 2013, Boudoukh 2013, Frattaroli,
  Ko, Xu→"Working paper"); flagged `chen2025aml` (future-dated arXiv id `2602.23373`)
  as `NEEDS_EXTERNAL_VERIFICATION` and stripped the fabricated id.

## 2c. Reproducibility — authorised tractable fixes (E1/E3)

- **Repointed all 24 notebook pointers** from the stub `demo.ipynb` to the genuine
  worked `exercises.ipynb` and dropped the false "the complete implementation" claim
  (ch01/02/04/05/07). This is `CODE_FIGURE_AUDIT` item 1's "point prose at
  `exercises.ipynb`" path — the highest-impact single action that does not require
  filling the stubs.
- **De-PII'd the code**: removed `instructor@dauphine.eu` / `jfimbett@gmail.com` from every
  SEC EDGAR User-Agent across `code/notebooks/**`; `gen_edgar_text_growth.py` now reads
  `EDGAR_USER_AGENT` from the environment with a placeholder default.

---

## 3. Files modified (19) + commits

`book/preamble.tex`, `book/bibliography.bib`, and chapters
01, 02, 03, 04, 05, 06, 07, 09, 10, 11, 12, 13, 14, 15, 16 + appendices C, D.
(+294 / −219.)

```
1b5f882 resolve book-wide blockers — dup labels, broken refs, dup bib key
3bb8bf7 ch05: derive WACC/CAPM, wire valuation_example, fix citations
bed9416 correct wrong-paper citations + small correctness errors
f91d1e7 convert hard-coded Chapter~N refs to \Cref; rebuild stale ch02 roadmap
c8208e8 ch07: rebuild stale tab:chapter-map to true 16-chapter reading order
c28684d bib hygiene — stop print-leaking TODO notes; flag fabricated id
bce0cf0 ch09 LM example; mark backlog blockers resolved
```

---

## 4. Remaining failures (tractable, no human input needed)

Per-chapter `non_repetition` / `progressive_learning` items:

- **A7** ch13 calibration — **DONE (bridge)**: added a forward/back bridge to
  `\Cref{ch:credit-risk}`. The full derivation is *kept* because ch13 is the evaluation
  chapter where calibration/ECE is a learning objective (the audit's earliest-appearance
  SSOT conflicts with topical ownership here).
- **A8** ch12 SHAP — **DONE (bridge)**: explicit "applied in `\Cref{ch:credit-risk}`;
  developed in full here" bridge. Kept in ch12 (the explainability chapter is SHAP's
  topical home).
- **A10** ch15 GDPR/MiFID — **DONE (bridge)**: defers Arts 5/17/22 + MiFID II to
  `\Cref{ch:regtech-compliance-aml}`, keeps only the local-deployment-specific framing.
- **A11** ch09 FinBERT — **DONE (bridge)**: defers the model to
  `\Cref{ch:domain-specific-llms}`, keeps the sentiment use.
- **A12** Tetlock/LM founding results re-narrated ch09/ch16 — **OPEN (low priority)**: the
  citations are used in topically-appropriate ways; a light `\Cref{ch:intro}` recall would
  suffice but is marginal.
- **B7** ch14 has no context/deepdive layering → add concept_separation boxes (OPEN).

> **Structural note for the author:** for SHAP (A8) and calibration (A7), the SSOT
> direction is a genuine judgement call — the *earliest* full derivation is ch06
> (credit-risk), but the *topical* home is ch12 (explainability) / ch13 (evaluation).
> This pass kept the derivations in the topical chapters and added bridges rather than
> gutting them; revisit if a different SSOT is preferred.

---

## 5. What now remains (and why it is not a targeted-edit task)

`reproducibility` and `code_figure_correctness` are still below 90 for several chapters.
The **authorised, tractable part is now DONE** (see §2c); what remains is genuinely
large-engineering or human-gated:

**Done this pass (authorised by `CODE_FIGURE_AUDIT` item 1 — "point prose at
`exercises.ipynb`"):**
- All 24 false "the complete Python implementation … `demo.ipynb`" pointers repointed to
  the real `exercises.ipynb` (the stubs are no longer cited as authoritative).
- Personal emails removed from every SEC EDGAR User-Agent in `code/`; the generator
  script now reads `EDGAR_USER_AGENT` from the environment.

**Remaining — large engineering / human-gated (not prose edits):**
1. **Generate figures for ch08–16 + appendices** (empty `figures/`). Data-driven figures
   need either live SEC/yfinance fetches (themselves flagged as non-deterministic) or
   vendored snapshots; schematic figures need author design intent. ch08 also lacks an
   `\illustration` block. *This is the single largest remaining lever and is content
   creation, not editing.*
2. **Fill the 16 `demo.ipynb`** (or accept the repointing in §2c as the final answer).
   Filling is a content/engineering task; the audit lists it as a book-wide effort.
3. **Data-snapshot infrastructure**: vendor frozen SEC/yfinance/GloVe snapshots, add
   seeds, pin accessions, and extend `run_illustrations.sh` past ch01–07.
4. **Empty `code/src/__init__.py` / `code/tests/`** (E6) — build the "shared package" or
   drop the claim (human decision).
5. **External verification** of working-paper numerics flagged
   `NEEDS_EXTERNAL_VERIFICATION` (BloombergGPT totals, KirtacGermano Sharpe 3.05,
   `chen2025aml`/Adverse Media Index, FinanceBench %, Hampole, `kang2023hallucination`),
   and **delete stale `bibliography_*.bib`** (D7, confirmed not loaded) — both human-gated.

## 5b. Per-chapter polish completed this pass

- **B7** ch14 concept_separation: added context/deepdive layering to the ROUGE & BERTScore
  derivations (0 → 4 dual-mode boxes).
- **A7/A8/A10/A11** SSOT bridges (SHAP, calibration, GDPR, FinBERT).
- **A12** ch09 Tetlock founding-result recall → `\Cref{ch:intro}`.

---

## 6. Recommended next steps

1. Decide the **notebook strategy** (§5.1) — unblocks `reproducibility`/`code_figure`
   for all 16 chapters at once.
2. Apply the **A7/A8/A10/A11/A12 + B7** trims (§4) — `non_repetition`/`concept_separation`.
3. Re-run `/audit-book-quality` to refresh scores, then `/book-quality-regression`.
4. Verify the flagged working-paper numerics; delete stale `.bib` files.

**Compile status: green. Structural integrity: green. Goal gate: blocked on
reproducibility (human decision).**
