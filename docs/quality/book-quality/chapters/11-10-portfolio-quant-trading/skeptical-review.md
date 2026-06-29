# Skeptical Review — Ch. 10 Portfolio Optimization & Quantitative Trading

Format: `SEVERITY · dimension_key · file:line — issue`. Scope tagged local / book-wide.
Audit date 2026-06-20 · **AUDIT ONLY**.

## BLOCKER

- `BLOCKER · notation_crossref · chapter.tex:923 — [local]` Hard-coded prose chapter
  reference "should consult Chapter~7 on regulatory compliance". Rubric §5 forbids
  hard-coded "Chapter N" prose; must be `\Cref{ch:...}`. **Worse, the number is wrong**:
  regulatory compliance is `\label{ch:regtech-compliance-aml}` (folder 11, reading index
  12), not ch07 (`ch:applications-future`, "Other Applications & Future Trends"). This is
  simultaneously a `correctness`/`completeness` defect (points the reader to the wrong
  chapter).
- `BLOCKER · correctness · chapter.tex:923 — [local]` Same line: misattributes the
  regulatory-compliance material to Chapter 7. The reader following this pointer lands on
  the wrong chapter.

## MAJOR

- `MAJOR · citation_accuracy · chapter.tex:439-442 — [citation]` KirtacGermano2024:
  claims 965,375 news articles, 74.4% next-day directional accuracy, and a post-cost
  Sharpe of **3.05**. A Sharpe of 3.05 net of costs is an extraordinary figure; the source
  is an SSRN working paper (#4706629) not verifiable locally. → `NEEDS_EXTERNAL_VERIFICATION`
  (caps citation_accuracy at 89).
- `MAJOR · citation_accuracy · chapter.tex:501-506 — [citation]` CoriatBenhamou2025
  (HARLF): "26% annualised return with a Sharpe ratio of 1.2" on 2018–2024 data. SSRN
  #5365047, unverifiable locally. → `NEEDS_EXTERNAL_VERIFICATION`.
- `MAJOR · citation_accuracy · chapter.tex:158-166 — [citation]` MantshimuliMwamba2025:
  "significantly improves both the Sharpe ratio and annualised return over single-LLM and
  market-cap benchmarks." SSRN #5394743, unverifiable. → `NEEDS_EXTERNAL_VERIFICATION`.
- `MAJOR · citation_accuracy · chapter.tex:201-207 — [citation]` LopezLiraTang2023:
  described as GPT sentiment with "statistically significant coefficients … small
  magnitudes … limited economic significance after costs." SSRN #4412788, unverifiable
  locally. → `NEEDS_EXTERNAL_VERIFICATION`.
- `MAJOR · reproducibility · code/notebooks/10-portfolio-quant-trading/demo.ipynb — [code-figure]`
  `demo.ipynb` is a stub: it imports numpy/pandas and prints "Chapter 10 demo notebook".
  None of the chapter's quantitative content (mean-variance, BL posterior, walk-forward
  backtest, CVaR/GARCH, transaction-cost model) is demonstrated or regenerable. Notebook
  is a placeholder, which the rubric scores 0 for "notebooks are placeholders."
- `MAJOR · reproducibility · book/chapters/10-portfolio-quant-trading/figures/ — [code-figure]`
  Figures directory contains only `.gitkeep`; chapter has **no** `\includegraphics`. No
  efficient-frontier plot, no backtest equity curve, no signal-decay figure — all natural
  candidates. Not a contradiction (no figure claims), but completeness/pedagogy suffer.

## MINOR

- `MINOR · code_figure_correctness · chapter.tex (whole) — [code-figure]` Chapter contains
  no figures and no in-text code; all numeric content is in worked examples and inline
  arithmetic. Dim 3 is scored on the correctness of those worked numbers (all internally
  consistent), not null. The turnover-cost arithmetic at line 640 (`0.15 × 252 × 0.05% ≈
  1.89%`) checks out (= 1.89%). The IR computation at 327-328 (corr 0.08, T=800) is
  plausible/illustrative.
- `MINOR · finance_examples · chapter.tex:323-328 — [finance-example]` Example 10.2 states
  a 0.08 signal–return correlation is "statistically significant in a T=800 sample" and a
  "Sharpe 15% above equal-weight before costs." These are *illustrative* numbers presented
  in the indicative mood; add a one-clause "illustrative" qualifier so a reader does not
  cite them as empirical results.
- `MINOR · correctness · chapter.tex:609-610 — [local]` "a backtest Sharpe above 1.5 on at
  least three years OOS is a reasonable threshold for proceeding to paper trading" is a
  rule-of-thumb stated as such — acceptable, but uncited; consider attributing or softening.
- `MINOR · notation_crossref · chapter.tex:747-748 — [local]` Helpful parenthetical that
  $\varphi_1$ (ARCH coeff) is "not to be confused with the CVaR confidence level $\alpha$."
  Good catch, but $\alpha$ is reused across the chapter (scaling constant in Eq.
  ch10-signal-to-view line 283; CVaR confidence line 719; significance level in Eq.
  ch10-min-track line 692). Three distinct meanings of $\alpha$ — acceptable but worth a
  notation note.
- `MINOR · completeness · chapter.tex:735-744 — [local]` The GARCH(1,1) augmentation adds
  $\kappa v_{t-1}$ linearly to the conditional-variance recursion; the chapter does not
  note that this can yield negative $\sigma_t^2$ if $\kappa<0$ or $v$ is signed. A
  one-line non-negativity caveat would complete the model.

## NIT

- `NIT · pedagogy · chapter.tex:4-20 — [local]` Learning Objectives use a `remark`
  environment (rubric §5: no dedicated objectives box exists, so `remark` is the correct
  choice). Fine. No action.
- `NIT · concept_separation · chapter.tex (whole) — [local]` Chapter uses `definition`,
  `example`, `remark` boxes well but **no** `context`/`deepdive` split. Big-picture vs
  under-the-hood separation is achieved through prose section structure rather than the
  rubric's preferred `context`/`deepdive` boxes. Readable, but not the §5 pattern.

## Book-wide

- `MINOR · notation_crossref · — [book-wide]` Hard-coded "Chapter~N" prose-reference
  pattern (here line 923) — audit other chapters for the same anti-pattern and the
  wrong-target risk it carries.
- `MAJOR · reproducibility · — [book-wide]` Stub `demo.ipynb` (print-only) — likely
  replicated across chapter notebooks; book-wide notebook-realness audit warranted.
- `MAJOR · citation_accuracy · — [book-wide]` Heavy reliance on 2024–2025 SSRN working
  papers with headline performance numbers (Sharpe 3.05, 26%/1.2) across the applied
  chapters; a single external-verification pass over all SSRN-sourced quantitative claims
  is needed before any of these dimensions can exceed 89.
