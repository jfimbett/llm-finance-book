# Lecture 1: Introduction — From Text to Signals in Finance

**Paired chapter:** `book/chapters/01-intro/chapter.tex`
**Duration:** 2 hours
**Practical session:** `course/slides-html/01-intro/practical.html` (separate 1-hour session)

---

## Learning Objectives

By the end of this lecture, you should be able to:

1. Trace the evolution of textual analysis in finance from dictionary methods through statistical topic models to transformer-based LLMs, situating each generation in the research context that motivated it.
2. Explain why text-based return signals can coexist with approximate market efficiency, identifying the three main reconciling mechanisms.
3. State the formal definition of a textual signal, write out the linear factor model linking signals to returns, and identify the four main identification challenges in empirical evaluation.
4. Articulate the four fundamental limitations of classical bag-of-words methods; in the accompanying practical session, construct bag-of-words and TF-IDF representations from scratch for a small corpus and compute cosine similarity between documents.
5. Explain the distributional hypothesis and describe how Word2Vec (Skip-Gram with Negative Sampling) and GloVe learn word embeddings from co-occurrence statistics — including the key gradient updates and their interpretation.
6. Describe why finance-specific embeddings outperform general-purpose embeddings and name three strategies for domain adaptation.
7. Read and interpret a PCA projection of financial vocabulary embeddings, with appropriate caveats about axis interpretability.

---

## Part I: Why Text Matters in Finance

### 1.1 The Founding Moment

The story begins in 2006. Paul Tetlock, then a doctoral student, assembled a dataset: daily fractions of negative words in the *Wall Street Journal*'s "Abreast of the Market" column, running back to 1984, matched against next-day Dow Jones Industrial Average returns. The correlation was small — but it was there. And according to the textbooks on his shelf, it should not have been. If markets were semi-strong efficient in the sense of Fama (1970), the newspaper's sentiment should already be reflected in prices the moment the column was published.

Tetlock published his finding in the *Journal of Finance* (2007). It launched a field. The deeper insight is methodological: human language — the qualitative, messy, ambiguous prose of financial journalism — can be turned into a quantitative signal with genuine predictive content for asset prices.

**Key findings of Tetlock (2007):**
- High media negativity predicts *lower* next-day DJIA returns
- The effect *reverses* over the subsequent week (mean reversion to fundamental value)
- Unusually high or low negativity predicts high next-day trading volume
- Interpretation: temporary sentiment-driven mispricing, subsequently corrected

The reversal is the crucial piece. If the negative sentiment were purely informative about deteriorating fundamentals, there would be no subsequent recovery. The reversal indicates that sentiment is *temporarily depressing* prices below fundamental value — a mispricing that arbitrageurs eventually correct. This is the mechanism behind the textual signal, and it is fully consistent with markets being *approximately* efficient even if not perfectly so.

A companion paper by Tetlock, Saar-Tsechansky, and Macskassy (2008) extended this to firm-level news: negative-word fractions in Dow Jones Newswires stories predict short-run stock returns *and* subsequent quarterly earnings, with the earnings predictability concentrated in stories that directly discuss fundamentals. This established that media text contains information beyond what contemporaneous prices already reflect.

---

### 1.2 The Early History: Dictionary Methods (1960s–2010s)

The roots of textual analysis go back further, to social scientists at Harvard in the 1960s. Philip Stone and colleagues published the *General Inquirer* system (1966): a computer-assisted program matching words against hand-coded psychological and semantic dictionaries. The Harvard IV-4 dictionary classified roughly 11,000 word stems into categories such as Positive, Negative, Strong, Weak, Active, and Passive. Sentiment scoring was simple: count the words belonging to each category and normalise by document length. The appeal is transparency: every score can be explained by pointing to the words that generated it.

Tetlock (2007) applied Harvard IV-4 to WSJ financial columns. The method worked, but the dictionary was designed for *general* English prose. Loughran and McDonald (2011) exposed the problem: when applied to 10-K filings, words like *tax*, *liability*, *depreciation*, and *cost* were flagged as "negative." These are not negative in a financial context — they are technical vocabulary. Using Harvard IV-4 on financial filings introduces substantial measurement error.

In response, Loughran and McDonald built their own financial sentiment dictionary (LM dictionary) by hand-reading thousands of 10-K filings. Their six tone categories — Negative, Positive, Uncertainty, Litigious, Strong Modal, and Weak Modal — were calibrated for the financial register. Empirically, the LM Negative list substantially outperformed Harvard IV-4 in predicting filing-date abnormal returns, IPO underperformance, and earnings surprises.

