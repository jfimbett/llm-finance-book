# Hallucination Audit — Summary Report

**Date:** 2026-06-12  
**Chapters audited:** 16  
**Chapters with issues:** 14  
**Chapters clean:** 2 (ch08, ch16)

---

## Summary Table

| Chapter | Title                                              | Status       | H-text | H-code |
|---------|----------------------------------------------------|--------------|--------|--------|
| ch01    | Introduction                                       | ISSUES FOUND |   5    |   0    |
| ch02    | LLM Architecture and Practice                     | ISSUES FOUND |   5    |   0    |
| ch03    | Training and Fine-Tuning LLMs                     | ISSUES FOUND |   6    |   0    |
| ch04    | LLM Agents and Finance Applications               | ISSUES FOUND |   8    |   0    |
| ch05    | LLMs for Business Valuation                       | ISSUES FOUND |   4    |   0    |
| ch06    | LLMs for Credit Risk Analysis                     | ISSUES FOUND |   3    |   0    |
| ch07    | Other Applications and Future Trends              | ISSUES FOUND |   4    |   1    |
| ch08    | Domain-Specific LLMs                              | CLEAN        |   0    |   0    |
| ch09    | Financial NLP and Sentiment Analysis              | ISSUES FOUND |   6    |   0    |
| ch10    | Portfolio Optimization and Quantitative Trading   | ISSUES FOUND |   2    |   0    |
| ch11    | RegTech, Compliance, and AML                      | ISSUES FOUND |   4    |   0    |
| ch12    | Explainability and Interpretability               | ISSUES FOUND |   3    |   0    |
| ch13    | LLM Limitations and Rigorous Evaluation           | ISSUES FOUND |   5    |   0    |
| ch14    | Financial Text Summarization and IE               | ISSUES FOUND |   4    |   0    |
| ch15    | Privacy and Local Deployments                     | ISSUES FOUND |   4    |   0    |
| ch16    | AI and ML in Finance: Text                        | CLEAN        |   0    |   0    |

**Totals across all chapters: 63 text hallucinations, 1 code hallucination**

---

## Chapters Requiring Attention

### HIGH severity issues (require fix before release)

| Chapter | Finding | Type |
|---------|---------|------|
| ch01 | API pricing table (H6/H1) — no citation, prices are stale/unverifiable | H6/H1 |
| ch01 | EU AI Act Article 51–52 — wrong or unverified article numbers | H3 |
| ch02 | EU AI Act Annex III attribution for "AI-assisted securities pricing" | H3 |
| ch03 | FinBERT ESG/forward-looking results — not in Yang et al. (2020) | H1 |
| ch03 | Example 3.7 LLaMA-2 results (94.2%, 88.7%, 79.3%) — fabricated precision | H4 |
| ch04 | Example 4.8 Apple 10-K chunk counts + 94% recall — uncited simulation | H1 |
| ch04 | Example 4.9 Apple Q4 2023 pipeline output — real company, no citation | H1/H4 |
| ch04 | MiFID II Article 25 for record-keeping — likely wrong article | H3 |
| ch05 | Coverage rates 90%/75% attributed to "internal experiments" | H1 |
| ch12 | Example `ex:mifid-disclosure` — "0.3% revision rate over first year" | H4 |
| ch13 | `kang2023hallucination` citation — may be phantom; 15–30% figure at risk | H1+H5 |
| ch14 | Example `ex:earnings-gpt4` — 40% / 8% figures, uncited | H1 |
| ch14 | Example `ex:entities-earnings-call` — Microsoft/Nadella figures, uncited | H4 |

### Report paths

- [ch01](ch01-hallucination-report.md)
- [ch02](ch02-hallucination-report.md)
- [ch03](ch03-hallucination-report.md)
- [ch04](ch04-hallucination-report.md)
- [ch05](ch05-hallucination-report.md)
- [ch06](ch06-hallucination-report.md)
- [ch07](ch07-hallucination-report.md)
- [ch09](ch09-hallucination-report.md)
- [ch10](ch10-hallucination-report.md)
- [ch11](ch11-hallucination-report.md)
- [ch12](ch12-hallucination-report.md)
- [ch13](ch13-hallucination-report.md)
- [ch14](ch14-hallucination-report.md)
- [ch15](ch15-hallucination-report.md)

---

## Clean Chapters

- **ch08** — Domain-Specific LLMs: all numeric claims carry `\cite{}` keys or are scoped to explicitly labelled example blocks; notebook is a stub.
- **ch16** — AI and ML in Finance: Text: all numeric claims cite sources or are textbook stylized facts; example figures are clearly framed as illustrative.

---

## Recurring Patterns

The following issue types appear across multiple chapters and likely reflect systematic drafting practices rather than isolated oversights:

1. **Uncited API pricing/latency tables** (ch01, ch02, ch05): Specific dollar and millisecond figures for commercial APIs with no provider citations. All such tables should cite provider pricing pages with an access date.

2. **EU AI Act Annex III overreach** (ch01, ch02): The chapter text extends Annex III's scope to financial applications (securities pricing, algorithmic trading) that are not explicitly listed. All EU AI Act references should be verified against the final OJ text of Regulation (EU) 2024/1689.

3. **MiFID II article misidentification** (ch03, ch04, ch07, ch15): Multiple chapters cite incorrect or uncited MiFID II article numbers. All MiFID II article references should be audited against the final directive text and its delegated acts.

4. **"Internal experiment" statistics** (ch03, ch04, ch05): Performance figures in example blocks labelled as experimental outcomes without a citation or explicit "hypothetical" label. All such figures must either cite a paper or be reframed as illustrative.

5. **Real company examples without citations** (ch05, ch14): Named public companies (Apple, Microsoft) appear with specific financial figures in example blocks that do not cite the underlying filing or transcript.
