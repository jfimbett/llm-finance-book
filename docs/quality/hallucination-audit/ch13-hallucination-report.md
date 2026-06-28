# Hallucination Audit Report — Chapter 13: LLM Limitations and Rigorous Evaluation in Finance

**Verdict:** HALLUCINATIONS FOUND (1 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section heading of \Cref{sec:ch13-empirical-evidence-llm-accuracy}, "Empirical Evidence: LLMs Achieve 51--65\% Accuracy on 250 Stocks" (line 491).
- **Quoted text:** "Empirical Evidence: LLMs Achieve 51--65\% Accuracy on 250 Stocks"
- **Why flagged:** The figure "250 Stocks" is a precise, oddly specific quantity presented as an established empirical fact, but it is never supported anywhere in the section body. The body cites \citet{LopezLiraTang2023} (headline sentiment), \citet{VidalSSRN2024} (a sample of S\&P~500 firms), \citet{xu2024stock}, and the \citet{zhao2025frontiers} meta-analysis — none of which is described as covering 250 stocks. The "51--65\%" range is corroborated in the text, but "250 Stocks" is invented specificity with no corresponding study, dataset, or `\cite{}` key. A reader would reasonably infer a concrete 250-stock benchmark that does not exist in the chapter.
- **Recommended action:** Remove the unsupported "on 250 Stocks" from the heading (e.g., "LLMs Achieve 51--65\% Directional Accuracy"), or tie the number to a specific cited study whose sample is genuinely 250 stocks.

---

## Code Hallucinations

None — there is no notebook for this chapter and no embedded code listings.

---

## Notes on Claims Reviewed but NOT Flagged

- All numeric tables and figures in \texttt{Example}/\texttt{example} blocks (the ECE table and 0.115 computation in \Cref{ex:ch13-ece-credit}; the "34 of 500", "62\% to 54\%", "8 percentage points" figures in \Cref{ex:ch13-contamination-audit}) are explicitly illustrative — excluded per the spec.
- "Apple report revenue above \$100 billion in Q4 2022" and "Company X ... approximately \$380 billion" (Sec. \ref{sec:ch13-point-in-time-data}) are framed as a pedagogical illustration of contextual anonymisation, not asserted financials — not flagged.
- Transaction-cost magnitudes ("half-spreads ... 1--3 bps", "5--20 bps", "10--50 bps per day") are hedged with "typically" and are generic practitioner stylized facts — not flagged.
- IR rules of thumb ("IR $>0.5$ strong, $>1.0$ exceptional") and the $\sqrt{252}$ annualisation are standard textbook conventions — not flagged.
- All other precision/empirical claims ("above 62\%", "51--54\%", "exceed 10\%", GPT-4 numerical-error claim, the year-specific-LLM and LAP findings) carry `\cite{}` keys — excluded per the spec.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec 13.3.2 heading (line 491) | MEDIUM |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision
