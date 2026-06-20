# IMPLEMENTATION_BACKLOG.md

> Prioritized backlog for the book-quality goal system. **Status: FULL 16-chapter audit
> complete (2026-06-20).** Items are `BLOCKER` / `MAJOR` / `MINOR`. "Owning chapter" uses
> **reading index** (see `RUBRIC.md`). Status: `OPEN` until fixed by `/iterate-book-quality`
> and verified by `/book-quality-regression`. Cross-cutting detail lives in the sibling
> maps (`REPETITION_MAP`, `CONCEPT_DEPENDENCY_MAP`, `CITATION_DESCRIPTION_AUDIT`,
> `CODE_FIGURE_AUDIT`, `FINANCE_EXAMPLES_MAP`).

## Top 10 blockers across the whole book (fix order)

> **Update 2026-06-20 (release-quality pass):** Items 1, 3, 4, 5, 6, 7, 8, 9, 10
> are **DONE** and verified by a clean full compile (no multiply-defined labels,
> no undefined refs, no undefined cites). Item **2 (notebook/figure
> reproducibility) remains OPEN** — it is the principal blocker to all-chapter
> ≥90 and needs a human decision (fill 16 `demo.ipynb` vs. repoint prose to the
> real `exercises.ipynb`; generate ch08–16 figures; data snapshots). See
> `GOAL_STATUS.md`.

