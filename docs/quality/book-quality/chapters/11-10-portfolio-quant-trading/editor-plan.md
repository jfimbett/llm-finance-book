# Editor Plan — Ch. 10 Portfolio Optimization & Quantitative Trading

Reading index 11 · audit date 2026-06-20 · **AUDIT ONLY — no edits applied.**
Targeted, minimal edits. Protect all `KEEP*` content from the constructive review.

## MUST_FIX (blocks pass)

1. **`chapter.tex:923` — wrong + hard-coded chapter reference.** Replace
   "should consult Chapter~7 on regulatory compliance" with a `\Cref{ch:regtech-compliance-aml}`
   reference (the actual regulatory-compliance chapter, reading index 12). Fixes one
   BLOCKER each in `notation_crossref`, `correctness`, and `completeness`.

2. **`demo.ipynb` — replace stub with a real demo.** Implement at minimum: (a) a
   mean-variance efficient-frontier solve on synthetic/sample returns, (b) the
   Black-Litterman posterior from Eq. ch10-bl-posterior reproducing the AAPL example,
   (c) a toy walk-forward backtest with the linear transaction-cost model (Eq.
   ch10-transaction-cost). Seed all randomness. Raises `reproducibility` from placeholder.

## SHOULD_FIX (caps a dimension below 90 until resolved)

3. **citation_accuracy — external verification pass.** Verify against the SSRN sources the
   headline numbers: KirtacGermano2024 (965,375 articles, 74.4%, Sharpe 3.05 — line
   439-442); CoriatBenhamou2025 HARLF (26% / Sharpe 1.2 — line 503-504);
   MantshimuliMwamba2025 (line 158-166); LopezLiraTang2023 magnitudes (line 201-207).
   Until verified, dimension capped at 89 (`NEEDS_EXTERNAL_VERIFICATION`).

4. **`chapter.tex:323-328` (and 327) — label illustrative numbers.** Add an "illustrative"
   qualifier to Example 10.2's 0.08 correlation / 15%-above-EW Sharpe so they are not read
   as empirical findings. Lifts `finance_examples`.

5. **Add at least one figure.** An efficient-frontier plot (sec ch10-markowitz) and/or a
   walk-forward equity curve would materially help `pedagogy` and remove the empty
   `figures/` directory. Generate from the upgraded `demo.ipynb` for reproducibility.

## OPTIONAL (polish)

6. `chapter.tex:735-744` — add a one-line non-negativity caveat to the GARCH+text
   augmentation (guard $\sigma_t^2 \ge 0$).
7. `chapter.tex:747-748` — add a short notation note that $\alpha$ carries three distinct
   meanings (signal-scaling, CVaR confidence, significance level).
8. `chapter.tex:609-610` — attribute or soften the "Sharpe > 1.5 / 3yr OOS" rule of thumb.
9. Consider wrapping the big-picture sections (e.g. ch10-llm-limits, ch10-llm-not-stock-pickers)
   in `context` boxes and the BL/GARCH math in `deepdive` boxes to match rubric §5
   concept-separation pattern (currently achieved via prose only).

## DO_NOT_CHANGE

- Mean-variance derivation (44-109), Black-Litterman derivation (116-185), CVaR/GARCH
  model (718-756) — all single-source-of-truth; do not duplicate or relocate.
- "Where LLMs can/cannot add value" (188-244) and market-efficiency section (509-551) —
  the chapter's analytical spine; preserve tone and structure.
- Worked examples 10.1 (BL AAPL, 168-185), 10.2 (earnings-call, 307-329), 10.3 (8-K alert,
  813-835) — keep; only add illustrative qualifiers per SHOULD_FIX #4.
- Intentional thesis repetition (239-240 ↔ summary 853-856) — cross-referenced
  reinforcement, not redundancy. Keep.

## BOOK_WIDE_ITEMS

- **B1 (notation_crossref):** Sweep all chapters for hard-coded "Chapter~N" prose refs;
  ch10:923 also had the *wrong* number — audit for similar mis-pointers.
- **B2 (reproducibility):** Audit every chapter's `demo.ipynb`; ch10's is a print-only
  stub and the pattern likely repeats book-wide.
- **B3 (citation_accuracy):** Single external-verification pass over all SSRN working-paper
  performance figures cited across the applied chapters (Sharpe/return/accuracy headline
  numbers) before any of those dimensions can exceed 89.