**Fundamental limitation of all dictionary methods:** They are static. Word order, negation, and syntax are entirely discarded. "Earnings did *not* decline" receives the same score as "Earnings *did* decline" unless negation is explicitly handled — and even negation-aware heuristics remain fragile.

Researchers also developed *readability* measures for corporate disclosures. Li (2008) showed that annual reports measured as more difficult to read (by the Fog Index, based on sentence length and polysyllabic word fraction) are associated with *lower future earnings*, suggesting linguistic complexity may serve as obfuscation. This opened the door to a broader conception of what "textual information" means in finance.

---

### 1.3 Statistical and Neural Methods (2003–2019)

By the mid-2000s the NLP community had moved toward statistical representations that learn structure from data. *Latent Dirichlet Allocation* (LDA; Blei, Ng, and Jordan, 2003) represents each document as a mixture of latent *topics*, each a distribution over vocabulary words. Topics are discovered from the corpus without labelled data. Applied to finance: Boudoukh et al. (2013) analysed firm-level news; Hansen, McMahon, and Prat (2018) analysed FOMC transcripts, revealing structure invisible to dictionary counting. But LDA still treats documents as bags of words — word order and syntax remain invisible.

*Word2Vec* (Mikolov et al., 2013) and *GloVe* (Pennington et al., 2014) changed this by learning dense, low-dimensional word representations from distributional statistics — the topic of Section 3 of this lecture.

RNNs and LSTMs (Hochreiter and Schmidhuber, 1997) then enabled models to read a document sequentially, maintaining a hidden state summarising everything read so far. LSTM-based models achieved state-of-the-art performance on financial sentiment benchmarks in 2016–2018.

The *Transformer* architecture (Vaswani et al., 2017) introduced self-attention: for each token, a weighted average of all other tokens' representations, with weights learned to reflect relevance. This enabled training on far larger datasets than RNNs could accommodate and enabled *pre-training* — learning rich contextual representations from massive unlabelled corpora, then *fine-tuning* on small labelled datasets for specific tasks.

BERT (Devlin et al., 2019) exemplified this paradigm. FinBERT (Araci, 2019; Yang et al., 2020) applied it to finance, with substantially better sentiment classification accuracy on financial datasets than generic BERT. These are the direct antecedents of GPT-4, Claude, Gemini, and Llama — the models that form the subject of this course.

---

### 1.4 Sources of Financial Text

Financial text comes in several forms, each with distinct characteristics:

**Earnings call transcripts.** Quarterly calls in which management presents results and answers sell-side analyst questions. The scripted presentation is carefully prepared; the *Q&A section is spontaneous* and hence harder to rehearse and more information-rich. Davis et al. (2015) and a large subsequent literature show that transcript sentiment predicts abnormal returns and earnings surprises.

**10-K and 10-Q filings.** Annual (10-K) and quarterly (10-Q) SEC filings contain MD&A, risk factor disclosures, and financial statements. 10-K filings can exceed 200 pages — a major information-extraction challenge that NLP is well-placed to address. The primary data source in Loughran–McDonald (2011).

**Newswire and newspaper articles.** Tetlock (2007) worked with WSJ columns. A larger body of work uses Reuters or Bloomberg newswire feeds. Key feature: *high frequency*. Material news triggers immediate repricing, so the window for exploiting a textual signal is narrow. The value of NLP lies partly in speed (classifying thousands of articles per second) and partly in breadth (aggregating across many sources simultaneously).

**Analyst reports.** Sell-side research combines quantitative analysis with specialist narrative commentary. Lehavy, Li, and Merkley (2011) show that textual complexity in analyst reports is associated with greater investor uncertainty and information asymmetry.

**Central bank communications.** FOMC minutes, ECB statements, and Bank of England communications move interest rates and equity prices when published. Hansen, McMahon, and Prat (2018) used LDA on FOMC transcripts (publicly available with a 5-year lag) to study deliberation and market effects.

**Social media and alternative data.** Twitter/X, Reddit's r/wallstreetbets, StockTwits. Bollen, Mao, and Zeng (2011) showed aggregate Twitter mood states predict DJIA returns — though subsequent work questions robustness. Key challenges: bot activity, sarcasm, slang, and mixing of retail and institutional sentiment.

---

### 1.5 Why Text Signals Survive in Efficient Markets

