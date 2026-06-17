# Peer Review — Chapter 13: LLM Limitations and Rigorous Evaluation in Finance

**Manuscript:** `book/chapters/13-llm-limitations-evaluation/chapter.tex`
**Date:** 2026-05-31
**Reviewer:** Anonymous

---

## Summary

This chapter addresses five interconnected evaluation challenges for LLMs in finance: probabilistic calibration, temporal leakage, the empirical track record on stock prediction, economic evaluation metrics, and hallucination. The treatment is systematic, clearly motivated, and well-grounded in the relevant literature. The chapter would make a valuable contribution to any advanced course on AI in finance.

---

## Significance

**Rating: Strong.** The subject matter is timely and practically important. The finance literature has produced many empirical papers on LLM forecasting performance that suffer from the exact methodological failures described here — temporal leakage, lack of transaction cost adjustment, and absence of calibration measurement. Consolidating these failure modes into a single chapter with formal definitions, worked examples, and grounding in market microstructure theory (Grossman-Stiglitz) is genuinely useful for students and practitioners alike. The synthesis of the contamination literature (Ziemke 2024, Lopez-Lira et al. 2025, Gao et al. 2025) is particularly strong and not found together in a single pedagogical treatment elsewhere.

---

## Technical Correctness

**Rating: Acceptable with required corrections.**

1. **ECE arithmetic error (Section 1.1, Example 1):** The weight for Bin 1 is printed as `0.012` in the intermediate calculation line, whereas it should be `0.120` ($= 120/1000$). The final numerical answer (0.115) is coincidentally correct because the gap term for Bin 1 (0.03) multiplied by either value is small, but the intermediate step as printed is wrong. This must be corrected.

2. **Incorrect citation for Fama-French factors (Section 4.1):** Equation (eq:ch13-factor-alpha) presents the Fama-French three-factor alpha regression with SMB and HML, but the supporting citation is `\cite{fama1970efficient}` — the 1970 Efficient Market Hypothesis paper by Fama. The correct citation is Fama and French (1993), "Common Risk Factors in the Returns on Stocks and Bonds." This is a factual bibliographic error that must be corrected.

3. **Conformal prediction and non-exchangeability (Section 1.3):** The chapter states that conformal prediction provides coverage guarantees "under mild exchangeability assumptions" without noting that financial return series are serially correlated and therefore non-exchangeable. In practice, the coverage guarantees presented apply in expectation over exchangeable sequences. For non-stationary financial data, extensions such as SPCI (Xu and Xie, 2023) or rolling conformal methods are needed. The current text may leave readers with a false sense of security about coverage guarantees in live financial applications. At minimum, a caveat sentence is required.

4. **Walk-forward definition (Definition 2):** The expression $\mathcal{D}_\text{eval}^{(k)} = \{(x_t, y_t) : kh \leq t \leq (k+1)h - 1\}$ is ambiguous. If $h$ is a real-valued horizon length and $t$ indexes discrete periods, then "$-1$" is ambiguous. Clarifying that $t$ is a discrete integer index and $h$ is measured in periods would resolve this.

---

## Exposition Quality

**Rating: Good, with one structural gap.**

The prose is clear, professional, and well-suited to the mixed academic-practitioner audience. The learning objectives are well-specified, the chapter follows them faithfully, and the summary section is one of the better summary sections in the manuscript — it concisely restates the five failure modes and their methodological remedies without being repetitive.

The worked examples are well-chosen: the ECE credit classifier (Example 1) makes the abstraction concrete with a domain-relevant scenario, and the contamination audit (Example 2) is one of the best-executed examples in the book, making the quantitative stakes of leakage tangible.

Three exposition concerns:

1. **Missing exercises:** Every other chapter in the manuscript includes end-of-chapter exercises at `[B]` (beginner), `[I]` (intermediate), and `[A]` (advanced) difficulty levels. Chapter 13 has none. Given the centrality of these topics to applied practice, exercises would substantially enhance the chapter's pedagogical value. At minimum: (B) compute ECE from a calibration table, (I) design a contamination-resistant evaluation protocol for a given dataset, (A) implement and compare walk-forward validation with and without purge periods on a real financial time series.

2. **Subsection title:** The heading "Empirical Evidence: LLMs Achieve 51--65% Accuracy on 250 Stocks" is more suitable for a popular press article than an academic textbook. The "250 stocks" figure refers to a single study and should not appear in a section title that covers the broader empirical landscape. Recommend neutral title: "Empirical Evidence on LLM Directional Accuracy."

3. **Prompt sensitivity:** Section 1.3 briefly mentions that verbalized confidence is unstable across prompt templates but does not develop this point. Prompt sensitivity is a distinct and important evaluation fragility — two evaluators using different prompt formats can reach different conclusions about model capability — and deserves at least a paragraph noting that evaluation protocols should specify and fix the prompt template.

---

## Exercise Quality

**Rating: Not applicable — no exercises present.** This is a required revision (see above).

---

## Verdict: MINOR_REVISION

The chapter is technically sound, well-organized, and makes a genuine contribution to the teaching literature on LLM evaluation in finance. Two factual errors (ECE arithmetic, wrong citation) and one structural omission (missing exercises) must be corrected before publication. The remaining issues are editorial. The chapter is close to publication-ready and does not require fundamental restructuring.

### Required Before Acceptance

1. Correct ECE arithmetic on line 118 (`0.012` → `0.12`).
2. Replace `\cite{fama1970efficient}` with `\cite{fama1993common}` in eq:ch13-factor-alpha.
3. Add end-of-chapter exercises at `[B]`, `[I]`, `[A]` difficulty.

### Recommended

4. Add exchangeability caveat to conformal prediction discussion.
5. Rename subsection 3.2 to remove the newspaper-headline tone.
6. Expand prompt sensitivity discussion to a full paragraph.
7. Standardise notation $\bar{p}_m$ vs $\bar{p}(B_m)$ throughout Section 1.1.
8. Add SR 11-7 footnote on first use.
