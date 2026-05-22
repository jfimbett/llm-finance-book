# Lecture 1: Introduction — Textual Analysis in Finance

**Paired chapter:** `book/chapters/01-intro/chapter.tex`

## Learning Objectives

By the end of this lecture, you should be able to:

1. Trace the evolution of textual analysis in finance from dictionary methods to transformer-based LLMs.
2. Construct and interpret bag-of-words and TF-IDF representations, and explain their core limitations.
3. Explain the distributional hypothesis and describe how Word2Vec and GloVe learn word embeddings from text.
4. Define a *textual signal* formally and identify the key identification challenges when using text to predict returns.

> *LLM API usage (querying OpenAI, Anthropic, HuggingFace in Python, reasoning about token costs and latency) is covered in Lecture 4 (LLM Agents) where it is the central practical topic.*

---

## 1. The Evolution of Textual Analysis in Finance

The story of text in finance begins with a spreadsheet. In autumn 2006, Paul Tetlock was staring at a column of daily negative-word fractions from the *Wall Street Journal*'s "Abreast of the Market" column on one side, and next-day Dow Jones returns on the other. The correlation was small — but it was there. According to the efficient markets hypothesis, it should not have been. Tetlock's 2007 *Journal of Finance* paper launched a field.

### 1.1 Dictionary Methods (1960s–2010s)

The roots go back further. In the 1960s, social scientists at Harvard developed *content analysis*: assign words to categories, count them, draw inferences. Their General Inquirer system (Stone et al., 1966) classified roughly 11,000 word stems into psychological categories such as Positive, Negative, Strong, and Weak.

Tetlock (2007) applied the Harvard IV-4 dictionary to predict DJIA returns. High media negativity predicts next-day price declines followed by a reversal — consistent with temporary sentiment-driven mispricing.

The critical problem: general-purpose dictionaries misclassify financial vocabulary. Loughran and McDonald (2011) showed that words like *tax*, *liability*, and *depreciation* are flagged as "negative" by Harvard IV-4, but are merely technical vocabulary in finance. Their Loughran–McDonald (LM) dictionary, built from hand-reading thousands of 10-K filings, substantially outperforms Harvard IV-4 in predicting filing-date abnormal returns.

**Key limitation of all dictionary methods:** They are static. Word order, negation, and syntax are all discarded. The sentence "earnings did *not* decline" receives the same score as "earnings *did* decline."

### 1.2 Statistical and Topic Models (2003–2013)

The NLP community moved toward statistical approaches that learn from data. Latent Dirichlet Allocation (LDA; Blei, Ng, Jordan 2003) represents each document as a mixture of latent *topics*, each in turn a distribution over vocabulary words. Topics are discovered from the corpus — no hand-crafted categories required.

Applied to finance: Boudoukh et al. (2013) applied LDA to firm-level news; Hansen, McMahon, and Prat (2018) applied it to FOMC transcripts, revealing structure invisible to dictionary counting.

**Still the same core limitation:** bag-of-words. Word order and syntax remain invisible.

### 1.3 The Neural Turn: Embeddings, RNNs, and Transformers (2013–present)

Word2Vec (Mikolov et al., 2013) changed the landscape by training shallow neural networks to predict a word from its context. The by-product: dense *embedding* vectors in which semantically similar words lie close together. "Equity" and "stock" end up near each other; $\text{king} - \text{man} + \text{woman} \approx \text{queen}$.

LSTM networks (Hochreiter & Schmidhuber, 1997) combined with embeddings brought sequential modelling — the ability to handle negation and long-range dependencies — to financial NLP benchmarks.

The Transformer (Vaswani et al., 2017) eliminated sequential processing via *self-attention*, allowing all tokens to interact in parallel. This design enabled pre-training on massive corpora and fine-tuning on small labelled datasets. BERT (Devlin et al., 2019) and FinBERT (Araci, 2019) set new benchmarks for financial sentiment classification. GPT-4, Claude, Gemini, and Llama — the models that are the subject of this book — are their direct descendants.

<!-- BOOK-ONLY: The LSTM cell-state dynamics and the vanishing-gradient bound are derived in Chapter 2 and are not required for this lecture. -->

