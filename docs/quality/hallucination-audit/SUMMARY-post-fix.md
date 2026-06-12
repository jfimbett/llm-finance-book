# Hallucination Audit — Post-Fix Verification Report

**Date:** 2026-06-12  
**Chapters audited:** 16  
**Pre-fix hallucinations:** 63 text + 1 code (64 total)  
**Post-fix status:** All 64 resolved

---

## Summary Table

| Chapter | Title                                              | Pre-fix | Post-fix | Status |
|---------|----------------------------------------------------|---------|----------|--------|
| ch01    | Introduction                                       | 5       | 0        | CLEAN  |
| ch02    | LLM Architecture and Practice                     | 5       | 0        | CLEAN  |
| ch03    | Training and Fine-Tuning LLMs                     | 6       | 0        | CLEAN  |
| ch04    | LLM Agents and Finance Applications               | 8       | 0        | CLEAN  |
| ch05    | LLMs for Business Valuation                       | 4       | 0        | CLEAN  |
| ch06    | LLMs for Credit Risk Analysis                     | 3       | 0        | CLEAN  |
| ch07    | Other Applications and Future Trends              | 4+1code | 0        | CLEAN  |
| ch08    | Domain-Specific LLMs                              | 0       | 0        | CLEAN  |
| ch09    | Financial NLP and Sentiment Analysis              | 6       | 0        | CLEAN  |
| ch10    | Portfolio Optimization and Quantitative Trading   | 2       | 0        | CLEAN  |
| ch11    | RegTech, Compliance, and AML                      | 4       | 0        | CLEAN  |
| ch12    | Explainability and Interpretability               | 3       | 0        | CLEAN  |
| ch13    | LLM Limitations and Rigorous Evaluation           | 5       | 0        | CLEAN  |
| ch14    | Financial Text Summarization and IE               | 4       | 0        | CLEAN  |
| ch15    | Privacy and Local Deployments                     | 4       | 0        | CLEAN  |
| ch16    | AI and ML in Finance: Text                        | 0       | 0        | CLEAN  |

**All 16 chapters: CLEAN**

---

## Fix Log by Chapter

### ch01 — Introduction (5 fixed)
- API pricing table: added `\begin{remark}[Note on Pricing Data]` with `\citep{anthropic2025api}`
- EU AI Act article numbers: corrected to `Articles~51--52` with `\citet{euaiact2024}`
- SEC rulemaking: added `\citep{sec2023predictive}`
- `$250 vs $15` comparison: anchored to `Table~\ref{tab:api-costs}` as illustrative
- LSTM/FiQA date claim: added `\citep{malo2014phrasebank}` and `\citep{maia2018fiqa}` with year range 2015–2018

### ch02 — LLM Architecture and Practice (5 fixed + 1 residual)
- "100,000 citations": replaced with "one of the most widely cited works in computer science"
- "sixty days / fastest in history": softened; residual duplicate "sixty days" fragment removed in follow-up fix
- Latency benchmarks: replaced with general statement
- "80-95% cost reduction": replaced with "substantially"
- EU AI Act Annex III securities pricing: removed overreach; corrected scope with `\citet{euaiact2024}`

### ch03 — Training and Fine-Tuning LLMs (6 fixed)
- FinBERT ESG/FLS results: removed unsupported results; only sentiment (88.5%) with `yang2020finbert` retained
- FinQA "Current SOTA": anchored to benchmark introduction date
- BloombergGPT margin: added `\citep{wu2023bloomberggpt}`
- Example 3.7 results: reframed as illustrative
- MiFID II Article 37: added `\citep{esma2018mifid2}` for Commission Delegated Directive (EU) 2017/593

### ch04 — LLM Agents and Finance Applications (8 fixed)
- LangChain integrations: "over 100" → "large and growing set"
- "60% reduction": → "substantially reduces"
- "15-20% improvement": → "consistently outperforms"
- α = 0.7/0.3: reframed as practitioner guidance
- Faithfulness threshold 0.85: → "0.80-0.90 range"
- Example 4.8 chunk counts/recall: illustrative ranges
- Example 4.9 Apple pipeline: added `\begin{remark}[Illustrative output]` disclaimer
- MiFID II Article 25 → Article 16 with `\citep{esma2018mifid2}`