The semi-strong form of the efficient markets hypothesis (Fama, 1970) holds that prices fully reflect all publicly available information. Under strict semi-strong efficiency, reading an earnings call transcript provides no trading advantage. Yet a large empirical literature documents predictive content in financial text. Three non-mutually-exclusive mechanisms reconcile textual predictability with approximate market efficiency:

**1. Processing costs and limited attention.** Markets aggregate information through the trading of many investors, each with limited attention and cognitive capacity. If processing a 200-page 10-K requires substantial effort and only a small fraction of investors performs that analysis, prices may not immediately reflect all information the filing contains. Once cheap NLP tools make processing feasible at scale, the anomaly should attenuate — and indeed textual signals tend to be most powerful for documents that are longest, most complex, and hence most costly to process (Li, Lundholm, and Minnis, 2013).

**2. Soft information and interpretive disagreement.** Even when a document is widely read, its implications may be ambiguous. A cautious management tone might reflect genuine uncertainty about business conditions *or* strategic expectation management designed to lower analyst forecasts before the next earnings announcement. If sophisticated investors disagree about the correct interpretation, prices reflect an average of beliefs, and no single interpretation is instantly impounded. NLP tools that classify the *degree* of hedging or strategic obfuscation can extract a signal not already priced.

**3. Latent information.** Corporate disclosures are constrained by regulation (Regulation FD in the US context limits selective disclosure of material non-public information). Information may be conveyed *implicitly* through word choice, rhetorical structure, and what is *omitted* rather than stated. Analysing the tone, readability, or linguistic complexity of a disclosure can extract this latent signal even when the explicit content is already known.

> Under any of these accounts, textual analysis adds value not because markets are irrational, but because *information extraction from text is genuinely costly* and the technology for doing it at scale has improved dramatically. LLMs represent the latest — and most powerful — step in that progression.

---

### 1.6 Formal Framework: The Textual Signal

**Definition (Textual Signal).** Let $\mathcal{D}$ denote the space of documents (finite sequences of tokens from vocabulary $\mathcal{V}$). Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space. A *textual signal* is a measurable function:
$$f : \mathcal{D} \to \mathbb{R}^k$$
mapping document $d_t$ observed at time $t$ to signal value $s_t = f(d_t) \in \mathbb{R}^k$.

When $k=1$, $s_t$ is a scalar sentiment score. When $k > 1$, it is a vector of topic proportions, an embedding in $\mathbb{R}^{768}$, or the output of a classifier head over discrete categories.

The central empirical question is whether the signal has forecasting content:
$$\text{Cov}(s_t,\, r_{t+1}) \neq 0$$

where $r_{t+1}$ is the excess return over $[t, t+1]$. If this covariance is non-zero, a long–short strategy that takes positions proportional to $s_t$ earns a non-zero expected return in a linear projection model.

**The linear factor model:**
$$r_{t+1} = \alpha + \beta^\top s_t + \varepsilon_{t+1}, \qquad \mathbb{E}[\varepsilon_{t+1} \mid s_t] = 0$$

The signal is *economically significant* if $|\beta| > 0$ after controlling for known return predictors (size, value, momentum, and so forth), and if the associated Sharpe ratio exceeds plausible transaction costs. Both conditions are necessary: statistical significance without economic significance is not useful.

The rest of this course can be read as an investigation of the best choice of $f$: from simple word counts, to topic models, to transformer embeddings, to instruction-tuned LLMs used as zero-shot classifiers or reasoning agents.

---

### 1.7 Identification Challenges

Establishing $\text{Cov}(s_t, r_{t+1}) \neq 0$ is *necessary but not sufficient* for claiming the signal is causally informative about future returns:

**Reverse causality.** The document $d_t$ may be written *in response to* lagged returns rather than in anticipation of future ones. A pessimistic earnings call might reflect a poor quarter already priced in. One must identify the component of $s_t$ that is not predictable from public information already in prices.

**Confounding.** Macroeconomic conditions simultaneously affect the tone of news coverage and asset returns. A negative correlation between negativity and returns may simply reflect a common dependence on the business cycle. Standard practice: control for contemporaneous return, volatility, and macro variables; use high-frequency event studies where the information release time is known precisely.

**Overfitting and multiple testing.** With modern NLP tools one can construct an enormous number of candidate signals from the same corpus. Without correction for multiple testing or out-of-sample validation, spurious correlations are likely. Best practice: strict temporal split (train on pre-2010, evaluate on post-2010) rather than in-sample $t$-statistics.

