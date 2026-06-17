# Seven New Chapters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold and draft 7 new chapters that fill the gaps identified by deep research against competing books and 2023–2026 literature, then wire them into `book/main.tex` at their logical positions.

**Architecture:** Two parallel phases. Phase 1 scaffolds all 7 chapters simultaneously (directory trees, placeholder `.tex` files, lecture notes, slides, exercises, notebooks). Phase 2 drafts all 7 chapters simultaneously (full LaTeX content, bibliography entries, quality scoring). A final serial phase updates `main.tex` to include all chapters in the correct narrative order.

**Tech Stack:** LaTeX (book chapters), Beamer (slides), Markdown (notes/exercises), Jupyter (notebooks), `book/bibliography.bib` (references), project skill system (`/new-topic`, `/draft-chapter`).

---

## Chapter Placement Map

The book has 15 planned chapters; 7 exist (01–07). The 7 new chapters are assigned folder numbers 08–14 but inserted into `main.tex` at logical narrative positions:

| Folder | Title | Inserted after |
|--------|-------|---------------|
| `08-domain-specific-llms` | Domain-Specific Financial LLMs | ch03 (Training & Fine-tuning) |
| `09-financial-nlp-sentiment` | Financial NLP & Sentiment Analysis | ch04 (LLM Agents) |
| `14-financial-text-summarization` | Financial Text Summarization & Information Extraction | ch09 (NLP/Sentiment) |
| `10-portfolio-quant-trading` | Portfolio Optimization & Quantitative Trading | ch06 (Credit Risk) |
| `11-regtech-compliance-aml` | RegTech, Compliance & AML | ch10 (Portfolio) |
| `12-xai-explainability` | Explainability & XAI in Finance | ch11 (RegTech) |
| `13-llm-limitations-evaluation` | LLM Limitations & Evaluation Rigor | ch12 (XAI) |

**Final include order in `book/main.tex`:**
```
01-intro → 02-llm-foundations → 03-llm-training-finetuning →
08-domain-specific-llms → 04-llm-agents →
09-financial-nlp-sentiment → 14-financial-text-summarization →
05-business-valuation → 06-credit-risk →
10-portfolio-quant-trading → 11-regtech-compliance-aml →
12-xai-explainability → 13-llm-limitations-evaluation →
07-applications-future
```

---

## File Structure per New Chapter

Each chapter creates the following (replace `NN-name` with the actual slug):

```
book/chapters/NN-name/
  chapter.tex          — LaTeX source (scaffold → draft)
  figures/
    .gitkeep

course/lectures/NN-name/
  notes.md             — Lecture notes with objectives
  slides.tex           — Beamer presentation
  exercises.md         — B/I/A difficulty exercises
  solutions.md         — Exercise solutions

code/notebooks/NN-name/
  demo.ipynb           — Demonstration notebook
  exercises.ipynb      — Exercise notebook
```

Plus entries in `docs/STATUS.md` and `book/bibliography.bib`.

---

## Phase 1 — Scaffold (7 parallel tasks)

### Task 1.1: Scaffold `08-domain-specific-llms`

**Files to create:**
- `book/chapters/08-domain-specific-llms/chapter.tex`
- `book/chapters/08-domain-specific-llms/figures/.gitkeep`
- `course/lectures/08-domain-specific-llms/notes.md`
- `course/lectures/08-domain-specific-llms/slides.tex`
- `course/lectures/08-domain-specific-llms/exercises.md`
- `course/lectures/08-domain-specific-llms/solutions.md`
- `code/notebooks/08-domain-specific-llms/demo.ipynb`
- `code/notebooks/08-domain-specific-llms/exercises.ipynb`

**Outline:**
1. Why Domain-Specific LLMs?
   1.1 Financial language: jargon, numerics, tables
   1.2 Limitations of general-purpose models
2. A Taxonomy of Financial LLMs
   2.1 BERT-family: FinBERT, SEC-BERT
   2.2 Decoder-family: BloombergGPT, FinGPT, FinMA
3. Pre-training Strategies for Finance
   3.1 Domain-adaptive pre-training (DAPT)
   3.2 Corpus composition: Bloomberg archives, EDGAR
4. Benchmark Comparisons
   4.1 Financial NLP benchmarks: FinQA, FLUE
   4.2 When do FinLLMs win vs. general models?
5. Practical Deployment
   5.1 Licensing and data governance
   5.2 Cost vs. performance trade-offs

- [ ] Create `book/chapters/08-domain-specific-llms/chapter.tex` with `\chapter{Domain-Specific Financial LLMs}` and one `\section{}`/`\subsection{}` per outline item, each with `[Placeholder]` body.
- [ ] Create `book/chapters/08-domain-specific-llms/figures/.gitkeep`
- [ ] Create `course/lectures/08-domain-specific-llms/notes.md`
- [ ] Create `course/lectures/08-domain-specific-llms/slides.tex`
- [ ] Create `course/lectures/08-domain-specific-llms/exercises.md` with B/I/A exercises
- [ ] Create `course/lectures/08-domain-specific-llms/solutions.md`
- [ ] Create `code/notebooks/08-domain-specific-llms/demo.ipynb`
- [ ] Create `code/notebooks/08-domain-specific-llms/exercises.ipynb`
- [ ] Append row to `docs/STATUS.md`
- [ ] `git add` and commit: `chore: scaffold chapter 08-domain-specific-llms`

