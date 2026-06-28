# Slide Coverage — Chapter 16: AI, Machine Learning, and Text in Finance

Source: `book/chapters/16-ai-ml-finance-text/chapter.tex`
Deck: `course/slides-html/16-ai-ml-finance-text/index.html`

---

## Concept Checklist

### Sections & Subsections
- [x] §1 Artificial Intelligence: Definitions and Scope
- [x] §1.1 From Expert Systems to Learning Machines
- [x] §1.2 Symbolic vs. Statistical AI
- [x] §2 The AI–ML–Deep Learning Hierarchy
- [x] §2.1 Machine Learning: Learning from Data
- [x] §2.2 Deep Learning: Representation at Scale
- [x] §2.3 Large Language Models as a Special Case
- [x] §3 AI Applications in Finance
- [x] §3.1 Decision-Making Under Uncertainty
- [x] §3.2 Forecasting, Risk, and Alpha Generation
- [x] §3.3 Regulatory Compliance and Fraud Detection
- [x] §4 The Textual Nature of Financial Data
- [x] §4.1 Structured vs. Unstructured Data in Finance
- [x] §4.2 Sources of Financial Text: Filings, News, Earnings Calls
- [x] §4.3 Why Text is Hard: Noise, Ambiguity, and Context
- [x] §5 From Bag-of-Words to Large Language Models
- [x] §5.1 Early NLP Approaches in Finance
- [x] §5.2 The Transformer Revolution
- [x] §5.3 Why LLMs are Particularly Suited to Finance
- [x] §6 Roadmap: What This Book Covers and How to Read It

### Named Methods / Models / Results
- [x] Expert systems ("if-then" rules; 1980s credit risk example)
- [x] AI effect / moving-target definition (Remark in §1.1)
- [x] Symbolic AI (Definition §1.2)
- [x] Statistical AI (Definition §1.2)
- [x] Finance hybrid: statistical backbone + deterministic compliance rule
- [x] Supervised learning (Definition §2.1): loss minimization, classification, regression
- [x] Unsupervised learning: clustering, market regimes
- [x] Reinforcement learning: algorithmic trading, portfolio rebalancing
- [x] Distribution shift (credit model on benign cycle → crisis failure)
- [x] Deep learning: universal approximation theorem (§2.2)
- [x] Hierarchical representation: lower layers general, higher layers task-specific
- [x] Transfer learning: pre-train broadly, fine-tune with fewer labels
- [x] Deep networks ↔ markets analogy (Context box §2.2)
- [x] Large Language Model (Definition §2.3): token, vocabulary, next-token objective
- [x] Emergent abilities (Wei et al., 2022)
- [x] In-context learning (few-shot, no parameter update)
- [x] BloombergGPT (Wu et al., 2023)
- [x] Reflexivity: AI systems as market actors, not observers
- [x] Deep RL market maker (Example §3.1)
- [x] Advances in Financial Machine Learning framework (Lopez de Prado, 2018)
- [x] Variance-covariance VaR: Gaussian assumption fails under stress
- [x] AML, sanctions screening, KYC, real-time fraud detection
- [x] EU AI Act + GDPR right to explanation
- [x] Structured data (Definition §4.1)
- [x] Unstructured data (Definition §4.1)
- [x] Processing bottleneck: tens of thousands of documents/day
- [x] SEC EDGAR: 10-K, 10-Q, 8-K; MD&A; Risk Factors; forward-looking statements
- [x] Loughran–McDonald (2011): 10-K sentiment predicts post-filing returns
- [x] Tetlock (2007): WSJ pessimistic language predicts downward pressure then mean-reversion
- [x] Earnings call research: content + tone, hedging, speech pace (Loughran–McDonald, 2020)
- [x] Context as first-class variable (Remark §4.3)
- [x] Bag-of-Words (BoW) + tf-idf weighting
- [x] BoW applied to filings since 1990s (Kearney & Liu, 2014)
- [x] Dictionary sentiment: Loughran–McDonald lexicon (~2,700 words, six categories)
- [x] Loughran–McDonald lexicon still a benchmark (Loughran–McDonald, 2020)
- [x] Latent Semantic Analysis (LSA) + Latent Dirichlet Allocation (LDA) / topic models
- [x] LSA/LDA: "operational efficiency vs. regulatory risk" earnings-call theme example
- [x] Shallow semantics limitation: context-independent, order-free
- [x] Vaswani et al. (2017) "Attention Is All You Need" — largest NLP transition
- [x] Self-attention: every position attends to every other position
- [x] Scaled dot-product attention formula: softmax(QK^T / sqrt(d_k)) V
- [x] sqrt(d_k) scaling: prevents softmax saturation / vanishing gradients
- [x] Multi-head attention: parallel subspaces (syntax, coreference)
- [x] Pre-trained transformers: BERT, GPT, RoBERTa
- [x] Transfer learning economics: thousands → hundreds of labeled examples
- [x] Four LLM properties suited to finance: long-document, in-context, world knowledge, NL interface
- [x] LLMs not a panacea: hallucination, prompt-sensitivity, opacity, calibration (Remark §5.3)
- [x] Book roadmap: Parts I–VI
- [x] Reading conventions: Context boxes, Deep Dive boxes, [B]/[I]/[A] exercises

