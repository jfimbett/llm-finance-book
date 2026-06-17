# Peer Review — Chapter 10: Portfolio Optimization and Quantitative Trading with LLMs

**Book:** Large Language Models in Finance  
**Author:** Juan F. Imbet (Paris Dauphine – PSL University)  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Verdict:** MAJOR_REVISION

---

## 1. Significance

The chapter addresses a timely and practically important question: how do large language models fit into the classical quantitative-finance toolkit of Markowitz optimization, Black-Litterman, factor models, and systematic trading? The framing is sensible—LLMs as "information extractors, not optimizers"—and the coverage is broader than most competing treatments, which tend to focus narrowly on sentiment classification. The inclusion of tail-risk estimation, CVaR-constrained optimization, and real-time monitoring via LLM alert systems is particularly valuable and not widely covered in the textbook literature.

**Assessment: High significance. The chapter fills a genuine gap.**

---

## 2. Technical Correctness

Several technical issues require revision before publication.

**Critical:**

1. **Almgren-Chriss cost function (eq. ch10-ac-cost).** The presented equation conflates the temporary-impact term and the residual-inventory risk term in a way that does not correspond to the canonical Almgren and Chriss (2001) formulation. In the original, the cost has the form:
   - Expected cost from temporary impact: $\sum_k \eta x_k^2$
   - Risk term on residual inventory: $\frac{1}{2}\gamma\sigma^2 \sum_k x_k^2 (T-t_k)$ (or a continuous equivalent)
   The presented form $\gamma \sigma^2 x_k (X - \sum_{j=1}^k x_j)$ is neither the temporary-impact term nor the standard risk penalty. If this is a simplified exposition, it must be labeled as such; as written, it is technically incorrect.

2. **Symbol $\alpha$ overloaded four times.** The same symbol $\alpha$ denotes: (i) the CVaR confidence level (eq. ch10-cvar), (ii) the GARCH ARCH coefficient (eq. ch10-risk-model-2), (iii) the factor regression intercept (eq. ch10-lf-alpha-regression), and (iv) the BL calibration constant (eq. ch10-signal-to-view). In a chapter where students will move between sections, this is a correctness failure. Standard convention uses $a$ or $\phi$ for the GARCH ARCH coefficient.

**Significant:**

3. **Minimum track-record-length formula (eq. ch10-min-track).** The skewness and kurtosis are denoted $\gamma_1$ and $\gamma_2$, clashing with uses of $\gamma$ elsewhere (risk-aversion, GARCH coefficient). These should be explicitly re-labeled with a clearly defined legend.

4. **Sharpe ratio of 3.05 (KirtacGermano2024).** An annualized Sharpe ratio of 3.05 post-transaction-costs is in the top percentile of any published systematic strategy. The claim is presented without specifying the sample period, universe, or cost model. Extraordinary claims require either full methodological specification or a hedging caveat.

**Minor:**

5. The shrinkage attribution to DeMiguel et al. (2009) is imprecise—Ledoit and Wolf (2003) is the canonical shrinkage reference.

6. The signal-decay half-life range ($\lambda \approx 0.1$–$0.5$ day$^{-1}$) is stated without a citation.

7. The FinRL simulation result (8–12% shortfall reduction from LLM state augmentation) is not sourced.

---

## 3. Exposition Quality

The chapter is generally well-written. The progression from classical theory (Section 1) to LLM-augmentation (Sections 2–3) to empirical evaluation (Section 4) to risk management (Section 5) is logical. The three worked examples—BL single view (Ex. ch10-bl-single-view), earnings-call extraction (Ex. ch10-earnings-call-bl), and 8-K alert (Ex. ch10-8k-alert)—are concrete and illustrative, and are the chapter's pedagogical highlight.

**Areas for improvement:**

- **No figures.** A chapter on portfolio optimization that contains no graphical illustration of the efficient frontier, the BL update, or the walk-forward protocol is pedagogically weaker than it could be. Even a single schematic figure of the BL pipeline would substantially improve comprehension.

- **Illustrative numbers not labeled as such.** In Example ch10-earnings-call-bl, the correlation of 0.08 and the 15% Sharpe improvement are presented without a clear statement that they are illustrative/hypothetical. This is a recurring issue—the chapter should distinguish numerical facts (from cited papers) from illustrative numbers (from the author's exposition).

- **CVaR-constrained optimization (eq. ch10-cvar-constrained) is stated but never demonstrated.** Given that objective 6 in the learning objectives explicitly mentions "Apply CVaR-based risk management," a brief numerical example or worked problem would satisfy the stated learning goal.

- **The RL execution section (Sec. 3.2)** is the weakest section. The state space and reward function of the RL agent are described abstractly but the connection to the LLM augmentation is not illustrated with a worked example or a specific algorithm.

---

## 4. Exercise Quality

No exercises appear in this file; they are expected to reside in a companion `exercises.md` per the book conventions. If exercises exist, this review cannot evaluate them. If they do not yet exist, exercises covering at least the following topics are essential:
- Computing the BL posterior mean given a single view (beginner)
- Constructing and evaluating a language factor from a provided sentiment matrix (intermediate)
- Identifying look-ahead bias in a described backtest scenario (intermediate)
- CVaR-constrained portfolio formation with a textual risk signal (advanced)

---

## 5. Summary and Verdict

This chapter makes a valuable contribution to the LLM-in-finance textbook literature. Its strengths—broad coverage, clear theoretical framing, realistic examples, and the "LLM as information extractor" organizing principle—make it worth revising. The technical errors (Almgren-Chriss equation, alpha overloading) are fixable and must be fixed before publication. The exposition would benefit substantially from at least one figure and from clearer labeling of illustrative numerical claims.

**Verdict: MAJOR_REVISION**

Primary revision requirements:
1. Correct or clearly qualify the Almgren-Chriss cost function.
2. Resolve the fourfold overloading of $\alpha$.
3. Reconcile $\gamma$ / $\gamma_1$ / $\gamma_2$ notation across sections.
4. Add caveat to the 3.05 Sharpe claim and label illustrative numbers as such.
5. Add at least one figure (efficient frontier or BL pipeline schematic).
6. Add a worked CVaR numerical example or exercise to satisfy learning objective 6.
