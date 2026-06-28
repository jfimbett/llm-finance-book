# Hallucination Audit Report — Chapter 11: RegTech, Compliance, and Anti-Money Laundering

**Verdict:** HALLUCINATIONS FOUND (1 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section~\ref{sec:ch11-xbrl-tagging} (XBRL tagging and automated filing), paragraph beginning "The challenge is the size of the taxonomy space."
- **Quoted text:** "The US GAAP taxonomy contains over 20,000 elements."
- **Why flagged:** A specific quantitative claim about the size of a real, externally published artifact (the FASB US GAAP Financial Reporting Taxonomy) presented as established fact with no `\cite{}` key. The element count is a versioned figure sourced from FASB releases; the bare "over 20,000" implies a specific source that is absent. It is not a generic placeholder, an illustrative example block, or a standard textbook stylized fact.
- **Recommended action:** Add a citation to the relevant FASB/SEC taxonomy release, or soften and frame as approximate ("on the order of tens of thousands of elements") to remove the implied precise source.

---

## Code Hallucinations

None. (No notebook exists for this chapter.)

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec 11 (XBRL tagging) | LOW |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

**Notes on claims deliberately NOT flagged:**
- The FATF 2%–5% / \$800B–\$2T laundering estimate, the 95%–99% AML false-positive range, the SR~11-7 verbatim model definition, and the FSB "challenges for existing model risk management frameworks" quote all carry `\cite{}` keys (`fatf2021aml`, `fincen2020aml`, `sr117`, `FSB2024stability`) and are exempt.
- Real, correctly-named regulations and provisions (EU AI Act / Regulation (EU) 2024/1689, MiFID II, Basel III IRB, GDPR Articles 5/9/17/22 and 9(2)(g), FATF Recommendation 24, Corporate Transparency Act 2021, SEC XBRL since 2009) are verifiable real instruments, not phantom regulations — no H3.
- Named subjects and figures in `\begin{example}` blocks (Carlos Fernandez-Gutierrez, Meridian Capital Holdings, A.~Petrov score 0.87, seven-year retention, precision<60%/recall<95% thresholds, 200-case samples) are explicitly illustrative and exempt per the "What NOT to Flag" list.
- Design parameters (200–400 token chunks, RRF κ≈60, <30s latency, two-to-four hours per SAR) are hedged/illustrative engineering choices, not factual world-claims implying a source.
