# Slide Coverage Checklist — Chapter 01-intro

Source: `book/chapters/01-intro/chapter.tex`
Generated during deck overhaul (2026-06-28).

---

## Sections and Subsections

- [x] §1 Artificial Intelligence, Jobs, and Tasks
- [x] §1.1 The Task-Based Framework
- [x] §1.2 Implications for Finance Professionals
- [x] §2 A Brief History of Textual Analysis in Finance
- [x] §2.1 Early Approaches: Keyword Counting and Dictionary Methods
- [x] §2.2 The Shift to Statistical and Neural Methods
- [x] §3 Why Text Matters in Finance
- [x] §3.1 The Quantitative Growth of Financial Text (fig_edgar_text_growth)
- [x] §3.2 The Information Content of Earnings Calls, News, and Filings
- [x] §3.3 Text as a Signal: Evidence from the Literature
- [x] §4 Classical Text Representations
- [x] §4.1 Vocabulary, Tokens, and the Bag-of-Words Model
- [x] §4.2 One-Hot Encoding
- [x] §4.3 TF-IDF Weighting
- [x] §5 Word Embeddings
- [x] §5.1 Distributional Semantics and the Embedding Idea
- [x] §5.2 Word2Vec and GloVe
- [x] §5.2.1 Skip-Gram with Negative Sampling
- [x] §5.2.2 GloVe: Global Vectors for Word Representation
- [x] §5.2.3 Finance-Specific Embeddings and Domain Adaptation
- [x] §5.3 Case Study: Visualising a Word Analogy with PCA (fig_king_analogy)
- [x] §6 Recurrent Neural Networks and the Vanishing Gradient
- [x] §6.1 The Recurrence and Why Gradients Vanish
- [x] §6.2 The LSTM Fix
- [x] §7 Scaled Dot-Product Attention and the Transformer
- [x] §7.1 Attention as Content-Based Lookup
- [x] §7.2 Multiple Heads, Multiple Relations
- [x] §8 A Taxonomy of Modern Language Model Families
- [x] §8.1 Autoregressive Models: The GPT Family
- [x] §8.2 Bidirectional Encoder Models: BERT and Its Descendants
- [x] §8.3 Encoder-Decoder Models: T5
- [x] §8.4 Open-Weight Models: The LLaMA Family
- [x] §8.5 Finance-Domain Models (BloombergGPT, FinGPT)
- [x] §9 Querying LLMs via Python APIs
- [x] §9.1 The OpenAI Chat Completions API
- [x] §9.2 The Anthropic API
- [x] §9.3 HuggingFace transformers: Open-Weight Inference
- [x] §9.4 Token Costs and Latency Trade-offs
- [x] §10 Limitations of LLMs and the Regulatory Landscape
- [x] §10.1 Hallucination: Taxonomy and Detection
- [x] §10.2 Context Window Limitations
- [x] §10.3 Model Bias in Financial Applications
- [x] §10.4 The Regulatory Landscape
- [x] §11 Looking Ahead

---

## Named Methods / Models / Results

