# Peer Review: Chapter 8 — Domain-Specific Financial Large Language Models

**Manuscript:** `book/chapters/08-domain-specific-llms/chapter.tex`
**Review date:** 2026-05-31
**Reviewer:** Anonymous

---

## 1. Significance

The chapter addresses a genuinely important topic: the practical and empirical case for domain-specific pre-training in financial NLP. The material is well-scoped and the research surveyed (FinBERT, BloombergGPT, FinGPT, FinMA, InvestLM, FinQA, FLUE, FinBen) constitutes the canonical literature. The section on the "scaling crossover" (Section 4.2) and the cost-per-correct-output framework (Definition 4) are original pedagogical contributions that add value beyond a simple survey. The chapter will be useful to its intended mixed academic/practitioner audience.

**Significance verdict: Acceptable.**

---

## 2. Technical Correctness

**2.1 Factual error — BloombergGPT corpus size (lines 263–266).**

The text reads: "a 50-billion-parameter autoregressive decoder model trained on a 363-billion-token corpus. The corpus blends a proprietary Bloomberg dataset (363B tokens…) with 345B tokens from standard general corpora."

The Bloomberg dataset is reported as 363B tokens and the general corpora as 345B tokens, giving a total of approximately 708B tokens — not 363B. The figure 363B on line 263 refers only to the Bloomberg-side component, not the combined corpus. This is a factual error that needs correction before publication.

**2.2 Citation inconsistency — FinBERT (Yang, Uy, Huang 2020) (lines 206–208).**

The subsection heading references "Yang, Uy, and Huang 2020" and the cite key `yang2020finbert`, but the prose on line 208 uses `\citet{huang2023finbert}`, which resolves to a 2023 Contemporary Accounting Research article (a different paper). The inline author attribution should cite the original Yang, Uy, Huang (2020) paper throughout, not the 2023 follow-up. The 2023 paper (`huang2023finbert`) is correctly cited later in the Further Reading section (line 873) but its misplacement in the subsection heading paragraph creates confusion.

**2.3 Assumption in Definition 4 — effective cost per correct output (lines 743–755).**

The formula assumes human review has recall of 1.0 ("we assume human review recovers all incorrectly classified queries"). This is a convenient simplification but should be flagged as an assumption explicitly in the definition body. More significantly, the formula conflates query-level and corpus-level costs: $c_m$ as written is the per-query model inference cost, but the numerator $c_m + \rho c_h$ implies that the human review cost is additive per query even for the $(1-\rho)$ fraction that bypass review. A cleaner formulation would make explicit that $c_m$ is incurred for every query and $c_h$ only for the $\rho$-fraction.

**2.4 Encoder-decoder family absent.**

The taxonomy (Section 2) covers encoder-only and decoder-only architectures but omits the encoder-decoder family (T5, BART). FinT5 and domain-adapted T5 models have been applied to financial summarisation and QA tasks. This gap should be acknowledged at minimum with a footnote or paragraph noting that encoder-decoder models exist but are less prevalent in the current financial LLM literature.

**2.5 Numerical claims — benchmark accuracy figures.**

The FinQA accuracy figures cited (specialist systems 68–72%, GPT-4 zero-shot 55–60%; Financial PhraseBank FinBERT F1 ~0.88 vs. BERT ~0.72 and RoBERTa ~0.80) are plausible but stated without a specific publication date or leaderboard snapshot. Given the rate of progress in the field, readers should be warned that these figures may be superseded. A footnote referencing the data as of a specific year (or at publication) would improve reproducibility.

**Technical correctness verdict: Minor-to-major revisions needed.**

---

## 3. Exposition Quality

The chapter's expository quality is generally high. The three-feature characterisation of financial language (Section 1.1) is pedagogically crisp. The encoder/decoder taxonomy (Section 2) is useful and practical. The DAPT section (3.1) correctly cites Gururangan et al. 2020 as the foundational reference and explains the mechanics clearly.

However, three exposition issues warrant revision:

- **No exercises.** The CLAUDE.md project convention requires at least one each of [B] (beginner), [I] (intermediate), and [A] (advanced) exercise. The chapter has none. This is a significant omission for a textbook chapter; readers have no practice tasks.
- **Fine-tuning/instruction-tuning distinction.** Section 2.2 covers FinMA and InvestLM but does not clearly distinguish supervised fine-tuning (SFT) from instruction tuning, which differ in dataset construction and intended use. This distinction matters for practitioners deciding how to replicate these approaches.
- **Quantisation section (lines 722–728)** introduces GPTQ, AWQ, and QLoRA as techniques but does not explain the core mechanism of post-training quantisation or the accuracy-compression trade-off. A one-sentence definition of quantisation would be helpful given the mixed audience.

---

## 4. Exercise Quality

**Not applicable — no exercises are present.** This is a deficiency that must be addressed before publication.

---

## 5. Summary and Verdict

The chapter presents a well-organised, largely accurate, and clearly written survey of domain-specific financial LLMs, with original contributions in the cost-per-correct-output deployment framework and the scaling-crossover discussion. However, it cannot be accepted in its current form due to: (1) a factual error in the BloombergGPT corpus size, (2) a citation misattribution in the FinBERT (Yang 2020) subsection, (3) complete absence of exercises, (4) missing encoder-decoder family coverage, and (5) an unqualified benchmark figure table that will date rapidly.

These issues are correctable and none requires restructuring the chapter. With focused revisions the chapter would be ready for publication.

**Verdict: MINOR_REVISION**