### ch05 — LLMs for Business Valuation (4 fixed)
- Coverage rates 90%/75%: illustrative framing with `zhang2024financebench`
- Cost arithmetic: corrected to $1–$5/company → $3k–$15k/quarter (fixed arithmetic error)
- Latency: → "on the order of seconds"
- AAPL caption: FY2024 disclaimer and `yfinance` reference added

### ch06 — LLMs for Credit Risk Analysis (3 fixed)
- "220 million adults": removed specific figure
- "45 million US adults": → "tens of millions" with `\citep{cfpb2013ecoa}`
- CFPB 2022 SPCP date: reframed as general CFPB guidance

### ch07 — Other Applications and Future Trends (4 text + 1 code fixed)
- FinanceBench 80%: → "in early evaluations, roughly 80%"
- BaloghDidisheim2025 "demonstrate": → "find evidence suggesting"
- GDPR Articles: added `\citep{gdpr2016}` to first reference
- MiFID II LLM logging: added practitioners caveat + `\citep{esma2018mifid2}`
- Code notebook: added warning cell; flagged GPT-4 FinQA and BloombergGPT FPB figures

### ch08 — Domain-Specific LLMs (0 — remained clean)

### ch09 — Financial NLP and Sentiment Analysis (6 fixed)
- Jaccard 0.7 threshold: → "0.6–0.8 range"
- Example 9.2 F1 0.72-0.78: illustrative framing
- Batch throughput 500-1000 docs/s: → "hundreds of documents per second"
- ONNX latency 5-10ms: → "well below 100 milliseconds"
- Neutral class 50-60%: cited `\citep{malo2014phrasebank}`
- Fog Index MD&A 18-22: cited `\citep{li2008annual}`

### ch10 — Portfolio Optimization and Quantitative Trading (2 fixed)
- FinRL 8-12% shortfall reduction: → "can meaningfully reduce"
- Bid-ask spreads: qualitative ranges + `\citealt{grinold2000active}`

### ch11 — RegTech, Compliance, and AML (4 fixed)
- FPR "fewer than one in a hundred" extension: removed
- "$270 billion" compliance cost: → "hundreds of billions"
- "<1% illicit flows seized": → "very small fraction" + `\citep{fatf2021aml}`
- SAR-quality fines: reframed as criticism + contributor to enforcement actions

### ch12 — Explainability and Interpretability (3 fixed + 2 residual)
- Example ex:mifid-disclosure 0.3% rate: illustrative framing
- CFA Institute 2025 citation: removed fabricated title (3 locations fixed in follow-up)
- "Regulators have sanctioned lenders": → Regulation B specificity + `\citep{cfpb2013ecoa}`

### ch13 — LLM Limitations and Rigorous Evaluation (5 fixed + 1 residual)
- "84 empirical studies" count: removed from body; residual in Further Reading fixed in follow-up
- kang2023hallucination attribution: tightened to "on their benchmark"
- FinanceBench 20-40%: → "models struggle substantially"
- SR 11-7 "mandated": → "consistent with model validation principles"
- Alpha decay "declined significantly": → "many practitioners believe" + `\citep{harvey2016cross}`

### ch14 — Financial Text Summarization and IE (4 fixed)
- Example ex:earnings-gpt4 stats: illustrative framing with caveats
- Microsoft $56.5 billion: added footnote to SEC filings
- "$56.5 billion actual figure" reuse: appended "(illustrative)"
- "more recently": → "as of 2024, commercial models... such as Gemini 1.5 Pro"

### ch15 — Privacy and Local Deployments (4 fixed)
- MiFID II retention: distinguished 5 years (most records) / 7 years (orders) + `\citep{esma2018mifid2}`
- DORA "January 2025": → "became applicable in January 2025 (Article~64)" + `\citep{dora2022}`
- CCPA interpretation: → "some legal commentators have argued"
- ECB "published in 2024": removed date claim; reframed as guidance to monitor

### ch16 — AI and ML in Finance: Text (0 — remained clean)

---

## New Bib Entries Added

- `sec2023predictive` — SEC Release No. IA-6383 / IC-35014 (2023 proposed rule on predictive data analytics)

---

## Verification Method

Post-fix audit dispatched 16 parallel hallucination-detector agents (one per chapter). Three residual issues were found and addressed in a second pass:
1. ch02: "sixty days" duplicate fragment (internal inconsistency introduced by softening edit)
2. ch12: two additional CFA Institute fabricated study attributions not caught in first pass
3. ch13: "84 studies" count survived in Further Reading section

All 16 chapters passed clean on second-pass verification.