- [x] Task-based framework (Autor, Levy & Murnane, 2003)
- [x] Automation and new tasks (Acemoglu & Restrepo, 2019)
- [x] AI exposure scores (Hampole et al., 2025)
- [x] AI Occupational Exposure index (Felten, Raj & Seamans, 2021)
- [x] General Inquirer / Harvard IV-4 dictionary (Stone et al., 1966)
- [x] Tetlock (2007) WSJ negativity → DJIA returns
- [x] Tetlock & Loughran (2008) firm-level news sentiment
- [x] Loughran–McDonald (2011) LM financial sentiment dictionary
- [x] Li (2008) Fog Index readability
- [x] Latent Dirichlet Allocation (Blei, Ng & Jordan, 2003)
- [x] Boudoukh et al. (2013) LDA on news
- [x] Hansen, McMahon & Prat (2018) LDA on FOMC transcripts
- [x] Word2Vec / Skip-Gram (Mikolov et al., 2013)
- [x] Negative sampling
- [x] GloVe (Pennington, Socher & Manning, 2014)
- [x] Co-occurrence matrix
- [x] Ke et al. (2019) supervised text-mining
- [x] Manela & Moreira (2017) news-implied volatility
- [x] LSTM (Hochreiter & Schmidhuber, 1997)
- [x] Financial PhraseBank (Malo et al., 2014)
- [x] FiQA benchmark (Maia et al., 2018)
- [x] Attention mechanism (Bahdanau et al., 2015)
- [x] Transformer (Vaswani et al., 2017)
- [x] Scaled dot-product attention formula
- [x] Multi-head attention
- [x] BERT (Devlin et al., 2019)
- [x] Masked Language Modelling (MLM) objective
- [x] FinBERT — Araci (2019) and Yang et al. (2020) [two distinct models]
- [x] GPT-1 (Radford et al., 2018)
- [x] GPT-2 (Radford et al., 2019)
- [x] GPT-3 (Brown et al., 2020)
- [x] T5 (Raffel et al., 2020)
- [x] LLaMA (Touvron et al., 2023)
- [x] BloombergGPT (Wu et al., 2023)
- [x] FinGPT (Yang et al., 2023)
- [x] EMH semi-strong form (Fama, 1970)
- [x] Vector space model (Salton et al., 1975)
- [x] Davis et al. (2015) earnings call sentiment → returns
- [x] Lehavy et al. (2011) analyst report complexity
- [x] Bollen et al. (2011) Twitter mood predicts DJIA
- [x] Lopez-Lira & Tang (2023) ChatGPT sentiment scores
- [x] Larcker & Zakolyukina (2012) deceptive speech detection
- [x] Li, Lundholm & Minnis (2013) competition measure
- [x] EU AI Act (2024) — four risk tiers
- [x] SEC 2023 guidance on predictive data analytics / AI in investment advice
- [x] Didisheim et al. (2025) LLM memorized knowledge / data contamination
- [x] Liu et al. (2023) "lost in the middle"
- [x] Wei et al. (2022) chain-of-thought prompting
- [x] Retrieval-augmented generation (RAG)
- [x] LLM hallucination taxonomy (factual, attribution, reasoning)
- [x] Distributional hypothesis (Firth, 1957)
- [x] Textual signal definition
- [x] Bag-of-Words definition
- [x] One-hot encoding / discrete metric
- [x] TF-IDF definition (tf, idf, tfidf)
- [x] Word embedding definition
- [x] King analogy: vec(king) − vec(man) + vec(woman) ≈ vec(queen)
- [x] Autoregressive objective
- [x] Model selection heuristics (task type, data sensitivity, latency)

---

## Key Numbers

- [x] Harvard IV-4: ~11,000 word stems
- [x] Tetlock (2007): 1984–1999 WSJ data
- [x] LM dictionary: 6 tone categories
- [x] Word embedding typical dimension: d = 50–300; compression ~150–1000×
- [x] Transformer context dimension d = 768 or 1024
- [x] LLaMA: 7B–65B parameters
- [x] BloombergGPT: 50B parameters, 363B-token financial + 345B general corpus
- [x] GPT-3: 175B parameters
- [x] BERT: 12 or 24 layers; 15% masking
- [x] Negative sampling: K = 5–20 (small corpus), K = 2–5 (large)
- [x] GloVe: α = 0.75, x_max = 100
- [x] Vanishing gradient: 0.95^500 ≈ 5 × 10^{-12}
- [x] GloVe analogy queen: cosine similarity 0.67
- [x] API costs: gpt-4o $2.50/$10.00 per M tokens, gpt-4o-mini $0.15/$0.60, claude-sonnet $3.00/$15.00, claude-haiku $0.25/$1.25
- [x] Context windows: 10-K ~70K tokens, proxy statement ~120K, Basel III ~250K
- [x] EDGAR 10-K text growth: 1993–2023

---

## Figures

- [x] fig_edgar_text_growth.png — embedded on "Why financial text exploded" slide (lesson deck §02)
- [x] fig_king_analogy.png — embedded on PCA word-analogy slide (lesson deck §04) and word-analogy problem slide (practical deck §03)

---

## Omissions

All omissions listed below were filled during the deck overhaul:

- [x] §1 AI, Jobs, and Tasks section (entire) — added as Section 00
- [x] Li (2008) Fog Index readability — added to history section
- [x] LDA (Blei 2003) + Boudoukh 2013 + Hansen 2018 — added to history section
- [x] fig_edgar_text_growth embedded in lesson deck
- [x] fig_king_analogy embedded in lesson deck and practical deck
- [x] GloVe formal co-occurrence objective — added to main deck (not just appendix)
- [x] §6 RNN & LSTM — added as Section 05
- [x] §7 Attention & Transformer — added as Section 06
- [x] §8 LLM taxonomy — added as Section 07
- [x] §9 Python APIs — added as Section 08
- [x] §10 LLM Limitations & Regulatory — added as Section 09
- [x] MBA framing removed from both decks
