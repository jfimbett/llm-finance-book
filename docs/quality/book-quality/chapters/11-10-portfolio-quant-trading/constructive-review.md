# Constructive Review — Ch. 10 Portfolio Optimization & Quantitative Trading

Reading index 11 · slug `10-portfolio-quant-trading` · audit date 2026-06-20 · **AUDIT ONLY**

This chapter is strong: finance-first framing, clean mathematical exposition, and a
consistent thesis ("LLMs are information extractors, not optimizers") that ties the
sections together. Below is what to preserve.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **`chapter.tex:44-109` — Mean-variance / efficient frontier derivation.** Verified that
  mean-variance, Sharpe, and the efficient frontier are *not* derived in ch05 (valuation)
  or ch06 (credit risk). This chapter is the legitimate single source of truth for
  classical portfolio theory. `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **`chapter.tex:116-185` — Black-Litterman derivation (Eq. ch10-bl-pi … ch10-bl-posterior).**
  Posterior-mean formula is the standard BL result; the "no views → market portfolio"
  sanity check (line 147-149) is exactly right. Sole derivation in the book. `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **`chapter.tex:718-756` — CVaR / GARCH(1,1) augmented-volatility model.** CVaR appears
  nowhere else as a derivation (ch13 only mentions GARCH in passing). `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH / GOOD_BIG_PICTURE_EXPLANATION

- **`chapter.tex:188-244` — "Where LLMs Can and Cannot Add Value."** Disciplined,
  honest framing (information vs extraction hypothesis; explicit "where LLMs do not add
  value" list). This is the chapter's spine and the right tone for the mixed audience.
  `GOOD_BIG_PICTURE_EXPLANATION`.
- **`chapter.tex:509-551` — Market-efficiency argument (Grossman-Stiglitz, calibration
  problem).** Correctly separates statistical predictability from economic profitability;
  the crowding/decay argument is well-grounded. `GOOD_BIG_PICTURE_EXPLANATION`.

## GOOD_TECHNICAL_EXPLANATION

- **`chapter.tex:80-100` — Estimation-error discussion + shrinkage/factor remedies.**
  The `\hat\sigma/\sqrt{60}` standard-error intuition (line 82-84) is correct and
  pedagogically valuable. `KEEP`.
- **`chapter.tex:580-594` — Walk-forward evaluation protocol (Def.).** Precise,
  reproducible definition with explicit fold arithmetic. `KEEP`.
- **`chapter.tex:653-698` — Backtesting pitfalls (look-ahead, survivorship, PBO, minimum
  track record length).** The three LLM-specific look-ahead forms (embedding leakage,
  model-selection leakage, timestamp errors) are genuinely insightful and chapter-unique.
  `KEEP`.

## GOOD_FINANCE_EXAMPLE

- **`chapter.tex:168-185` — Single absolute view in Black-Litterman (AAPL).** Concrete,
  numerically grounded, and correctly explains the confidence/posterior-shift relationship.
  `GOOD_FINANCE_EXAMPLE` (numbers are illustrative — flagged in skeptical review only as
  "illustrative, label as such").
- **`chapter.tex:307-329` — Earnings-call BL view extraction example.** Realistic
  pipeline; the 0.08 correlation → IR ≈ 0.25 chain is internally coherent. `GOOD_FINANCE_EXAMPLE`.
- **`chapter.tex:813-835` — 8-K critical-alert example.** Excellent end-to-end illustration
  of the alert pipeline; the closing paragraph (837-842) responsibly states the limitation.
  `GOOD_FINANCE_EXAMPLE`.

## KEEP — citation integration

- The recent SSRN working papers (KirtacGermano2024, MantshimuliMwamba2025,
  CoriatBenhamou2025, Yuksel2025alpha, YukselAlphaQuant2025, MeskovskisKenyon2024,
  SahaLyuEtAl2025, Mann2024) are woven in as empirical anchors rather than dropped as
  name-checks. All keys resolve. `KEEP` (descriptions need external verification — see
  citation_accuracy).

## DO_NOT_CHANGE without care

- The thesis sentence at `chapter.tex:239-240` ("LLMs are information extraction engines,
  not portfolio optimizers") is the through-line repeated (intentionally) in the summary.
  This is *intentional, cross-referenced reinforcement*, not redundancy. `KEEP`.