**Model misspecification.** The mapping $f$ is itself an assumption. Dictionary-based $f$ imposes strong restrictions (only word counts matter). LLM-based $f$ relaxes these restrictions but introduces its own assumptions (training data distribution, fine-tuning objective, prompt design). The empirical signal-to-noise ratio of $\hat{\beta}$ depends on how well $f$ captures the true information in the document.

---

### 1.8 Key Empirical Regularities

Four stylised facts from the literature anchor the formal framework:

1. **Negative tone predicts negative returns (short-run), with reversal.** Tetlock (2007): more pessimistic WSJ prose → lower next-day DJIA returns, with reversion over the subsequent week.

2. **Financial-domain dictionaries outperform general-domain ones.** Loughran–McDonald (2011): the LM Negative list substantially outperforms Harvard IV-4 in predicting filing-date abnormal returns, IPO underperformance, and earnings surprises.

3. **Earnings call tone predicts future earnings surprises.** Larcker and Zakolyukina (2012): linguistic characteristics of CEO and CFO speech on earnings calls contain information about the accuracy of disclosed earnings; deceptive speech has distinct linguistic markers.

4. **LLM-based signals show incremental predictive power.** Lopez-Lira and Tang (2023): ChatGPT-generated sentiment scores for news headlines predict next-day stock returns with a positive-coefficient pattern. This predictability is *absent* for smaller, less capable predecessors (GPT-1, BERT — a transformer-based encoder model introduced formally in Lecture 2), suggesting it is an *emergent property of scale*.

---

## Part II: Classical Text Representations

Classical methods remain competitive baselines in many financial applications. More importantly for this course, neural methods such as self-attention can be understood as learning, dynamically, context-dependent analogues of the static representations described here.

### 2.1 Tokenisation and the Preprocessing Pipeline

**Definitions.** A *corpus* $\mathcal{C} = \{d_1, \ldots, d_N\}$ is a collection of $N$ documents. Each document is a sequence of *tokens* from vocabulary $\mathcal{V}$ of size $V$. *Tokenisation* converts a raw character string into a sequence of tokens.

Standard preprocessing steps:

1. **Case folding.** Lowercase all tokens: "Revenue" → "revenue".
2. **Stop word removal.** Remove high-frequency function words ("the", "and", "of", ...). Standard lists contain 100–300 words. In financial NLP, researchers sometimes also remove common financial jargon ("company", "year", "quarter") that appears in nearly every document.
3. **Stemming and lemmatisation.** Apply *stemming* (rule-based suffix stripping: earnings, earned, earns → earn) or *lemmatisation* (dictionary-based mapping to canonical lemma: better → good). Lemmatisation is linguistically more accurate but slower. Both reduce $V$ and increase effective document frequency of important terms.
4. **Vocabulary truncation.** Retain only the $V'$ most frequent types. Very rare words are either noise or proper nouns with document-specific meaning.

Modern LLMs use *sub-word tokenisation*: "earnings" might tokenise to ["earn", "ings"], allowing rare words to be represented as combinations of frequent sub-units. For the classical methods in this section, word-level tokenisation is standard.

---

### 2.2 Bag-of-Words Model

**Definition (Bag-of-Words).** Let $\mathcal{V} = \{v_1, \ldots, v_V\}$ be an ordered vocabulary. The *bag-of-words* (BoW) representation of document $d$ is:
$$\mathbf{x}(d) = \bigl(\text{count}(v_1, d),\, \text{count}(v_2, d),\, \ldots,\, \text{count}(v_V, d)\bigr)^\top \in \mathbb{Z}_{\geq 0}^V$$

The BoW representation discards sequential order entirely — it treats the document as an unordered multiset of word occurrences. "The fund outperformed the market" and "the market outperformed the fund" have *identical* BoW representations.

The BoW matrix for a corpus $\mathcal{C}$ of $N$ documents is the *term-document matrix* $\mathbf{X} \in \mathbb{Z}_{\geq 0}^{N \times V}$. For large vocabularies and corpora, $\mathbf{X}$ is very sparse: most documents use a small fraction of the full vocabulary. Sparse matrix formats (CSR, CSC) are used in practice.

---

### 2.3 One-Hot Encoding and Its Limitations

**Definition (One-Hot Vector).** The *one-hot encoding* of token $v_k \in \mathcal{V}$ is:
$$\mathbf{e}_k = (0, \ldots, 0, \underbrace{1}_{k\text{-th}}, 0, \ldots, 0)^\top \in \{0,1\}^V$$

