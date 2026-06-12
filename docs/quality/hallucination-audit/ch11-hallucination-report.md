# Hallucination Audit Report — Chapter 11: RegTech, Compliance, and Anti-Money Laundering

**Verdict:** HALLUCINATIONS FOUND (4 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 11.2.1, Definition block, FPR range claim
- **Quoted text:** "In practice, AML screening systems operate with $\mathrm{FPR}$ values between 95\% and 99\%, meaning fewer than one in twenty --- and often fewer than one in a hundred --- flagged alerts correspond to genuine matches~\cite{fincen2020aml}."
- **Why flagged:** The main FPR range (95%–99%) is cited. However, the inline extension "often fewer than one in a hundred" implies FPR > 99%, which goes beyond the cited range without further support. This secondary quantitative claim is embedded within a cited sentence but effectively introduces uncited precision.
- **Severity:** MEDIUM
- **Recommended action:** Remove "and often fewer than one in a hundred" or add a separate citation supporting sub-1% alert precision in high-volume AML operations.

**Finding 2**
- **Location:** Section 11.2, context block
- **Quoted text:** "the global cost of financial crime compliance was estimated at over \$270 billion per year before the advent of widespread AI adoption"
- **Why flagged:** Precise dollar figure (\$270 billion) without any `\cite{}`. The preceding FATF estimate is cited, but this distinct figure has no attribution.
- **Severity:** MEDIUM
- **Recommended action:** Add citation (frequently attributed to LexisNexis Risk Solutions' True Cost of Financial Crime Compliance study). If uncitable, replace with "hundreds of billions of dollars annually."

**Finding 3**
- **Location:** Section 11.2, context block
- **Quoted text:** "Less than 1\% of illicit financial flows are estimated to be seized and frozen globally."
- **Why flagged:** Precise threshold claim ("less than 1%") with no `\cite{}`. The FATF citation in the same paragraph covers GDP-share laundering estimates, not this seizure-rate figure.
- **Severity:** MEDIUM
- **Recommended action:** Add citation (commonly attributed to UNODC reports). If uncitable, soften to "a very small fraction."

---

### H1/H3 — Uncited Enforcement Claim

**Finding 4**
- **Location:** Section 11.2.1, consequences paragraph
- **Quoted text:** "Banks face fines both for failure to detect money laundering and, paradoxically, for generating so many low-quality SARs that regulators cannot process the useful information~\cite{fincen2020aml}."
- **Why flagged:** The claim that fines have been levied specifically for SAR volume/quality (rather than AML programme deficiencies generally) is a legally precise assertion. FinCEN has issued SAR quality guidance, but the current citation may not directly support fines for excessive low-quality SARs as a specific enforcement outcome.
- **Severity:** LOW
- **Recommended action:** Replace with a citation to a specific enforcement action where SAR quality was cited as the cause, or reframe as: "Regulators have specifically criticised institutions for generating excessive low-quality SARs~\cite{fincen2020aml}, and such deficiencies can contribute to broader AML enforcement actions."

---

## Code Hallucinations

No code hallucinations detected. The notebook contains only a markdown title cell and a single stub cell (`# Your code here`).

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 11.2.1, FPR range — "often fewer than one in a hundred" extension | MEDIUM |
| 2 | H1 | Sec 11.2, \$270 billion compliance cost figure (uncited) | MEDIUM |
| 3 | H1 | Sec 11.2, "<1% of illicit flows seized" (uncited) | MEDIUM |
| 4 | H1/H3 | Sec 11.2.1, "fines for generating low-quality SARs" (enforcement claim) | LOW |