### Task 1.2: Scaffold `09-financial-nlp-sentiment`

**Outline:**
1. Text as Financial Data
   1.1 Sources: social media, news, filings, transcripts, policy
   1.2 Preprocessing pipeline
2. Sentiment Analysis
   2.1 Lexicon-based: Loughran-McDonald
   2.2 Fine-tuned classifiers: FinBERT sentiment
   2.3 LLM zero-shot and few-shot sentiment
3. Applications by Source
   3.1 Social media: Twitter/X, Reddit WSB, StockTwits
   3.2 News and wire services
   3.3 Earnings call transcripts
   3.4 SEC filings: 10-K/10-Q risk factors
   3.5 FOMC and ECB communications
4. From Sentiment to Signal
   4.1 Aggregation and normalization
   4.2 Event studies: earnings surprises, FOMC shocks
5. Practical Pipeline
   5.1 Data collection APIs
   5.2 Evaluation: Krippendorff's alpha, precision/recall

- [ ] Create all 8 files (same structure as Task 1.1, with chapter title `Financial NLP \& Sentiment Analysis`)
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 09-financial-nlp-sentiment`

### Task 1.3: Scaffold `10-portfolio-quant-trading`

**Outline:**
1. Classical Portfolio Theory and Its Limits
   1.1 Markowitz mean-variance optimization
   1.2 Black-Litterman: views and priors
2. LLMs as Alternative Data Processors
   2.1 Extracting views from text
   2.2 LLM-based factors for Fama-French models
3. LLM-Guided Algorithmic Trading
   3.1 LLMs as signal generators
   3.2 LLM-guided reinforcement learning
   3.3 Why LLMs are not stock pickers
4. Backtesting with LLM Signals
   4.1 Walk-forward evaluation
   4.2 Transaction costs and capacity analysis
5. Risk Management Applications
   5.1 Tail risk estimation from text
   5.2 Real-time monitoring systems

- [ ] Create all 8 files, chapter title `Portfolio Optimization and Quantitative Trading`
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 10-portfolio-quant-trading`

### Task 1.4: Scaffold `11-regtech-compliance-aml`

**Outline:**
1. The Regulatory Landscape for AI in Finance
   1.1 EU AI Act, MiFID II, Basel III
   1.2 GDPR and data privacy constraints
2. Anti-Money Laundering with LLMs
   2.1 The false-positive crisis in keyword-based AML
   2.2 Agentic LLM systems for adverse media screening
   2.3 RAG-based adverse media pipelines
   2.4 Adverse Media Index: quantitative risk scoring
3. KYC and Sanctions Screening
   3.1 Entity resolution and disambiguation
   3.2 Politically exposed persons (PEP) screening
4. Regulatory Reporting Automation
   4.1 XBRL tagging and filing
   4.2 Suspicious activity report (SAR) drafting
5. Governance and Audit Trails
   5.1 Explainability for compliance decisions
   5.2 Model risk management for LLM compliance

- [ ] Create all 8 files, chapter title `RegTech, Compliance, and Anti-Money Laundering`
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 11-regtech-compliance-aml`

### Task 1.5: Scaffold `12-xai-explainability`

**Outline:**
1. Why Explainability Matters in Finance
   1.1 Regulatory requirements: EU AI Act, SR 11-7
   1.2 Stakeholder expectations
2. Classical XAI Methods Applied to LLMs
   2.1 SHAP values and feature attribution
   2.2 LIME for local explanations
   2.3 Attention visualization: uses and misuses
3. LLM-Native Explainability
   3.1 Chain-of-thought as explanation
   3.2 Counterfactual explanations
   3.3 Natural language justifications
4. Case Studies
   4.1 Credit scoring explainability
   4.2 Loan denial letters under ECOA
   4.3 Investment recommendation disclosures
5. Evaluating Explanations
   5.1 Faithfulness, completeness, plausibility
   5.2 Human studies with domain experts

- [ ] Create all 8 files, chapter title `Explainability and XAI in Finance`
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 12-xai-explainability`

### Task 1.6: Scaffold `13-llm-limitations-evaluation`

**Outline:**
1. Calibration and Overconfidence
   1.1 When LLMs say "I'm sure" and are wrong
   1.2 Measuring calibration in financial tasks
2. Temporal Leakage and Look-Ahead Bias
   2.1 How pretrained models memorize future events
   2.2 Point-in-time data and anonymization
   2.3 Contamination-resistant evaluation design
3. Stock Movement Prediction: A Cautionary Tale
   3.1 Why LLMs cannot predict markets
   3.2 Accuracy evidence: 51–65% across 250 stocks
   3.3 Efficient markets and the information barrier
