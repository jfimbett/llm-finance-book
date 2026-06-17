# Peer Review: Chapter 5 — LLMs for Business Valuation

**Manuscript:** book/chapters/05-business-valuation/chapter.tex  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Verdict:** MINOR_REVISION

---

## Summary

This chapter presents a comprehensive framework for applying large language models to equity valuation workflows, covering data extraction from SEC EDGAR, free-cash-flow computation, chain-of-thought forecasting, tool-augmented arithmetic, scenario analysis, comparable selection, and end-to-end pipeline integration. The scope is ambitious and the execution is largely successful. The chapter would make a valuable contribution to the book and, with the revisions noted below, will serve the target audience well.

---

## 1. Significance

**Score: High**

The chapter addresses a genuinely important and timely problem: translating the general capabilities of LLMs into a rigorous, production-deployable financial workflow. Unlike much of the LLM-in-finance literature, which focuses on sentiment analysis or return prediction, this chapter tackles the harder problem of end-to-end valuation automation. The hybrid comparable-selection pipeline and the first-order error-propagation analysis are methodologically original contributions appropriate for an advanced textbook. The chapter's scope is well-matched to the mixed academic-industry audience of the book.

---

## 2. Technical Correctness

**Score: Mostly correct, one material error**

**2.1 Factual error — enterprise value inconsistency (must fix)**

Example 2.1 (§2.1) states that the illustrative technology firm has an enterprise value of "approximately $15.2B" using FCFF = $713.6M, WACC = 9%, 5-year explicit growth = 8%, terminal growth = 3%. The ReAct trace in Listing 8 (§4.3) uses identical parameters and the Python computation yields EV = $13,346.7M ≈ $13.3B. These two figures are inconsistent. The Python code is verifiable and almost certainly correct; the $15.2B prose claim appears to be an error — possibly from an earlier parameterisation. This must be corrected before publication.

**2.2 FCFF-FCFE proof**

The proof of Proposition 1 is technically correct but telescopes the key algebraic step ("rearranging yields") without showing the substitution. For a textbook proof, the intermediate step should be made explicit.

**2.3 WACC omission**

WACC appears in the DCF formula (Eq. 1), in every numerical example, and in the error-propagation section, but is never estimated or derived. The chapter assumes the reader already knows how to compute WACC, which is inconsistent with the stated learning objectives. At minimum, a boxed remark should direct the reader to standard references (Damodaran's CAPM and WACC derivation) or, preferably, a short subsection should derive the WACC formula and explain how each component is estimated.

**2.4 Partial-derivative verification**

The in-text derivation of $\partial V/\partial g \approx 0.176$ for the specific parameters WACC = 0.09, g = 0.03 is correct and is a nice pedagogical touch. Equation (24) gives $\partial V/\partial g = \mathrm{FCF}_n(1+\mathrm{WACC})/(\mathrm{WACC}-g)^2$; at the stated parameters this yields a multiplier consistent with the claimed ~15–18% per 100 bps.

**2.5 Monte Carlo implementation**

The simulation is algorithmically correct. The truncation `g_term_sim = np.minimum(g_term_sim, wacc_sim - 0.005)` enforces the Gordon Growth Model validity condition. The use of explicit-period growth as a matrix draw `(n_simulations, n_years)` correctly introduces year-by-year variation. A reviewer note: the correlation between WACC and terminal growth rate is assumed zero, which may understate tail risk (rising rates typically compress growth; a Cholesky-correlated draw would be more realistic). This is worth a footnote acknowledgment.

**2.6 Code quality**

The FCFF computation function has a subtle Python bug: `if ebt and ebt != 0` evaluates `ebt` as a boolean before the explicit zero check, meaning `ebt = 0.0` returns False and bypasses the zero check incorrectly (though the result is the same). The idiomatic form is `if ebt is not None and ebt != 0`.

---

## 3. Exposition Quality

**Score: Good**

The chapter is clearly written and well-organised. The roadmap subsection is effective. Definitions, propositions, and examples are properly labelled and cross-referenced. The use of context and deepdive environments appropriately signals depth of treatment.

**3.1 Points requiring attention**

- The grammar error in §6.4 ("Prompt-based selection leverages broad world knowledge but hallucinate") should be corrected to "hallucinates."
- Python 3.10+ union-type hints (`float | None`) are used without a version note. Since many practitioners still run Python 3.9, a brief comment would prevent confusion.
- The figure caption for Figure 1 references "the most recently reported free cash flow" without specifying fiscal year or value, making the figure non-reproducible as stated. The caption should include the specific FCF and the fiscal year.
- The benchmarking subsection (§7.1) claims coverage rates of >90% for S&P 500 and >75% for Russell 2000, citing "internal experiments and published literature." The cited reference (Zhang et al. 2024) studies financial question-answering, not valuation pipeline coverage rates. These claims should be either properly sourced or reframed as illustrative estimates.

---

## 4. Exercise Quality

**Score: Insufficient — requires additional exercises**

The chapter presents eight learning objectives but provides only a single exercise (DCF sensitivity heatmap). This is a significant deficiency for a textbook chapter. A reader who completes the chapter has no structured opportunity to practise:
- FCFF computation from raw financial statement data
- Evaluating a CoT forecast using MAPE, RMSE, and directional accuracy against a random-walk baseline
- Building an embedding-based comparable peer set using FAISS
- Running a Monte Carlo DCF and interpreting the resulting distribution

The reviewer strongly recommends adding at least four additional exercises, with at least one at each difficulty level [B], [I], and [A], as per the project's convention. The existing exercise is well-designed and should be retained as the capstone problem.

---

## 5. Minor Comments

1. Consider adding a brief discussion of data licensing: EDGAR data is public, but supplementary financial data providers (FactSet, Bloomberg, Refinitiv) have licensing constraints that practitioners must navigate. A one-paragraph note would make the chapter more practically complete.
2. The case study in §6.3 uses "illustrative" numbers described as "a composite of publicly available filings." It would strengthen the chapter to either (a) use a specific real company with cited data, or (b) clearly label the case study as entirely hypothetical to avoid any appearance of misrepresentation.
3. The ReAct trace in Listing 8 is an excellent pedagogical device. Consider making it a formal worked example (with a \begin{example} environment) so it appears in the list of examples.

---

## Decision

**MINOR_REVISION**

The chapter is technically sound and pedagogically well-designed in most respects. The revisions required are:

1. **(Required)** Correct the EV inconsistency ($15.2B vs. $13.3B) between §2.1 and §4.3.
2. **(Required)** Add a WACC estimation subsection or prominent remark directing readers to CAPM-based derivation.
3. **(Required)** Add at least four exercises covering FCFF computation, forecast evaluation, comparable selection, and Monte Carlo simulation.
4. **(Recommended)** Correct the grammar error in §6.4, add a Python version note, fix the figure caption provenance, and reframe the benchmarking claims in §7.1.
5. **(Optional)** Correlate WACC and terminal growth in the Monte Carlo draws and acknowledge the zero-correlation assumption.

None of these changes require structural reorganisation. The chapter is accepted pending these revisions.