A document's BoW vector equals the sum of its constituent tokens' one-hot vectors: $\mathbf{x}(d) = \sum_{j=1}^n \mathbf{e}_{k(w_j)}$.

**Two critical geometric properties:**
- Unit $\ell_2$ norm: $\|\mathbf{e}_k\|_2 = 1$ for all $k$
- Orthogonality: $\mathbf{e}_j^\top \mathbf{e}_k = \mathbb{1}[j=k]$

The orthogonality property encodes the implicit assumption that every pair of distinct words is *equally dissimilar*. The cosine similarity between "revenue" and "income" is zero — identical to the similarity between "revenue" and "penguin." A financial analyst knows these words are nearly synonymous in most contexts; the one-hot representation has no way to encode this.

The metric structure induced on the vocabulary by one-hot cosine similarity is the *discrete metric*: $\text{sim}(v_j, v_k) = \mathbb{1}[j=k]$. This is a profound limitation because much of the value of language lies precisely in *partial* similarities between words. Word embeddings replace this discrete metric with a continuous one reflecting distributional similarity.

For vocabulary size $V \in [10{,}000,\, 100{,}000]$, the representation is extremely high-dimensional. Only one entry per token is non-zero; the vectors are $(1 - 1/V)$-sparse. This sparsity makes computation feasible via sparse linear algebra but makes the features unsuitable as inputs to dense neural network layers without dimensionality reduction.

---

### 2.4 TF-IDF Weighting

Raw BoW counts are dominated by common words. In a corpus of 10-K filings, "the" appears in every document and contributes nothing to distinguishing them. TF-IDF addresses this by down-weighting words that appear frequently across the corpus.

**Definitions:**

*Term Frequency*: the normalised count of token $v$ in document $d$:
$$\text{tf}(v, d) = \frac{\text{count}(v, d)}{|d|}$$

*Document Frequency* of token $v$: number of documents in which $v$ appears at least once.

*Inverse Document Frequency*:
$$\text{idf}(v, \mathcal{C}) = \log\!\left(\frac{|\mathcal{C}|}{\text{df}(v, \mathcal{C})}\right)$$

A smoothed variant adds 1 to the denominator: $\text{idf}_{\text{smooth}} = \log\!\left(\frac{|\mathcal{C}|}{1 + \text{df}(v, \mathcal{C})}\right) + 1$.

*TF-IDF weight*:
$$\text{tfidf}(v, d, \mathcal{C}) = \text{tf}(v, d) \times \text{idf}(v, \mathcal{C})$$

**Intuition.** IDF acts as an automatic stop-word suppressor. A word in every document has $\text{df} = |\mathcal{C}|$, so $\text{idf} = \log(1) = 0$ and its TF-IDF weight is zero regardless of frequency. A word in only a few documents receives a high IDF, and if also frequent in those documents, a high TF-IDF — signalling it is *characteristic* of those documents.

**Document similarity.** TF-IDF vectors are $\ell_2$-normalised before computing cosine similarity:
$$\text{sim}(d_i, d_j) = \frac{\tilde{\mathbf{x}}(d_i)^\top \tilde{\mathbf{x}}(d_j)}{\|\tilde{\mathbf{x}}(d_i)\|_2\, \|\tilde{\mathbf{x}}(d_j)\|_2}$$

This lies in $[0,1]$ for non-negative TF-IDF vectors and is invariant to document length. This is the foundation of the classic vector space model in information retrieval (Salton, Wong, and Yang, 1975).

**Worked example** (from the book chapter). Consider the corpus $\{d_1: \text{revenue grew strong earnings},\ d_2: \text{earnings declined weak guidance},\ d_3: \text{revenue guidance raised strong}\}$ with vocabulary $V = 8$. Words appearing in only one document (declined, grew, raised, weak) receive $\text{idf} = \ln(3) \approx 1.099$; words in two documents (earnings, guidance, revenue, strong) receive $\text{idf} = \ln(3/2) \approx 0.405$. The cosine similarity $\text{sim}(d_1, d_3) \approx 0.213$ correctly captures their shared positive vocabulary; $\text{sim}(d_1, d_2) \approx 0.106$ correctly reflects minimal overlap between the optimistic $d_1$ and negative $d_2$. See the practical session for a hands-on computation.

---

### 2.5 Limitations of Classical Methods

