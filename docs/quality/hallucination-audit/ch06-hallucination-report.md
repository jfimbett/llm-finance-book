# Hallucination Audit Report — Chapter 06: LLMs for Credit Risk Analysis

**Verdict:** HALLUCINATIONS FOUND (3 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 6.1.3 (Preprocessing → Anonymisation), paragraph beginning "Direct identifiers..."
- **Quoted text:** "The canonical result is Sweeney's (2002) finding that 87\% of the US population can be uniquely identified by the combination of ZIP code, date of birth, and sex."
- **Why flagged:** Precise statistic (87\%) attributed to a named author-year ("Sweeney's (2002)") but with no `\cite{}` key. The inline attribution is not a real citation, so the precision implies a source that is absent from the bibliography. (This is a genuine result, but the audit targets the uncited-precision pattern, not factual correctness.)
- **Recommended action:** Add a `\cite{}` to the Sweeney reference (e.g. `\citet{sweeney2002kanonymity}`) or reframe as an approximate, attributed stylized fact.

**Finding 2**
- **Location:** Section 6.3 (Household Decisions Under Uncertainty), opening `\begin{context}` paragraph beginning "In 2018, the Consumer Financial Protection Bureau published a study..."
- **Quoted text:** "...roughly one-third of mortgage borrowers in the United States did not shop for their mortgage... Among low-income borrowers the fraction was closer to one-half. The CFPB estimated that the average borrower who did not shop paid approximately \$300 per year more in interest..."
- **Why flagged:** Specific statistics (one-third, one-half, \$300/year) attributed to a named real institution and a specific dated study ("a 2018 CFPB study") without any `\cite{}` key. The dollar figure and study year imply a precise source that is not given.
- **Recommended action:** Add a `\cite{}` to the specific CFPB study, or reframe the figures as illustrative ("a substantial share of borrowers...").

---

### H4 — Synthetic Real-World Examples

**Finding 3**
- **Location:** Section 6.1 (Credit Data), opening `\begin{context}` paragraph beginning "In 2019 a viral tweet ignited a Congressional investigation."
- **Quoted text:** "...his Apple Card credit limit was twenty times lower than his wife's... Steve Wozniak... posted a similar complaint... Senator Elizabeth Warren had written to Goldman Sachs demanding an explanation, and the New York Department of Financial Services had opened a formal investigation."
- **Why flagged:** A factual narrative making specific claims (a "twenty times" limit ratio, a Warren letter to Goldman Sachs, an NYDFS investigation) about named real individuals and institutions, presented as established fact with no `\cite{}` and no "for illustration" framing. Matches the H4 pattern of named-entity factual claims lacking a citation.
- **Recommended action:** Add a citation to a press/regulatory source for the 2019 Apple Card / Goldman Sachs / NYDFS episode, or soften the specific quantitative/procedural claims.

---

## Code Hallucinations

None. There is no notebook for this chapter. The embedded JSON/API payloads (e.g. `\Cref{ex:api}`, `application_id "APP-20240315-78423"`) and the borrower/SHAP tables appear inside `\begin{example}`/`\begin{illustration}` blocks and are explicitly illustrative, so they are not flagged per the "What NOT to Flag" rule.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec 6.1.3 (Sweeney 87%) | MEDIUM |
| 2 | H1   | Sec 6.3 context (CFPB 2018 study) | MEDIUM |
| 3 | H4   | Sec 6.1 context (Apple Card 2019) | MEDIUM |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

**Notes (considered but NOT flagged):** FICO factor weights (35/30/15/10/10, hedged "publicly disclosed... approximately" — standard publicly disclosed fact); bureau coverage "200--230 million" (explicitly hedged as a "commonly cited range"); KS/Gini/PSI/default-rate thresholds (standard credit stylized facts); all named regulations (FCRA, ECOA, Reg B, GDPR Art. 22/Recital 71, Dodd-Frank §1033, SR 11-7 — genuine, and SR 11-7 carries `\cite{sr117}`); the Maria/Thomas personas and dialogues (explicitly labelled illustrative in `\begin{example}`); the LoRA "~48×" figure (derived from $768^2/(2\cdot8\cdot768)$, not a phantom statistic).