### Key Numbers (all from chapter.tex)
- [x] 1956 — McCarthy coins "AI"
- [x] 1980s — expert systems era; 1990s — BoW applied to filings; mid-2000s — data-driven dominant
- [x] ~2,700 words — Loughran–McDonald lexicon
- [x] six categories — L-M lexicon (negative, positive, uncertainty, litigious, strong/weak modal)
- [x] 3/4 — Harvard-Inquirer "negative" words neutral/positive in filings
- [x] 50,000 word vocabulary → high-dimensional sparse document-term matrix
- [x] tens of thousands of documents/day — institutional processing bottleneck
- [x] 30% — Risk Factors grew YoY in worked example
- [x] eleven — CEO used "challenging" eleven times in worked example
- [x] &#36;1.20 beats &#36;1.15 — EPS example (escaped to avoid KaTeX parse)
- [x] billions of parameters; hundreds of billions of tokens — LLM scale (from Definition §2.3)
- [x] thousands of labeled examples → hundreds — transfer learning economics

### Citations (Author, year)
- [x] McCarthy (1956) — AI coined
- [x] Goodfellow et al. (2016) — deep learning textbook (universally cited in §2.1 and §2.2)
- [x] Lopez de Prado (2018) — Advances in Financial Machine Learning
- [x] Wei et al. (2022) — emergent abilities
- [x] Wu et al. (2023) — BloombergGPT
- [x] Loughran–McDonald (2011) — 10-K sentiment lexicon + stock return prediction
- [x] Loughran–McDonald (2020) — lexicon benchmark + earnings call NLP survey
- [x] Tetlock (2007) — WSJ language and market returns
- [x] Kearney & Liu (2014) — textual analysis survey; BoW in filings since 1990s
- [x] Vaswani et al. (2017) — "Attention Is All You Need"

---

## Omissions

*(All checklist items above are marked [x]. No omissions remain.)*

---

## Figure Coverage
- [x] `diagram.svg` embedded in lesson deck (`index.html`) — slide "AI ⊃ ML ⊃ DL ⊃ NLP ⊃ LLM: five boxes, one hierarchy" (Section 02)
- [x] `diagram.svg` embedded in practical deck (`practical.html`) — slide "The taxonomy we navigate today" (Section 01 Recap)

---

## Badge / Audience
- [x] "MBA-friendly" removed from both decks; badge reads "Summer school · math one click away…"

---

## Validator Results (P5)
- `index.html`: **OK**
- `practical.html`: **OK**