---

## 2. Why Text Matters: The Financial Case

### 2.1 The Efficient Markets Hypothesis Reconsidered

Under the semi-strong EMH (Fama, 1970), prices fully reflect all publicly available information — so a text-based signal should be worthless. Yet a large empirical literature finds otherwise. Three non-mutually-exclusive explanations bridge the gap:

1. **Processing costs and limited attention.** Fully reading and interpreting a 100-page 10-K filing is costly. If only a fraction of investors do so, the information is not fully impounded. Textual signals are strongest for the longest, most complex documents.

2. **Soft information and interpretive disagreement.** Even widely-read documents can be ambiguous. A cautious management tone may reflect genuine uncertainty or strategic expectation management. If sophisticated investors disagree, no single interpretation is instantly priced.

3. **Latent information.** Regulation FD constrains what managers can say explicitly. Information still leaks through word choice, rhetorical structure, and what is omitted — none of which appear in GAAP figures.

### 2.2 Types of Financial Text

| Source | Frequency | Key feature |
|--------|-----------|-------------|
| Earnings call transcripts | Quarterly | Scripted + unscripted Q&A; spontaneous responses are especially informative |
| 10-K / 10-Q filings | Annual / quarterly | MD&A section, risk factors; can exceed 200 pages |
| Newswire / newspaper | Continuous | High frequency; narrow exploitation window |
| Analyst reports | Frequent | Dense information; complexity correlates with information asymmetry |
| Central bank communications | Irregular | FOMC minutes and statements move rates and equity prices on release |
| Social media | Continuous | Noisy; predictive power documented but robustness is debated |

### 2.3 The Textual Signal Framework

The history above illustrates a sequence of choices for how to turn a document into a number or vector. The abstract framework below unifies all these choices — from Tetlock's negative-word fraction to a GloVe embedding — under one definition.

We formalise what "text contains information" means.

Let $\mathcal{D}$ denote the space of documents. A **textual signal** is a measurable function

$$f \colon \mathcal{D} \to \mathbb{R}^k$$

mapping document $d_t$ to a $k$-dimensional signal $s_t = f(d_t)$. When $k=1$ the signal is a scalar (e.g., a sentiment score); when $k > 1$ it is a vector of topic proportions or an embedding.

The central empirical question: does the signal predict future excess returns $r_{t+1}$?

$$\mathrm{Cov}(s_t,\, r_{t+1}) \neq 0$$

Under a linear factor model:

$$r_{t+1} = \alpha + \beta^\top s_t + \varepsilon_{t+1}, \qquad \mathbb{E}[\varepsilon_{t+1} \mid s_t] = 0$$

The coefficient $\beta$ is economically significant if it survives controls for known predictors (size, value, momentum) and yields a Sharpe ratio exceeding transaction costs.

**Key identification challenges:**

- *Reverse causality* — documents may be written in response to lagged returns, not in anticipation of future ones.
- *Confounding* — macroeconomic conditions drive both tone and returns simultaneously.
- *Multiple testing* — with modern NLP one can generate thousands of signals; out-of-sample validation on a strict temporal split is essential.
- *Model misspecification* — the choice of $f$ (dictionary, topic model, LLM) is itself an assumption that affects the signal-to-noise ratio of $\hat{\beta}$.

**Four key empirical facts:**

1. Negative tone predicts negative short-run returns (Tetlock 2007).
2. Financial-domain dictionaries outperform general-domain ones (LM 2011).
3. Earnings call tone predicts future earnings surprises.
4. LLM-based signals (e.g., ChatGPT) show incremental predictive power over classical baselines (Lopez-Lira and Tang 2023).

---

## 3. Classical Text Representations

### 3.1 Vocabulary and the Bag-of-Words Model

**Pre-processing pipeline:** (1) case folding, (2) stop-word removal, (3) stemming or lemmatisation, (4) vocabulary truncation to the top $V'$ most frequent types.

The **bag-of-words (BoW)** representation maps each document $d$ to a count vector:

$$\mathbf{x}(d) = \bigl(\mathrm{count}(v_1, d), \ldots, \mathrm{count}(v_V, d)\bigr)^\top \in \mathbb{Z}_{\geq 0}^V$$

Word order is discarded. The term-document matrix for a corpus of $N$ documents is $\mathbf{X} \in \mathbb{Z}_{\geq 0}^{N \times V}$ — typically very sparse.

**One-hot encoding** represents each individual token as the $k$-th standard basis vector $\mathbf{e}_k \in \{0,1\}^V$. Every pair of distinct words is orthogonal: $\mathbf{e}_j^\top \mathbf{e}_k = \mathbb{1}[j = k]$. This encodes the false assumption that all words are equally (dis)similar — *revenue* and *sales* are as distant as *revenue* and *penguin*.

### 3.2 TF-IDF Weighting

Raw BoW counts are dominated by common words. TF-IDF addresses this by rewarding words that are frequent in this document but rare across the corpus:

$$\mathrm{tfidf}(v, d, \mathcal{C}) = \underbrace{\frac{\mathrm{count}(v,d)}{|d|}}_{\text{term frequency}} \times \underbrace{\log\!\left(\frac{|\mathcal{C}|}{\mathrm{df}(v,\mathcal{C})}\right)}_{\text{inverse document frequency}}$$

A word appearing in every document gets IDF $= \log(1) = 0$ — automatically suppressed. A word appearing in one document gets the highest IDF weight. Document similarity is measured by cosine similarity on $\ell_2$-normalised TF-IDF vectors.

<!-- BOOK-ONLY: The full three-document worked example computing TF-IDF and cosine similarity from scratch is in Section 3.3 of Chapter 1; it is suitable for problem sets but too detailed for a lecture slot. -->

**Fundamental limitations of BoW / TF-IDF:**

1. *Order invariance* — "earnings beat estimates" ≡ "estimates beat earnings."
2. *No semantic similarity* — synonyms (*revenue*, *sales*) have zero cosine similarity.
3. *Fixed vocabulary* — unseen terms at test time are silently discarded.
4. *High dimensionality* — $V \in [10\,000, 100\,000]$, mostly zeros; dense layers cannot consume these directly.

---

## 4. Word Embeddings

### 4.1 The Distributional Hypothesis

Classical one-hot encoding treats every word as equally distant from every other word. Word embeddings solve this by mapping each vocabulary item to a dense, low-dimensional vector so that semantically similar words are geometrically close.

The theoretical foundation is Firth's (1957) **distributional hypothesis**: *"You shall know a word by the company it keeps."* Words with similar meanings appear in similar contexts; learning contextual co-occurrence patterns thus approximates learning semantic similarity.

A **word embedding** of dimension $d$ is an injective map $\varphi : \mathcal{V} \to \mathbb{R}^d$ with $d \ll V$, stored as an embedding matrix $\mathbf{W} \in \mathbb{R}^{V \times d}$. Typical values: $d \in \{50, 100, 300\}$ for Word2Vec/GloVe versus $d = 768$ or $1024$ for Transformer-based contextual embeddings.

### 4.2 Word2Vec: Skip-Gram with Negative Sampling

Word2Vec frames embedding learning as a prediction task. The **Skip-Gram** variant trains each centre word to predict the words appearing in a context window of $\pm c$ positions around it.

The Skip-Gram objective maximises average log-likelihood over all centre–context pairs:

$$J_{\mathrm{SG}} = \frac{1}{T} \sum_{t=1}^{T} \sum_{\substack{k=-c \\ k \neq 0}}^{c} \log P(w_{t+k} \mid w_t)$$

Computing $P(w_{t+k} \mid w_t)$ via a softmax over the full vocabulary is expensive ($O(V)$ per step). **Negative sampling** replaces it with binary discrimination: distinguish the true context word from $K$ randomly sampled "noise" words. This reduces each gradient step to touching $K+1$ rows of the embedding matrix rather than all $V$ rows.

**What emerges:** linear analogical relationships.

$$\hat{\mathbf{v}}_{\text{king}} - \hat{\mathbf{v}}_{\text{man}} + \hat{\mathbf{v}}_{\text{woman}} \approx \hat{\mathbf{v}}_{\text{queen}}$$