1. **Order invariance.** The representation is unchanged by permuting words. "Earnings beat estimates" and "estimates beat earnings" have identical BoW/TF-IDF vectors.

2. **No semantic similarity.** Synonymous words that never co-occur ("revenue", "sales") have zero cosine similarity in TF-IDF space.

3. **Fixed vocabulary.** Words not seen at training time — new acronyms, company names — are out-of-vocabulary and discarded.

4. **High dimensionality and sparsity.** For large corpora $V$ can be hundreds of thousands. Even with IDF weighting, vectors are high-dimensional and sparse — unsuitable as direct inputs to dense neural layers.

These limitations motivate word embeddings: replacing the discrete, high-dimensional one-hot basis with a continuous, low-dimensional space where semantically similar words are geometrically close.

---

## Part III: Word Embeddings

### 3.1 The Distributional Hypothesis

The theoretical foundation of word embeddings is the *distributional hypothesis*, articulated by J.R. Firth (1957):

> "You shall know a word by the company it keeps."

Words that appear in similar contexts have similar meanings, so a representation built on co-occurrence patterns captures semantic similarity.

Recall that one-hot encoding has two critical deficiencies:
1. For $V = 50{,}000$, each word is a 50,000-dimensional vector with a single non-zero entry — extremely sparse.
2. Every pair of one-hot vectors is orthogonal: no semantic relatedness is encoded.

A word embedding replaces these sparse, semantically blind vectors with dense, semantically rich ones.

---

### 3.2 Word Embedding: Definition and Geometry

**Definition (Word Embedding).** Let $\mathcal{V}$ be a vocabulary of size $V$. A *word embedding* of dimension $d$ is an injective map:
$$\varphi : \mathcal{V} \to \mathbb{R}^d, \quad d \ll V$$

The *embedding matrix* $\mathbf{W} \in \mathbb{R}^{V \times d}$ has $\varphi(w_i)$ as its $i$-th row. Retrieving the embedding of word $w_i$ is the matrix–vector product $\mathbf{W}^\top \mathbf{e}_{w_i}$ (selecting the $i$-th row).

Typical dimensions: $d = 50$ (GloVe-50) to $d = 300$ (GloVe-300, Word2Vec) to $d = 768$ or $d = 1024$ for transformer contextual embeddings. Compression ratio: $V/d \approx 150$–$1{,}000$.

**Geometric power.** Under a well-trained embedding:
- Cosine similarity between vectors reflects semantic distance
- *Linear analogies* emerge: $\varphi(\text{king}) - \varphi(\text{man}) + \varphi(\text{woman}) \approx \varphi(\text{queen})$
- In a financial corpus: $\varphi(\text{call option}) - \varphi(\text{upside}) + \varphi(\text{downside}) \approx \varphi(\text{put option})$

These linear regularities arise because the embedding must be consistent with patterns of co-occurrence: if "king" and "queen" share the same contextual environments except for gender-related words, their difference captures a gender direction.

---

### 3.3 Word2Vec: Skip-Gram with Negative Sampling

Word2Vec (Mikolov et al., 2013) operationalises the distributional hypothesis by framing embedding learning as a supervised prediction task. The *Skip-Gram* variant trains each centre word to predict the words appearing in a window of $\pm c$ positions around it.

Each word $w \in \mathcal{V}$ gets two vectors: a *centre-word* vector $\hat{\mathbf{v}}_w \in \mathbb{R}^d$ (used when $w$ is the target) and a *context-word* vector $\mathbf{v}_w \in \mathbb{R}^d$ (used when $w$ is in context). This two-vector convention simplifies the mathematics; after training, typically the context vectors are discarded or the two sets are averaged.

**The softmax probability** of observing context word $w_{t+k}$ given centre word $w_t$:
$$P(w_{t+k} \mid w_t) = \frac{\exp(\mathbf{v}_{w_{t+k}}^\top \hat{\mathbf{v}}_{w_t})}{\sum_{w=1}^V \exp(\mathbf{v}_w^\top \hat{\mathbf{v}}_{w_t})}$$

**The Skip-Gram objective** maximises average log-likelihood over all centre–context pairs in a corpus of $T$ tokens:
$$J_{\text{SG}} = \frac{1}{T} \sum_{t=1}^T \sum_{\substack{k=-c \\ k \neq 0}}^{c} \log P(w_{t+k} \mid w_t)$$

