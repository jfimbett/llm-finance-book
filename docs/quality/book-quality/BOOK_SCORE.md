# BOOK_SCORE.md — Aggregate Quality Scorecard

> Status: **ALL 16 CHAPTERS PASS** (re-scored 2026-06-20 after the release-quality pass).
> Every chapter was independently re-audited at **≥90 on every applicable dimension**, and
> all book-level gates are green. Target met. See `GOAL_STATUS.md`.

## Headline

- **16 / 16 chapters fully pass** (all 14 dimensions ≥90), each **independently re-audited**
  post-fix: ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13,
  ch14, ch15, ch16.
- **Book compiles clean** (628 pp): 0 duplicate labels, 0 multiply-defined, 0 undefined
  refs, 0 undefined citations, 0 biber-missing entries, 0 fatal errors.

## Chapter pass table (reading order)

| Read# | Chapter | Pass | What closed the last gaps |
|-------|---------|------|---------------------------|
| 1 | 01-intro | ✅ | deterministic TF-IDF figure + 3 API listings (LO8) + hedge + SSOT dedup |
| 2 | 16-ai-ml-finance-text | ✅ | dup-key/hygiene/notation/correctness fixes (code_figure n/a) |
| 3 | 02-llm-foundations | ✅ | deterministic PE-figure generator + real demo + self-checks + hedge |
| 4 | 03-llm-training-finetuning | ✅ | hedge LopezLiraTang Sharpe + GPT-4→ChatGPT |
| 5 | 08-domain-specific-llms | ✅ | deterministic corpus figure + hedge + complete shah2022flue entry |
| 6 | 04-llm-agents | ✅ | hedge 3 working-paper numerics + SPLADE bridge |
| 7 | 09-financial-nlp-sentiment | ✅ | deterministic LM-lexicon figure + real demo + hedge + dedup |
| 8 | 14-financial-text-summarization | ✅ | dual-mode boxes + FINER fix + hedge 2 numerics |
| 9 | 05-business-valuation | ✅ | WACC/CAPM + valuation_example + deterministic DCF figure |
| 10 | 06-credit-risk | ✅ | KS-eq fix + deepdive boxes + notebook UTF-8 fix + fairness metric |
| 11 | 10-portfolio-quant-trading | ✅ | Almgren-Chriss/MinTRL fixes + deterministic frontier figure + hedge |
| 12 | 11-regtech-compliance-aml | ✅ | RRF figure + real demo + reframe AMI off unverifiable chen2025aml |
| 13 | 12-xai-explainability | ✅ | deterministic SHAP figure + real demo + IG citation + ordering |
| 14 | 13-llm-limitations-evaluation | ✅ | reliability-diagram figure + hedge + concept-ordering + \Cref |
| 15 | 07-applications-future | ✅ | correctness + deepdive + benchmark figure + hedge + exercises |
| 16 | 15-privacy-local-models | ✅ | DP privacy-utility figure + hedge + residual-risk note |

## The passing recipe (proven on every chapter)

1. **Deterministic, network-free figure generators** (`gen_*.py`, matplotlib `Agg`) +
   real runnable `demo.ipynb` → `code_figure_correctness` + `reproducibility` ≥90.
   Six new generators authored (ch01 TF-IDF, ch02 PE, ch05 DCF, ch07 benchmarks,
   ch08 corpus, ch09 LM-lexicon, ch10 frontier, ch11 RRF, ch12 SHAP, ch13 reliability,
   ch15 DP); all wired into `run_illustrations.sh`.
2. **Hedge unverified working-paper point-numerics** to attributed-qualitative claims
   (never assert unverifiable numbers) → `citation_accuracy` cleared of its ≤89 cap.
3. **Single-source-of-truth** fixes: dup labels collapsed + `\Cref` reminders;
   deepdive/context layering; SSOT bridges → `non_repetition`, `concept_separation`,
   `notation_crossref`.
4. Targeted **content lifts**: WACC/CAPM derivation, fairness metric, self-check
   exercises, inline API listings, missing definitions.

## Book-level gates

| Gate | Status |
|------|--------|
| All chapters pass (≥90 on all dims) | ✅ 16/16 |
| Book compiles | ✅ (628 pp, `-shell-escape` for minted) |
| No duplicate labels | ✅ |
| No broken refs | ✅ |
| No unresolved cites | ✅ |
| No known wrong-paper citations | ✅ (C1–C5 fixed) |
| No unnecessary repeated derivations | ✅ (SSOT + `\Cref`) |
| No orphaned finance examples | ✅ (`valuation_example` wired into ch05) |

**Book pass: YES.**
