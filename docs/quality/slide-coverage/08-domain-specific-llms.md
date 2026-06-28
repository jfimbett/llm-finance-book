# Slide Coverage — Chapter 08: Domain-Specific Financial LLMs

Generated during P1–P2 pass. Checked against `book/chapters/08-domain-specific-llms/chapter.tex`.

---

## Concept Checklist

### Sections / subsections

- [x] §1 Why Domain-Specific LLMs?
- [x] §1.1 Financial Language: Jargon, Numerics, Tables
- [x] §1.2 Limitations of General-Purpose Models on Financial Tasks
- [x] §2 A Taxonomy of Financial LLMs
- [x] §2.1 Encoder–Decoder Models: T5 Family in Finance
- [x] §2.2 BERT-Family: FinBERT, SEC-BERT, FinBERT-tone
- [x] §2.3 Decoder-Family: BloombergGPT, FinGPT, FinMA, InvestLM
- [x] §3 Pre-training Strategies for Finance
- [x] §3.1 Domain-Adaptive Pre-training (DAPT)
- [x] §3.2 Corpus Composition: Bloomberg Archives, EDGAR, Financial News
- [x] §4 Benchmark Comparisons
- [x] §4.1 Financial NLP Benchmarks: FinQA, FLUE, FinBen
- [x] §4.2 When Do FinLLMs Outperform General Models? When Do They Lose?
- [x] §5 Practical Deployment Considerations
- [x] §5.1 Licensing, Hosting, and Data Governance
- [x] §5.2 Cost vs. Performance Trade-offs: Hybrid Strategies
- [x] §6 Summary / Wrap-up
- [x] §7 Further Reading

### Named models / methods

- [x] FinBERT (Araci 2019)
- [x] FinBERT (Yang, Uy, and Huang 2020) / FinBERT-tone
- [x] SEC-BERT (Loukas 2022)
- [x] BloombergGPT (Wu et al. 2023)
- [x] FinGPT (Yang et al. 2023)
- [x] FinMA / PIXIU (Xie et al. 2023)
- [x] InvestLM (Yang et al. 2023)
- [x] T5 / FLAN-T5 (Raffel et al. 2020) — encoder–decoder family
- [x] Domain-Adaptive Pre-training (DAPT)
- [x] Task-Adaptive Pre-training (TAPT)
- [x] LoRA (Hu et al. 2022) — FinGPT's fine-tuning method
- [x] GPTQ (Frantar et al. 2022) — quantisation
- [x] AWQ (Lin et al. 2023) — quantisation
- [x] QLoRA (Dettmers et al. 2023) — quantisation
- [x] Retrieval-Augmented Generation (RAG, Lewis et al. 2020)
- [x] Loughran–McDonald financial dictionary

### Key numbers

- [x] LM dictionary: ~350 words with neutral/inverted polarity in SEC filings
- [x] FinBERT (Araci): ~1.8 billion words corpus (Reuters TRC2, Bloomberg, PhraseBank)
- [x] SEC-BERT: ~3 billion tokens of EDGAR text
- [x] BloombergGPT: 50B parameters, 708B total tokens
- [x] BloombergGPT corpus: 363B FinPile (financial) + 345B general (Pile, Wikipedia, books)
- [x] FinMA: 7B LLaMA, 136,000 instruction–response pairs
- [x] InvestLM: 65B LLaMA
- [x] DAPT budget: 1–10B domain tokens (vs. hundreds of billions original)
- [x] Encoders DAPT: 1–5B tokens typically sufficient
- [x] LR reduction: ~10× below original pre-training rate
- [x] FinQA: 8,281 QA pairs from 10-K/10-Q filings
- [x] FinQA accuracy: fine-tuned specialists ~68–72%; zero-shot GPT-4 class ~55–60%
- [x] FinBen: 36 datasets, 24 tasks, 5 capability categories
- [x] FLUE: 5-task NLU suite
- [x] GPT-3 175B on FinQA tables: <60% accuracy
- [x] Quantisation memory reduction: 2–4×
- [x] FinBERT inference latency: sub-50ms on single A10G
- [x] Cost example: API ~$0.002/1K tokens; FinBERT server ~$400/month; hybrid ~$250/year
- [x] Hybrid accuracy: 92%+ vs. 88% (FinBERT alone) vs. 93% (70B alone)

### Citations (Author, year)

- [x] Loughran & McDonald (2011) — LM dictionary
- [x] Chen et al. (2021) — FinQA
- [x] Malo et al. (2014) — Financial PhraseBank
- [x] Araci (2019) — FinBERT
- [x] Yang et al. (2020) — FinBERT-tone
- [x] Loukas et al. (2022) — SEC-BERT
- [x] Kang & Liu (2023) — hallucination in financial LLMs
- [x] Wu et al. (2023) — BloombergGPT
- [x] Gao et al. (2020) — The Pile
- [x] Yang et al. (2023) — FinGPT
- [x] Hu et al. (2022) — LoRA
- [x] Xie et al. (2023) — FinMA / PIXIU
- [x] Yang et al. (2023) — InvestLM
- [x] Gururangan et al. (2020) — DAPT paper
- [x] Hirano (2024a) — Japanese financial LLM DAPT
- [x] Hirano (2024b) — model merging without instruction data
- [x] Zhang et al. (2023) — instruction-tuning for financial sentiment
- [x] Keshri et al. (2025) — BloombergGPT survey
- [x] Cook & Kazinnik (2023) — evaluation framework on bank earnings calls
- [x] Shah et al. (2022) — FLUE
- [x] Xie et al. (2024) — FinBen
- [x] Tetlock (2007) — text predicts returns
- [x] Wei et al. (2022) — chain-of-thought prompting
- [x] Rahimikia & Drinkall (2024) — year-specific FinLLMs on return prediction
- [x] Liu et al. (2024) — FinGPT RAG extension
- [x] Lewis et al. (2020) — RAG
- [x] SR 11-7 — model risk management guidance
- [x] Frantar et al. (2022) — GPTQ
- [x] Lin et al. (2023) — AWQ
- [x] Dettmers et al. (2023) — QLoRA
- [x] Loughran & McDonald (2020) — textual analysis review
- [x] Huang et al. (2023) — FinBERT accounting research perspective
- [x] Li et al. (2023) — LLM-in-finance survey
- [x] Hansen (2018) — monetary policy transparency
- [x] Raffel et al. (2020) — T5
- [x] Devlin et al. (2019) — BERT

### Definitions (formal)

- [x] Definition: Financial Language Register (3 dimensions)
- [x] Definition: Financial LLM Taxonomy (formal set-theoretic)
- [x] Definition: Domain-Adaptive Pre-training (DAPT) — formula θ* = argmin L_PT(θ; D_domain)
- [x] Definition: Execution Accuracy (EA formula for FinQA)
- [x] Definition: Effective Cost per Correct Output — C_eff formula

### Figures / tables

- [x] Table: Major corpus sources (Scale, Quality, Access, Coverage)
- [x] Figure fig_corpus.png: log-scale corpus token counts (lesson deck + practical deck)
- [x] Example: FinBERT earnings-call sentiment ("cautiously optimistic")
- [x] Example: Central-bank corpus composition (FOMC hawkish/dovish)
- [x] Example: Hybrid deployment — regulatory filing classifier cost analysis

---

## Omissions (P2 diff pass — all resolved)

All items were either already present or added during P3/P4. No unchecked items remain.