In a financial corpus: $\hat{\mathbf{v}}_{\text{equity}} - \hat{\mathbf{v}}_{\text{dividend}} + \hat{\mathbf{v}}_{\text{coupon}} \approx \hat{\mathbf{v}}_{\text{bond}}$.

<!-- BOOK-ONLY: The full negative-sampling gradient derivations are in Section 4.2 of Chapter 1 and are suitable for students who want to implement the algorithm from scratch. -->

### 4.3 GloVe: Global Vectors for Word Representation

GloVe (Pennington, Socher, Manning 2014) takes a different route. It factorises the global word–word co-occurrence matrix $\mathbf{X}$ by minimising a weighted squared loss:

$$J_{\mathrm{GloVe}} = \sum_{i,j=1}^{V} f(X_{ij}) \Bigl(\mathbf{w}_i^\top \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij}\Bigr)^2$$

The weighting function $f$ down-weights very rare and very common co-occurrences. Word pairs that never co-occur contribute nothing to the sum.

GloVe and Word2Vec produce similar representations in practice. GloVe is faster when co-occurrence counts can be precomputed; Word2Vec scales more gracefully to streaming corpora.

### 4.4 Finance-Domain Embeddings

General embeddings trained on Wikipedia encode general-English meanings. The word *risk* maps to {danger, threat, hazard} in a general embedding but to {volatility, exposure, credit risk, drawdown} in one trained on SEC filings.

Finance-domain adaptation strategies:

1. **Domain-corpus pre-training** — train Word2Vec or GloVe from scratch on financial text (Bloomberg, 10-K filings, earnings calls).
2. **Fine-tuned transformer embeddings** — FinBERT further pre-trains BERT on Reuters news, 10-K filings, and earnings calls; its embeddings capture financial polysemy (*margin*, *return*, *position*).
3. **Retrofitting** — post-hoc adjustment using a financial ontology to pull synonyms together and push antonyms apart.

### 4.5 Case Study: PCA on Financial Vocabulary

We project 30 financial terms into two dimensions via PCA on their GloVe embedding vectors. Four semantic groups: rates & macro, equities & returns, risk concepts, corporate actions & derivatives.

Clusters that appear consistently across pre-trained models:

- *option*, *futures*, *derivative* → tight cluster (shared contextual vocab: premium, contract, expiry, strike).
- *default*, *credit* → cluster together; separated from equity-group terms.
- *merger*, *acquisition* → nearly identical vectors.
- *alpha*, *beta*, *factor* → cluster together (asset-pricing context).
- *yield*, *spread*, *inflation*, *interest rate* → most cohesive cluster (formulaic fixed-income language).

**Implementation:** `code/notebooks/01-intro/demo.ipynb`

<!-- BOOK-ONLY: The remark on PCA axis interpretability and the caveat about assigning domain-specific names to principal components without rigorous validation is in Section 4.5 of the book. -->

---

## 5. Looking Ahead

This lecture established the vocabulary and baseline methods that LLMs supersede. BoW discards order, one-hot encoding encodes no semantic similarity, and static embeddings are context-free. Each limitation motivates the next innovation — culminating in the Transformer architecture developed in Lecture 2.

**Lecture 2** derives recurrent architectures (RNN, LSTM), the attention mechanism, and the Transformer from first principles — the engine behind every large language model in finance today.

**Key papers to read before the next lecture:**

- Tetlock (2007) *Journal of Finance* — founding paper of media sentiment in finance
- Loughran and McDonald (2011) *Journal of Finance* — financial sentiment dictionaries
- Mikolov et al. (2013) — Word2Vec
- Pennington, Socher, Manning (2014) — GloVe
- Lopez-Lira and Tang (2023) — ChatGPT as a financial sentiment signal

---

## Further Reading

See Chapter 1 of the companion book for a deeper treatment, including the full TF-IDF worked example, Skip-Gram negative-sampling gradient derivations, GloVe co-occurrence matrix construction, and the PCA interpretability caveat.