**The computational problem:** The normalising constant sums over all $V \approx 10^4$–$10^5$ words at *every* gradient step. For 1 billion tokens this is prohibitively expensive.

**Negative Sampling (NEG):** Replace the full softmax with a binary classification task — distinguish the observed context word (one positive sample) from $K$ words drawn from a noise distribution $P_n$ (negative samples). The NEG objective for a single pair $(w_t, w_{t+k})$:
$$\mathcal{L}_{\text{NEG}}(w_t, w_{t+k}) = \log \sigma(\mathbf{v}_{w_{t+k}}^\top \hat{\mathbf{v}}_{w_t}) + \sum_{j=1}^K \mathbb{E}_{w_j \sim P_n}\bigl[\log \sigma(-\mathbf{v}_{w_j}^\top \hat{\mathbf{v}}_{w_t})\bigr]$$

where $\sigma(x) = (1 + e^{-x})^{-1}$ is the logistic sigmoid. Recommended: $K = 5$–$20$ for small corpora, $K = 2$–$5$ for large corpora; $P_n(w) \propto \text{freq}(w)^{3/4}$.

**Gradient interpretation.** Update for the positive context vector:
$$\frac{\partial \mathcal{L}_{\text{NEG}}}{\partial \mathbf{v}_{w_{t+k}}} = \bigl[1 - \sigma(\mathbf{v}_{w_{t+k}}^\top \hat{\mathbf{v}}_{w_t})\bigr]\,\hat{\mathbf{v}}_{w_t}$$

When the two vectors are dissimilar ($\sigma(\cdot)$ is small), the coefficient is large, pushing the positive context vector *toward* the centre vector. Each negative sample's vector is pushed *away*:
$$\frac{\partial \mathcal{L}_{\text{NEG}}}{\partial \mathbf{v}_{w_j}} = -\sigma(\mathbf{v}_{w_j}^\top \hat{\mathbf{v}}_{w_t})\,\hat{\mathbf{v}}_{w_t}$$

Each gradient step touches only $K+1$ rows of the embedding matrix — not all $V$ rows — making training extremely efficient.

---

### 3.4 GloVe: Global Vectors for Word Representation

Whereas Word2Vec processes one context window at a time, GloVe (Pennington, Socher, and Manning, 2014) directly factorises the *global word–word co-occurrence matrix*.

**Definition (Co-occurrence Matrix).** For corpus of $T$ tokens, vocabulary $\mathcal{V}$ of size $V$, and context window of half-width $c$:
$$X_{ij} = \sum_{t=1}^T \sum_{\substack{k=-c \\ k \neq 0}}^c \mathbf{1}[w_t = w_i]\,\mathbf{1}[w_{t+k} = w_j]$$

**Key theoretical insight:** The *ratio* of co-occurrence probabilities $P_{ik}/P_{jk}$ encodes relational meaning more faithfully than raw probabilities. GloVe learns vectors $\mathbf{w}_i, \tilde{\mathbf{w}}_j \in \mathbb{R}^d$ and biases $b_i, \tilde{b}_j$ by minimising:
$$J_{\text{GloVe}} = \sum_{i,j=1}^V f(X_{ij})\Bigl(\mathbf{w}_i^\top \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij}\Bigr)^2$$

The weighting function down-weights both rare and very frequent co-occurrences:
$$f(x) = \begin{cases} (x/x_{\max})^\alpha & x < x_{\max} \\ 1 & \text{otherwise} \end{cases}$$

Recommended: $\alpha = 0.75$, $x_{\max} = 100$. Pairs with $X_{ij} = 0$ contribute nothing.

**Comparison with Word2Vec:** GloVe is a single-pass weighted least-squares problem over the co-occurrence matrix (assembled once); Word2Vec uses online SGD without materialising the full matrix. GloVe tends to be faster when co-occurrence counts can be precomputed; Word2Vec scales better to streaming corpora. Both produce embeddings of similar quality in practice.

---

### 3.5 Finance-Specific Embeddings and Domain Adaptation

General-purpose embeddings trained on Wikipedia or Common Crawl encode general-English meanings, which differ substantially from technical financial meanings:

| Word | General English nearest neighbours | Finance-domain nearest neighbours |
|------|-----------------------------------|-----------------------------------|
| risk | danger, threat, hazard, peril | volatility, variance, exposure, drawdown, VaR |
| short | brief, abbreviated, concise | short-sell, short position, bear |
| margin | edge, border, margin | profit margin, maintenance margin, leverage |