| # | Sev | Issue | Dimensions lifted | Owner | Status |
|---|-----|-------|-------------------|-------|--------|
| 1 | BLOCKER | 10+ duplicate `\label`s from re-derived concepts (see §A) | notation_crossref, non_repetition, concept_ordering, progressive_learning | ch01/ch02 + SSOTs | ✅ DONE |
| 2 | BLOCKER | All 16 `demo.ipynb` are stubs cited as "the complete implementation" | reproducibility, code_figure_correctness | book-wide | ⛔ OPEN (human decision) |
| 3 | BLOCKER | Duplicate bib key `wei2022emergent` (bibliography.bib:1727 & 3175) | citation_hygiene + build | bibliography.bib | ✅ DONE |
| 4 | BLOCKER | ch05 WACC used 36+× but never derived (no CAPM/r_E/r_D) | completeness, finance_orientation, concept_ordering | ch05 (#9) | ✅ DONE (def:wacc/eq:capm) |
| 5 | BLOCKER | `\ref{ch:responsible-llms}` (ch12:890) targets a nonexistent label → `??` | notation_crossref, correctness | ch12 (#13) | ✅ DONE (→ch:applications-future) |
| 6 | BLOCKER | Dangling `\ref{fig:ch11-rag-pipeline}` (ch11:172) — figure never defined | notation_crossref, code_figure_correctness | ch11 (#12) | ✅ DONE (TikZ figure created) |
| 7 | MAJOR | 5 wrong-paper citations (see §C) | citation_accuracy | ch05, ch12, ch13, ch14, ch15 | ✅ DONE (C1–C5) |
| 8 | MAJOR | ch01 §6–§7 re-derives ch02's RNN/LSTM/attention/√d_k/MLM (root of #1) | non_repetition | ch01→ch02 SSOT | ✅ DONE (prior SSOT commit + reminders) |
| 9 | MAJOR | Orphaned `exercises/valuation_example/` (real AAPL DCF) never linked from ch05 | finance_examples, reproducibility, completeness | ch05 (#9) | ✅ DONE (rem:valuation-companion) |
| 10 | MAJOR | 22 hard-coded "Chapter~N" prose refs (ch02×15, ch16×5, ch10×1, ch14×1) + stale roadmap/chapter-map tables | notation_crossref, correctness | ch02, ch16, ch07, ch10 | ✅ DONE (all →\Cref; both tables rebuilt) |

## A. Cross-chapter / structural (book-wide) — VERIFIED

| # | Sev | Issue | Dimension(s) | Owning / SSOT | Action | Status |
|---|-----|-------|--------------|---------------|--------|--------|
| A1 | BLOCKER | `def:lstm` ch01:1584⇄ch02:455; `eq:rnn-jacobian` ch01:1533⇄ch02:402; `eq:multihead` ch01:1710⇄ch02:854 (+ `eq:lstm-*`) | notation_crossref, non_repetition | **SSOT = ch02 (#3)** | Collapse ch01 to intuition + `\Cref`; remove colliding labels | OPEN |
| A2 | BLOCKER | `def:mlm` ch01:1786⇄ch03:389 | notation_crossref | ch02 owns; ch03 reminds | `\Cref`; one label | OPEN |
| A3 | BLOCKER | `eq:cosine-sim` ch01:868⇄ch02:2004⇄ch05:926 (×3) | notation_crossref, non_repetition | **SSOT = ch01 (#1)** | ch02/ch05 → `\Cref`; remove redefs | OPEN |
| A4 | BLOCKER | `def:lora` ch02:2184⇄ch03:781; `eq:lora` ch02:2189⇄ch03:786⇄ch06:299 (×3) — **and ch02/ch03 formulas disagree** ($W_0+BA$ vs $W_0+\frac{\alpha}{r}BA$) | notation_crossref, non_repetition, correctness | **SSOT = ch03 (#4)** | Reconcile on ch03 form; others `\Cref` | OPEN |
| A5 | BLOCKER | `def:rag` ch02:1972⇄ch04:763 (two competing definitions) | notation_crossref, non_repetition | **SSOT = ch04 (#6)** | ch02 → `\Cref`; ch07 reminder | OPEN |
| A6 | MAJOR | `def:calibration` ch06:382⇄ch07:400 — **different concepts** (PD-calibration vs fairness "calibration within group") | notation_crossref | ch06 keeps; ch07 **renames** | rename ch07 label `def:fairness-calibration` | OPEN |
| A7 | MAJOR | Calibration re-defined in ch13 (`def:ch13-perfect-calibration` + Platt/isotonic/ECE) | non_repetition | **SSOT = ch06 (#10)** | ch13 → `\Cref` | OPEN |
| A8 | MAJOR | SHAP fully re-derived ch06 (#10) and ch12 (#13) | non_repetition | **SSOT = ch06** | ch12 → `\Cref`; add forward-ref from ch06 | OPEN |
| A9 | MAJOR | ReAct re-introduced in ch05 (ch04 is SSOT) | non_repetition | **SSOT = ch04 (#6)** | ch05 → reminder + `\Cref{ch:llm-agents}` | OPEN |
| A10 | MAJOR | GDPR Arts 5/17/22 + MiFID II developed in full in both ch11 (#12) and ch15 (#16) | non_repetition | **SSOT = ch11 (#12)** | ch15 → `\Cref`; unify bib keys | OPEN |
| A11 | MAJOR | FinBERT/SEC-BERT/Financial PhraseBank re-narrated ch09 (ch08 owns) | non_repetition | **SSOT = ch08 (#5)** | ch09 → trim to sentiment delta | OPEN |
| A12 | MAJOR | Tetlock + Loughran–McDonald founding results re-narrated ch09/ch16 | non_repetition | **SSOT = ch01 (#1)** | ch09/ch16 → `\Cref` | OPEN |
| A13 | MAJOR | 22 hard-coded "Chapter~N" prose refs + stale `tab:roadmap` (ch02:2563) & `tab:chapter-map` (ch07:56) & "Six chapters ago" (ch07:38) & wrong-target "Chapter 7" (ch10:923) | notation_crossref, correctness | each chapter | Convert to `\Cref{ch:...}`; rebuild tables from `main.tex` | OPEN |
| A14 | MAJOR | CAPM never properly defined before its use at #9 (only inline stray ch09:411) | concept_ordering, completeness | new SSOT near #7/#9 | Define CAPM before WACC (ties to #4) | OPEN |
| A15 | MINOR | ch16 logically introductory but at reading #2; uses biblatex `\parencite/\textcite` vs `\citet/\citep` | progressive_learning, citation_hygiene | ch16 | Decide role; unify citation macros | OPEN (human decision) |
| A16 | MINOR | Open-weight-models/quantisation overlap ch15 ⇄ Appendix C | non_repetition | Appendix C (hands-on SSOT) | ch15 → `\Cref` | OPEN |

## B. Local chapter defects — VERIFIED

| # | Sev | Issue | Chapter | Dimension | Action | Status |
|---|-----|-------|---------|-----------|--------|--------|
| B1 | BLOCKER | WACC never derived | ch05 (#9) | completeness, finance_orientation | Add WACC/CAPM box via companion exercise (B2) | OPEN |
| B2 | MAJOR | Orphaned `exercises/valuation_example/` not linked | ch05 (#9) | finance_examples, reproducibility | One companion `remark` box; surface its CAPM/WACC | OPEN |
| B3 | BLOCKER | `\ref{ch:responsible-llms}` undefined | ch12 (#13) | notation_crossref | Add the chapter/label or remove the ref | OPEN |
| B4 | BLOCKER | Dangling `\ref{fig:ch11-rag-pipeline}` | ch11 (#12) | notation_crossref, code_figure | Create figure or remove ref | OPEN |
| B5 | MAJOR | SR 11-7 dated "In 2012" (issued 2011; contradicts own bib `sr117`) | ch06 (#10) | correctness | Fix to 2011 | OPEN |
| B6 | MAJOR | `tab:roadmap` describes a non-existent book structure | ch02 (#3) | correctness | Rebuild from `main.tex` or delete | OPEN |
| B7 | MAJOR | Zero context/deepdive boxes; equation derivations interleaved with intuition | ch14 (#8) | concept_separation | Add layer separation | OPEN |
| B8 | MAJOR | Fused ungrammatical sentence (editing artifact, line 526) | ch16 (#2) | correctness | Repair sentence | OPEN |
| B9 | MAJOR | Toy ~20-word list mislabeled as Loughran–McDonald; net formula diverges from `eq:lm-sentiment` | ch09 (#7) | reproducibility, correctness | Use real LM list or relabel | OPEN |
| B10 | MINOR | ECE display typo line 118 (`0.012`→`0.12`) | ch13 (#14) | correctness | Fix typo | OPEN |
| B11 | MINOR | FCF $98.8B (yfinance) vs $108.8B (EDGAR) shown without reconciliation | ch05 (#9) | code_figure | One-line reconciliation note | OPEN |
| B12 | MINOR | ch01 "10-K length tripled 1993–2023" vs ~1.56× figure data | ch01 (#1) | correctness, code_figure | Attribute/soften | OPEN |
| B13 | MINOR | ch01 mischaracterizes `ke2019predicting` as "attention-based" (1728) | ch01 (#1) | citation_accuracy | Reword | OPEN |

## C. Wrong-paper citations (citation_accuracy)

| # | Sev | Chapter:line | Key | Fix | Status |
|---|-----|--------------|-----|-----|--------|
| C1 | MAJOR | ch05:645 | `frieder2023large` | Repoint to "Mathematical Capabilities of ChatGPT" (2301.13867) | OPEN |
| C2 | MAJOR | ch12:393 | `sundararajan2020shapley` for Integrated Gradients | Add + cite Sundararajan, Taly & Yan **2017** | OPEN |
| C3 | MAJOR | ch13:636 | `fama1970efficient` for FF3 | Replace with `fama1993common` | OPEN |
| C4 | MAJOR | ch15:136 | `touvron2023llama` for Llama 2/3 | Add a Llama 2 (2023) entry; repoint | OPEN |
| C5 | MAJOR | ch14:222 | `shah2023finer` for FINER-139 | Likely `loukas2022finer` (FiNER, ACL 2022); verify | OPEN |

## D. Bibliography hygiene (re-run `/audit-bibliography` fresh — old report stale)

| # | Sev | Issue | Action | Status |
|---|-----|-------|--------|--------|
| D1 | BLOCKER | `wei2022emergent` duplicated (1727 & 3175) | Delete redundant block | OPEN |
| D2 | MAJOR | Stub `note={Needs verification…}` entries: `shah2022flue`, `frattaroli2019`, `mukherjee2022ectsum`, `shen2023nlp` | Verify/replace before release | OPEN |
| D3 | MAJOR | Live inline flags: `zhang2024financebench % [CHECK]`, `fincen2020aml % [CITE: verify]` | Resolve | OPEN |
| D4 | MAJOR | `chen2025aml` arXiv `2602.23373` future-dated (Feb-2026), inconsistent with year — likely fabricated | Verify or remove (backs ch11 AMI claim) | OPEN |
| D5 | MAJOR | `xu2024stock` stub ("and others", venue TBD) | Complete or remove | OPEN |
| D6 | MINOR | `liu2018` year=2019 mismatch; `ziemke2024temporal` author/year drift | Fix fields | OPEN |
| D7 | MINOR | 2 stale `.bib` files (`bibliography_bibertool.bib`, `bibliography_test.bib`) | Delete (human-confirmed; not loaded) | OPEN (human decision) |
| D8 | MINOR | ~9 uncited entries (goodfellow2016deep, jegadeesh1993returns, …) | Cite or prune | OPEN |

## E. Reproducibility / code-figure (book-wide)

| # | Sev | Issue | Action | Status |
|---|-----|-------|--------|--------|
| E1 | BLOCKER | All 16 `demo.ipynb` are stubs but cited as the implementation | Fill, or point prose at `exercises.ipynb` | OPEN |
| E2 | MAJOR | Figures only for ch01–07; ch08–16 + appendices empty `figures/` | Generate figures; ch08 also lacks `\illustration` | OPEN |
| E3 | MAJOR | Live/non-deterministic deps (SEC/EDGAR, ~1GB GloVe, yfinance) + hard-coded personal User-Agents | Parameterize UA; vendor snapshots; seed | OPEN |
| E4 | MAJOR | `run_illustrations.sh` covers only ch01–07; `gen_*.py` not wired | Extend coverage | OPEN |
| E5 | MINOR | Mojibake / `[Placeholder]` cells in executed nbs (ch06, ch07, stale ch01) | Clean/refresh | OPEN |
| E6 | MINOR | Empty `code/src/__init__.py`, `code/tests/` | Build or drop the "shared package" claim | OPEN (human decision) |

## F. Stale reports (regenerate; do not trust)

| # | Issue | Action | Status |
|---|-------|--------|--------|
| F1 | `docs/STATUS.md` marks ch08–14 "Draft: No" (false) | Regenerate | OPEN |
| F2 | `docs/quality/bibliography-audit.md` says "no duplicates" (false) | Re-run `/audit-bibliography` | OPEN |

## Human decisions required (do not auto-apply)

- **Reorder `\include`?** ch16's introductory placement (A15) and any SHAP/calibration
  reorder — the system prefers back-references; escalate only if no lighter fix works.
- **Delete stale `.bib` files** (D7) and **empty `code/src`/tests** (E6).
- **External verification** of working-paper numerics across ch08/09/10/11/12/13/07
  (BloombergGPT totals, KirtacGermano Sharpe 3.05, FinanceBench %, Hampole 2%/14%,
  `chen2025aml`, `kang2023hallucination`) — see `CITATION_DESCRIPTION_AUDIT.md` §4. Never assert until checked.
- **`valuation_example` numbers** — confirm current `results/` values before quoting in ch05.

## Counts

- Audited chapters: **16/16**; passing: **0/16**.
- Backlog items: **~56** (BLOCKER **10**, MAJOR **~33**, MINOR **~13**).
