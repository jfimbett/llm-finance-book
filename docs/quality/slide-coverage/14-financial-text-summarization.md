# Slide Coverage — Chapter 14: Financial Text Summarization & Information Extraction

Source: `book/chapters/14-financial-text-summarization/chapter.tex`

---

## Sections / Subsections

- [x] §1 The Information Extraction Problem in Finance
- [x] §1.1 Structured vs. Unstructured Financial Text
- [x] §1.2 Key Entities: Companies, Dates, Monetary Figures, Covenants
- [x] §1.3 Extraction vs. Summarization: Task Definitions
- [x] §2 Named Entity Recognition in Finance
- [x] §2.1 Financial NER Datasets: FINER-139, FinNER, FinRE
- [x] §2.2 Fine-Tuning Transformer NER for Financial Documents
- [x] §2.3 Relation Extraction: Ownership, Employment, Transactions
- [x] §3 Financial Document Summarization
- [x] §3.1 Extractive vs. Abstractive Summarization
- [x] §3.2 Earnings Report and Annual Report (10-K) Summarization
- [x] §3.3 Analyst Note and Research Report Condensation
- [x] §3.4 Long-Document Challenges: Earnings Transcripts, S-1 Filings
- [x] §4 Table and Numerical Data Extraction
- [x] §4.1 SEC XBRL Data: Structured Extraction from Filings
- [x] §4.2 LLMs for Financial Table Understanding and Parsing
- [x] §4.3 Consistency Checking: Extracted Numbers vs. Prose Claims
- [x] §5 Evaluation and Benchmarks
- [x] §5.1 ROUGE, BERTScore, and Factual Consistency Metrics
- [x] §5.2 Human Evaluation by Financial Domain Professionals
- [x] §5.3 Available Datasets: ECTSum, EDGAR-Corpus, FINER, FinSBD

---

## Named Methods / Models / Results

- [x] FINER-139 (Loukas et al., 2022) — 139 fine-grained financial entity types
- [x] FinNER — document-level NER with coreference chains
- [x] FinRE — relation extraction with typed triples
- [x] EDGAR-Corpus (Loukas et al., 2021) — 6M+ filings, ~6.5B tokens, 1993–2020
- [x] SEC-BERT (Loukas et al., 2022) — SOTA on SEC-domain NER
- [x] FinBERT (Yang et al., 2020) — finance-pretrained BERT
- [x] BIO labelling scheme (Beginning / Inside / Outside)
- [x] CRF + Viterbi decoder for valid BIO sequences
- [x] DyGIE++ (Wadden et al., 2019) — joint entity-and-relation extraction
- [x] ECTSum (Mukherjee et al., 2022) — 2,425 earnings transcript–summary pairs
- [x] Longformer (Beltagy et al., 2020) — long-context encoder
- [x] Gemini 1.5 Pro (128K–1M token context window)
- [x] ROUGE-N and ROUGE-L (Lin, 2004)
- [x] BERTScore (Zhang et al., 2020) — cosine of contextual embeddings
- [x] FactCC (Kryscinski et al., 2020) — NLI-based factual consistency
- [x] FinQA (Chen et al., 2021) — numerical reasoning over financial tables
- [x] FinSBD (2020) — sentence boundary detection
- [x] ReAct framework (Yao et al., 2022) — route arithmetic to code interpreter
- [x] LayoutLM — document AI for table layout parsing
- [x] DocRED — document-level relation extraction benchmark
- [x] Hybrid summarization (see2017get) — extract then rephrase
- [x] FinBen survey (Xie et al., 2024) — 12+ financial NLP benchmarks
- [x] TextRank / PageRank extractive summarization (practical)
- [x] Delta summarization — highlight changes across report versions
- [x] Map-reduce / hierarchical summarization pipeline
- [x] Retrieval-augmented summarization (Lewis et al., 2020)
- [x] Inline XBRL mandate — U.S. domestic filers since 2020
- [x] LiGao2023 — prompt engineering for PDF financial data extraction
- [x] ShafferWang2024 — sequential prompting for non-recurring items in 10-K
- [x] CookKazinnik2023 — local LLMs on bank earnings call transcripts
- [x] Siano2025 — LLM representations explain short-window stock returns
- [x] ErnstbergerNazemi2025 — LLM earnings-call signals predict bond recovery rates
- [x] WangWang2025 — consistency/reproducibility of LLM outputs on financial texts
- [x] Lehner2024 — tone alteration in 10-K filings via LLM rewriting