Three domain adaptation strategies:

1. **Domain-corpus pre-training.** Train Word2Vec/GloVe from scratch on large financial corpora (SEC filings, Bloomberg articles, earnings call transcripts). Bloomberg Financial Word2Vec and FinancialPhraseBank embeddings are examples.

2. **Fine-tuned transformer embeddings.** FinBERT (Yang et al., 2020) is BERT further pre-trained on Reuters news, 10-K filings, and earnings calls. Its token embeddings capture the financial sense of polysemous terms such as "margin", "return", and "position".

3. **Retrofitting.** Post-hoc adjustment of a general embedding using a domain-specific lexicon or knowledge graph to pull synonymous terms together and push antonyms apart — without retraining from scratch.

---

### 3.6 Case Study: PCA on Financial Vocabulary

Projecting 30 financial terms' embedding vectors into 2D via PCA reveals domain-specific semantic structure. The terms span four semantic groups: rates & macro (yield, spread, inflation, central bank, interest rate); equities & returns (equity, dividend, earnings, revenue, profit, loss, alpha, beta, factor, return, sentiment); risk concepts (volatility, risk, default, credit, liquidity, leverage, portfolio, hedge); corporate actions & derivatives (option, futures, derivative, merger, acquisition).

**Consistent patterns across pre-trained models:**
- "option", "futures", "derivative" form a tight cluster (shared contextual vocabulary: premium, contract, expiry, strike)
- "default" and "credit" cluster together, distant from equity-group terms (consistent with the credit/equity divide)
- "merger" and "acquisition" are nearly synonymous, mapping to almost identical vectors
- "alpha", "beta", "factor" cluster together (shared origin in asset-pricing literature)
- The rates cluster ("yield", "spread", "inflation", "interest rate", "central bank") is the most cohesive, reflecting the highly formulaic language of fixed-income analysis

**Important caveat on axis interpretation.** The PCA axes $\mathbf{p}_1, \mathbf{p}_2$ are not directly interpretable as named financial concepts — they are linear combinations of 300 embedding dimensions that explain the most variance *among the 30 selected terms*. A different term selection produces different axes. Resist assigning domain-specific names to the $x$- and $y$-axes without rigorous validation. Rotation methods (Varimax) and supervised probing classifiers offer more principled approaches to identifying interpretable directions.

Full implementation: `code/practicals/01-intro/practical.ipynb`.

---

## Wrap-Up and Looking Ahead

**This lecture has covered:**
- Why text matters in finance: processing costs, soft information, and latent content; formal signal framework; four identification challenges; four empirical regularities
- Classical representations: BoW, one-hot encoding, TF-IDF — powerful baselines, but fundamentally limited by order invariance and the discrete metric of one-hot vectors
- Word embeddings: distributional hypothesis; Word2Vec Skip-Gram with Negative Sampling (objectives and gradient updates); GloVe (global co-occurrence factorisation); domain adaptation strategies; PCA case study

**All of these approaches treat language as bags of tokens or low-dimensional geometric objects.** They capture lexical similarity but cannot model syntax, long-range dependencies, or the meaning of a word in context.

**Lecture 2 (LLM Foundations)** addresses these limitations directly:
- Recurrent architectures (RNNs) that brought sequential order into text modelling
- Why vanishing gradients prevented deep sequence learning — and how LSTMs fix this
- The scaled dot-product attention mechanism and the Transformer
- Pre-training objectives: masked language modelling (BERT) vs. autoregressive next-token prediction (GPT)
- The practical layer: temperature and structured decoding, retrieval-augmented generation, model compression, and hallucination measurement

<!-- BOOK-ONLY: Full derivation of the vanishing-gradient bound for vanilla RNNs and the complete LSTM cell state equations with all four gate formulas are developed at depth in the book chapter but constitute preview material for the lecture sequence. -->

---

**Key References**
- Tetlock (2007) — Giving Content to Investor Sentiment, *Journal of Finance*
- Loughran and McDonald (2011) — When Is a Liability not a Liability?, *Journal of Finance*
- Blei, Ng, Jordan (2003) — Latent Dirichlet Allocation, *JMLR*
- Mikolov et al. (2013) — Efficient Estimation of Word Representations in Vector Space, *ICLR Workshop*
- Pennington, Socher, Manning (2014) — GloVe, *EMNLP*
- Lopez-Lira and Tang (2023) — Can ChatGPT Forecast Stock Price Movements?, *Review of Finance*
