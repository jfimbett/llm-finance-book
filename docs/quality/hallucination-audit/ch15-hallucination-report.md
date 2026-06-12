# Hallucination Audit Report — Chapter 15: LLMs and Privacy: Local Deployments and Text De-identification

**Verdict:** HALLUCINATIONS FOUND (4 text, 0 code)

---

## Text Hallucinations

### H3 — Invented Regulatory / Legal Claims

**Finding 1**
- **Location:** Section 15.1.2, MiFID II paragraph
- **Quoted text:** "Its record-keeping obligations require investment firms to retain records of all services and transactions for at least five years"
- **Why flagged:** The five-year retention figure is stated as a bare factual claim about MiFID II Article content with no `\cite{}`. The correct baseline under MiFID II is five years for most records and seven years for orders (Article 25(5)). The unqualified "at least five years" without distinction between record types could mislead practitioners.
- **Severity:** MEDIUM
- **Recommended action:** Add `\citep{mifid2014}` or equivalent, and distinguish retention periods by record type: "a minimum retention period of five years for most records, and seven years for orders under Article 25(5) of MiFID II."

**Finding 2**
- **Location:** Section 15.1.2, DORA paragraph
- **Quoted text:** "The Digital Operational Resilience Act (DORA, Regulation 2022/2554) entered into force in January 2025"
- **Why flagged:** Precise entry-into-force date ("January 2025") with `\citep{dora2022}` present. The date (January 17, 2025 application date) goes beyond what a general regulation citation confirms. The cite key should be verified to include the application date, or a footnote added.
- **Severity:** LOW
- **Recommended action:** Verify the cite key's content includes the application date. If not, add a footnote or rephrase as "applicable from January 2025 (Article 64)" with supporting citation.

**Finding 3**
- **Location:** Section 15.1.2, CCPA paragraph
- **Quoted text:** "regulators have interpreted broadly to include some forms of data sharing with third-party model providers"
- **Why flagged:** The claim that CCPA regulators have specifically ruled that sharing data with third-party model providers constitutes a "sale" is presented as established regulatory fact with no `\cite{}`. This is a contested legal interpretation; no California AG or CPPA enforcement action or formal guidance is cited.
- **Severity:** MEDIUM
- **Recommended action:** Add citation to specific CPPA guidance or enforcement, or reframe as "some legal commentators have argued that…" to reflect the interpretive status of the claim.

---

### H6 — Undated "Recent" Claims

**Finding 4**
- **Location:** Section 15.5.2, compliance checklists paragraph
- **Quoted text:** "the ECB's supervisory expectations on AI risk management, published in 2024, and the EBA's work on machine learning in credit risk are examples"
- **Why flagged:** "Published in 2024" for the ECB supervisory expectations is a precise date claim with no `\cite{}`. The EBA reference has no date, document title, or citation. Both are presented as authoritative factual references without citations.
- **Severity:** MEDIUM
- **Recommended action:** Identify and cite the specific ECB supervisory statement and the specific EBA ML in credit risk report. Without citations these function as phantom references.

---

## Code Hallucinations

No code hallucinations detected. The notebook contains a single markdown cell with no code.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H3 | Sec 15.1.2, MiFID II retention period (uncited, five/seven-year distinction absent) | MEDIUM |
| 2 | H3/H6 | Sec 15.1.2, DORA entry-into-force date ("January 2025") | LOW |
| 3 | H3 | Sec 15.1.2, CCPA interpretation re third-party model providers | MEDIUM |
| 4 | H6 | Sec 15.5.2, ECB 2024 AI guidance + EBA ML report (uncited) | MEDIUM |