---

## Key Numbers

- [x] 6,000+ companies in the Russell 3000
- [x] EDGAR-Corpus: 6M+ filings, ~6.5B tokens, 1993–2020
- [x] FINER-139: 139 fine-grained entity types
- [x] Outside (O) class: 85–95% of tokens in financial NER
- [x] Classification head dimension: C = 2 × 139 + 1 = 279
- [x] AdamW: β₁ = 0.9, β₂ = 0.999, weight decay = 0.01, peak LR = 2 × 10⁻⁵, 10 epochs
- [x] Training time: ~20 min on a single A100 GPU
- [x] 10-K length: 50,000–150,000 words
- [x] Sliding windows: 512-token chunks, 64-token overlap
- [x] Earnings transcripts: 15,000–30,000 words
- [x] ECTSum: 2,425 transcript–summary pairs; 3–6 bullet abstracts
- [x] S-1 registration statements can exceed 300,000 words
- [x] FinQA: ~50% exact-match for retrieval baselines; >70% for program-generation models
- [x] Hallucination rate: 25–30% on CNN/DailyMail (Kryscinski 2020)
- [x] Constrained prompt: ~40% reduction in number errors; ~8% paraphrase errors remain
- [x] Consistency tolerance: 0.1% for rounding
- [x] Section summaries target length: 200–400 words (two-stage hierarchical)
- [x] Cohen's κ / Krippendorff's α for inter-annotator agreement

---

## Citations (Author, year)

- [x] (Loughran & McDonald, 2020) — textual analysis of financial documents
- [x] (Tetlock, 2008) — words and stock returns
- [x] (Li, 2008) — annual report readability
- [x] (Frattaroli, 2019) — contractual covenants
- [x] (Lample et al., 2016) — neural NER
- [x] (Loukas et al., 2022) — FINER-139; SEC-BERT
- [x] (Loukas et al., 2021) — EDGAR-Corpus
- [x] (Yang et al., 2020) — FinBERT
- [x] (Beltagy et al., 2020) — Longformer
- [x] (Wadden et al., 2019) — DyGIE++
- [x] (Chen et al., 2021) — FinQA
- [x] (Loughran & McDonald, 2011) — MD&A tone and liability
- [x] (Lehner, 2024) — tone alteration in 10-K via LLM rewriting
- [x] (Mukherjee et al., 2022) — ECTSum
- [x] (Cook & Kazinnik, 2023) — local LLMs on earnings calls
- [x] (Siano, 2025) — LLM representations and stock returns
- [x] (Ernstberger & Nazemi, 2025) — LLM signals predict bond recovery
- [x] (Lewis et al., 2020) — RAG
- [x] (SEC, 2009 / 2020) — XBRL mandate
- [x] (Li & Gao, 2023) — prompt engineering for PDF extraction
- [x] (Shaffer & Wang, 2024) — sequential prompting for non-recurring items
- [x] (Lin, 2004) — ROUGE
- [x] (Zhang et al., 2020) — BERTScore
- [x] (Kryscinski et al., 2020) — FactCC
- [x] (Wang & Wang, 2025) — LLM output consistency/reproducibility
- [x] (Maynez et al., 2020) — faithfulness and hallucination
- [x] (Yao et al., 2022) — ReAct
- [x] (FinSBD, 2020) — sentence boundary detection
- [x] (Xie et al., 2024) — FinBen survey
- [x] (Devlin et al., 2019) — BERT survey
- [x] (Shah et al., 2023) — English/Greek FINER
- [x] (See et al., 2017) — hybrid extract-then-rephrase

---

## Omissions

*(All items checked — no omissions remain after P3 expansion pass.)*