4. Evaluation Beyond Accuracy
   4.1 Economic value metrics: Sharpe ratio, alpha
   4.2 Walk-forward tests, transaction costs, capacity
5. Hallucination in Financial Contexts
   5.1 Fabricated citations, numbers, company facts
   5.2 Detection and mitigation: RAG, grounding

- [ ] Create all 8 files, chapter title `LLM Limitations and Evaluation Rigor in Finance`
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 13-llm-limitations-evaluation`

### Task 1.7: Scaffold `14-financial-text-summarization`

**Outline:**
1. Structured vs. Unstructured Financial Text
   1.1 Information extraction vs. summarization
   1.2 Key entities: companies, dates, figures, covenants
2. Named Entity Recognition in Finance
   2.1 FINER, FinNER, FinRE datasets
   2.2 Fine-tuning NER for financial documents
3. Financial Summarization
   3.1 Extractive vs. abstractive approaches
   3.2 Earnings report and 10-K summarization
   3.3 Analyst note condensation
4. Table and Number Extraction
   4.1 Parsing SEC XBRL data
   4.2 LLMs for financial table understanding
5. Evaluation Frameworks
   5.1 ROUGE, BERTScore, factual consistency
   5.2 Human evaluation: financial professionals as judges
   5.3 Benchmark datasets: ECTSum, EDGAR-Corpus

- [ ] Create all 8 files, chapter title `Financial Text Summarization and Information Extraction`
- [ ] Append row to `docs/STATUS.md`
- [ ] Commit: `chore: scaffold chapter 14-financial-text-summarization`

---

## Phase 2 — Draft (7 parallel tasks)

For each chapter, invoke the draft-chapter skill: literature-reviewer → book-writer → math-checker → editor → score-content → refine if below threshold → commit.

### Task 2.1: Draft `08-domain-specific-llms`
- [ ] Invoke literature-reviewer: find 5–7 references (BloombergGPT paper, FinBERT, FinGPT, FLUE benchmark, DAPT paper)
- [ ] Invoke book-writer: draft all sections in LaTeX
- [ ] Invoke math-checker: verify any equations (e.g., cross-entropy loss, perplexity)
- [ ] Invoke editor: improve clarity and flow
- [ ] Run `/score-content book/chapters/08-domain-specific-llms/chapter.tex`
- [ ] Refine if any dimension < 8
- [ ] Commit: `feat(ch08): draft domain-specific financial LLMs chapter`

### Task 2.2: Draft `09-financial-nlp-sentiment`
- [ ] Literature: FinBERT (Araci 2019), Loughran-McDonald (2011), Twitter sentiment finance papers, FOMC text analysis
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch09): draft financial NLP and sentiment analysis chapter`

### Task 2.3: Draft `10-portfolio-quant-trading`
- [ ] Literature: Black-Litterman (1990), Markowitz (1952), FinRL paper, LLM trading papers (2024)
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch10): draft portfolio optimization and quantitative trading chapter`

### Task 2.4: Draft `11-regtech-compliance-aml`
- [ ] Literature: arxiv 2602.23373 (AML adverse media), FATF guidelines, EU AI Act
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch11): draft RegTech compliance and AML chapter`

### Task 2.5: Draft `12-xai-explainability`
- [ ] Literature: Lundberg SHAP (2017), Ribeiro LIME (2016), CFA XAI report (2025), EU AI Act explainability requirements
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch12): draft explainability and XAI in finance chapter`

### Task 2.6: Draft `13-llm-limitations-evaluation`
- [ ] Literature: CFA Institute LLM guide, stock prediction accuracy study (59.4% avg), Frontiers review (84 studies), temporal leakage papers
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch13): draft LLM limitations and evaluation rigor chapter`

### Task 2.7: Draft `14-financial-text-summarization`
- [ ] Literature: ECTSum dataset, EDGAR-Corpus, FinNER, FINER-139 paper
- [ ] Draft, check, edit, score, refine
- [ ] Commit: `feat(ch14): draft financial text summarization and IE chapter`

---

## Phase 3 — Wire Up (serial)

### Task 3.1: Update `book/main.tex`

Replace the current chapter include block with the new narrative order:

```latex
\include{chapters/01-intro/chapter}
\include{chapters/02-llm-foundations/chapter}
\include{chapters/03-llm-training-finetuning/chapter}
\include{chapters/08-domain-specific-llms/chapter}
\include{chapters/04-llm-agents/chapter}
\include{chapters/09-financial-nlp-sentiment/chapter}
\include{chapters/14-financial-text-summarization/chapter}
\include{chapters/05-business-valuation/chapter}
\include{chapters/06-credit-risk/chapter}
\include{chapters/10-portfolio-quant-trading/chapter}
\include{chapters/11-regtech-compliance-aml/chapter}
\include{chapters/12-xai-explainability/chapter}
\include{chapters/13-llm-limitations-evaluation/chapter}
\include{chapters/07-applications-future/chapter}
% Add new chapters here
```

- [ ] Edit `book/main.tex` to reflect the above order
- [ ] Commit: `chore: reorder chapters in main.tex to include 7 new topics`
