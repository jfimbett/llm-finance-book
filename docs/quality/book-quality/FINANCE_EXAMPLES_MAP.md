# FINANCE_EXAMPLES_MAP.md

> Inventory of finance examples, their grounding, and integration status. Drives
> `RUBRIC.md` dims 7 (`finance_orientation`) and 8 (`finance_examples`).
> **Status: VERIFIED across all 16 chapters (2026-06-20 full audit).**

| Example | Chapter (read#) | Finance area | Grounded? | Integration | Notes |
|---------|-----------------|--------------|-----------|-------------|-------|
| **AAPL DCF+comps valuation USING Claude** | `exercises/valuation_example/` | Equity valuation | **Yes — complete, passing** ($225.00 vs $226.84) | **ORPHANED** | `grep -rn valuation_example book/` = 0 hits; supplies the CAPM r_E≈9.48% / WACC≈9.27% ch05 lacks → **integrate (backlog #19)** |
| Stylised SaaS DCF case study | ch05 (#9) | Valuation | No (composite/synthetic) | Inline flagship | replace/pair with the real AAPL exercise |
| AAPL DCF sensitivity heatmap | ch05 (#9) | Valuation | Yes (yfinance) | `fig:ch05-illustration` | best grounded example in ch05; FCF $98.8B vs exercise $108.8B (reconcile) |
| Tetlock WSJ negativity → DJIA | ch01/ch09/ch16 | Sentiment | Yes | repeated 3× | **SSOT = ch01** (read#1); others `\Cref` |
| Loughran–McDonald 10-K sentiment | ch01/ch08/ch09/ch16 | Sentiment | Yes | repeated | founding result SSOT = ch01; FinBERT/domain SSOT = ch08 |
| EDGAR 10-K text-growth | ch01 (#1) | Filings | Yes (cached) | `fig:edgar-text-growth` | live SEC fetch + hard-coded UA (reproducibility) |
| Two-agent EPS beat/miss extractor | ch04 (#6) | Earnings | Partial (notebook stub) | demo.ipynb stub | strong concept; code not runnable |
| Multi-agent equity research (5 agents) | ch04 (#6) | Research | Partial (conceptual) | inline | — |
| Tesla 10-K liquidity ReAct trace | ch04 (#6) | Filings | Yes (illustrative) | inline | pedagogically excellent |
| BloombergGPT / FinBERT benchmarks | ch08 (#5) | Domain LLMs | Numbers NEEDS_EXTERNAL_VERIFICATION | inline | finance_examples 88 — illustrative not reproducible |
| GameStop/WSB, SVB bank-run | ch09 (#7) | Sentiment/risk | Yes | event studies | — |
| Black–Litterman on 100 S&P 500 firms | ch10 (#11) | Portfolio | Yes (illustrative) | inline | not regenerable (demo stub) |
| 8-K SEC-investigation position cut | ch10 (#11) | Trading/risk | Yes | verbatim JSON | — |
| AML adverse-media / UBO chains | ch11 (#12) | Compliance/AML | Yes (illustrative) | inline | strong; AMI cites suspicious `chen2025aml` |
| Hybrid credit pipeline (GBT+BERT+GPT-4o) | ch12 (#13) | Credit/XAI | Yes | SHAP adverse action | strong; SHAP re-derived vs ch06 |
| Apple Card gender-bias; constrained-decoding PD | ch06 (#10) | Credit/fairness | Yes | inline + grammar | — |
| ECE on credit classifier (0.115) | ch13 (#14) | Credit/eval | Yes | worked | verified |
| Microsoft Q3-2023 earnings NER; ECTSum | ch14 (#8) | Earnings/summ | Yes | inline | FINER-139 misattributed (citation) |
| French mortgage NER de-identification; DP/FedAvg | ch15 (#16) | Privacy | Yes | inline | math verified vs Dwork–Roth |

## Finance orientation by chapter (all 16 — consistently strong)

| Read# | Chapter | finance_orientation | finance_examples |
|-------|---------|---------------------|------------------|
| 1 | 01-intro | 92 | 90 |
| 2 | 16-ai-ml | 93 | 91 |
| 3 | 02-foundations | 92 | 91 |
| 4 | 03-training | 93 | 92 |
| 5 | 08-domain | 93 | 88 |
| 6 | 04-agents | 93 | 90 |
| 7 | 09-nlp-sentiment | 93 | 90 |
| 8 | 14-summarization | 94 | 92 |
| 9 | 05-valuation | **86** | **72** |
| 10 | 06-credit | 93 | 88 |
| 11 | 10-portfolio | 93 | 87 |
| 12 | 11-regtech | 93 | 92 |
| 13 | 12-xai | 93 | 92 |
| 14 | 13-limitations | 93 | 92 |
| 15 | 07-future | 92 | 86 |
| 16 | 15-privacy | 93 | 88 |

**finance_orientation is the book's strongest dimension (book-level 92, the only pass).**
The only soft spot is ch05, where the discount rate (WACC) is asserted, not finance-derived.

## Highest-value integration action

**Wire `exercises/valuation_example/` into ch05** via a single companion-exercise `remark`
box (ch05 plan T1). It is the only orphaned grounded asset and simultaneously closes the
WACC completeness BLOCKER and raises `finance_examples`, `finance_orientation`,
`concept_ordering`, `progressive_learning`, and `reproducibility`. Do **not** paste the
exercise into prose.
