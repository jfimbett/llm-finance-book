# Lecture 2: Large Language Models — Architecture and Practice

**Course:** Large Language Models in Finance  
**Institution:** Paris Dauphine — PSL University  
**Instructor:** Juan F. Imbet  
**Duration:** 2 hours

---

## Learning Objectives

By the end of this lecture, students should be able to:

1. Explain the three standard document-level representation strategies (mean embedding, TF-IDF weighted embedding, Sentence-BERT) and identify when each is appropriate for financial text.
2. Derive the vanishing-gradient bound for vanilla RNNs and explain how the LSTM cell state resolves it through additive updates.
3. State the LSTM's six gated equations, interpret each gate in a financial-text context, and compare the GRU as a parameter-efficient alternative.
4. Derive the scaled dot-product attention formula, prove why dividing by $\sqrt{d_k}$ stabilises softmax gradients, and describe how multi-head attention and sinusoidal positional encoding extend the mechanism.
5. Contrast BERT's masked language modelling objective with GPT's causal language modelling objective and match each architecture type to appropriate downstream tasks.
6. Navigate the modern LLM landscape — including FinBERT, BloombergGPT, and reasoning models — and apply appropriate financial benchmarks for evaluation.
7. Design a production-ready pipeline combining the correct sampling strategy, structured generation, RAG, and hallucination-mitigation techniques for a given financial NLP task.

---

## Section 1 — From Words to Documents

Lecture 1 introduced word embeddings: dense vectors that capture distributional semantics at the token level. Financial applications rarely operate at the word level. An earnings-call transcript contains thousands of tokens. A 10-K filing may contain hundreds of thousands. A news headline is ten words. The natural unit of analysis is the document or the passage, and we need aggregation strategies that produce a fixed-size vector from a variable-length token sequence.

Three strategies are in widespread use, each with a distinct accuracy-cost profile.

The simplest is the mean embedding. Given a document $d = (w_1, \ldots, w_n)$ and an embedding function $\varphi$, the mean embedding is:

$$
\bar{\varphi}(d) = \frac{1}{n} \sum_{i=1}^{n} \varphi(w_i)
$$

This is algebraically a bag-of-words model: swapping the order of any two tokens does not change the mean. The mean embedding of "the company did not meet earnings expectations" is identical to the mean embedding of "earnings expectations met the company not did" — a garbled sentence with the same words but no meaning. The practical implications are significant: negations, conditional clauses, and temporal reasoning all require word order, and none of it survives averaging.

TF-IDF weighted averaging addresses the equal-weight problem by scaling each token's contribution by its term frequency–inverse document frequency weight:

$$
\varphi_{\text{tfidf}}(d) = \frac{\sum_{i=1}^{n} \text{tfidf}(w_i, d)\,\varphi(w_i)}{\sum_{i=1}^{n} \text{tfidf}(w_i, d)}
$$

Domain-specific terms such as "EBITDA", "covenants", or "contango" receive high weights; generic terms such as "the" receive low weights. The resulting embedding is more discriminative on financial text classification tasks than the unweighted mean, though it still discards word order.

Sentence-BERT (SBERT) represents the state of the art for contextual document embeddings without requiring full LLM inference at query time. Standard BERT produces contextual token representations, but averaging those representations at the document level performs surprisingly poorly for semantic similarity. SBERT addresses this by fine-tuning a BERT encoder on a Natural Language Inference objective using a Siamese architecture: two weight-sharing encoders process a sentence pair, and the model learns to produce embeddings where semantically similar sentences have high cosine similarity. The key operational advantage is that SBERT embeddings can be pre-computed and indexed; semantic search over a corpus of $N$ documents then requires only one forward pass per document plus an approximate nearest-neighbour lookup at query time, rather than $N$ separate forward passes.

A critical practical constraint for all BERT-based models is the context-window limit (typically 512 tokens for standard BERT, 4096 or more for long-context variants). Long financial documents require one of three strategies: truncation (only the first 512 tokens are encoded), chunking (the document is split into overlapping windows and chunk embeddings are aggregated), or hierarchical encoding (sentences are encoded individually and a second-level encoder aggregates sentence embeddings). The right choice depends on where material information is located in the document and on the available compute budget.

<!-- BOOK-ONLY: The proof that mean embedding equals a BoW linear projection through the embedding matrix (Proposition 1 in the chapter) is mathematically clean but adds five minutes to the lecture. Cover only the intuition here. -->

---

## Section 2 — Sequential Models: RNNs and the Vanishing Gradient

Documents are sequences, not bags. The sentiment of "the company did not miss its targets" depends on the negation appearing before the noun phrase. An earnings-call transcript unfolds over time; the CFO's guidance on page 20 may qualify a claim on page 3. Static aggregation strategies are blind to these dependencies.

Recurrent Neural Networks (RNNs) process sequences by maintaining a hidden state $\mathbf{h}_t$ that summarises the history $\mathbf{x}_1, \ldots, \mathbf{x}_t$:

$$
\mathbf{h}_t = \sigma\!\left(W_h\,\mathbf{h}_{t-1} + W_x\,\mathbf{x}_t + \mathbf{b}\right)
$$

All parameters are shared across time steps. Training requires backpropagation through time (BPTT), which chains Jacobians across every time step. The product of $T - t$ Jacobian matrices carries the gradient from loss at step $T$ back to the weights at step $t$.

This creates the fundamental problem. Each Jacobian factor satisfies

$$
\left\|\frac{\partial \mathbf{h}_{k+1}}{\partial \mathbf{h}_k}\right\|_2 \leq M_\sigma \cdot \rho
$$

where $\rho = \|W_h\|_2$ is the spectral norm of the recurrent weight matrix, and $M_\sigma = \sup_z |\sigma'(z)|$ is the maximum derivative of the activation function. The product of $T-t$ such factors is bounded above by $(M_\sigma \rho)^{T-t}$. For the logistic sigmoid $M_\sigma = 1/4$; for tanh $M_\sigma = 1$. Whenever $M_\sigma \rho < 1$, the gradient decays exponentially with sequence length.

For an S&P 500 earnings call of roughly 10,000 tokens, a gradient signal from position 100 contributes essentially nothing to the weight update — long-range financial dependencies are unlearnable. Gradient clipping handles the exploding case (when $\rho > 1/M_\sigma$), but there is no analogous in-architecture fix for vanishing gradients in the vanilla RNN.

---

## Section 3 — LSTM: Six Gates and the Constant Error Carousel

The Long Short-Term Memory (LSTM) unit was designed precisely to overcome vanishing gradients. The central innovation is a cell state $\mathbf{c}_t$ maintained alongside the hidden state $\mathbf{h}_t$, with an additive update path protected by sigmoid gates. The six equations are:

$$
\mathbf{f}_t = \sigma\!\left(W_f\,[\mathbf{h}_{t-1},\,\mathbf{x}_t] + \mathbf{b}_f\right) \quad \text{(forget gate)}
$$

$$
\mathbf{i}_t = \sigma\!\left(W_i\,[\mathbf{h}_{t-1},\,\mathbf{x}_t] + \mathbf{b}_i\right) \quad \text{(input gate)}
$$

$$
\mathbf{g}_t = \tanh\!\left(W_g\,[\mathbf{h}_{t-1},\,\mathbf{x}_t] + \mathbf{b}_g\right) \quad \text{(candidate cell)}
$$

$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \mathbf{g}_t \quad \text{(cell state update)}
$$

$$
\mathbf{o}_t = \sigma\!\left(W_o\,[\mathbf{h}_{t-1},\,\mathbf{x}_t] + \mathbf{b}_o\right) \quad \text{(output gate)}
$$

$$
\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t) \quad \text{(hidden state)}
$$

The key to understanding why the LSTM works is the cell-state update equation. It is additive in the candidate $\mathbf{g}_t$: the cell state at time $t$ is the old cell state times a forget gate, plus a new candidate times an input gate. The cell-state gradient satisfies:

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{c}_t} = \frac{\partial \mathcal{L}}{\partial \mathbf{c}_{t+1}} \odot \mathbf{f}_{t+1} + \text{(terms via } \mathbf{h}_t\text{)}
$$

When $\mathbf{f}_{t+1} \approx \mathbf{1}$, the gradient flows back through the cell-state highway without decay — Hochreiter and Schmidhuber called this the "constant error carousel." When the forget gate saturates toward zero, exponential decay can still occur, but the gate values are learned rather than fixed, giving the LSTM the flexibility to protect gradients on tasks that genuinely require long-range memory.

In financial text, the gates have natural interpretations. The forget gate clears irrelevant boilerplate sentiment as an earnings transcript shifts from procedural opening remarks to core financial figures. The input gate filters out legal safe-harbour language that appears in every 10-K filing and carries no firm-specific information. The output gate selects which components of the cell state to expose for a given output prediction.

The Gated Recurrent Unit (GRU) simplifies this to four equations by merging the cell state and hidden state and combining the forget and input gates into a single update gate. GRUs have approximately 25% fewer parameters than LSTMs, making them preferable under data or compute constraints; LSTMs retain an advantage on tasks with very long-range dependencies.

<!-- BOOK-ONLY: The bidirectional LSTM equations and the empirical GRU vs. LSTM benchmark comparisons from Chung et al. 2014 are in the chapter but exceed the 2-hour scope. -->

---

## Section 4 — Bahdanau Attention: The Bridge to Transformers

Even with LSTMs, the encoder must compress an entire input sequence into a fixed-length vector before the decoder begins generating. For long financial documents, this bottleneck discards information.

Bahdanau et al. (2015) proposed a solution: the decoder is allowed to look back at all encoder hidden states at each decoding step. For encoder states $\mathbf{h}_1, \ldots, \mathbf{h}_T$ and decoder state $\mathbf{s}_t$, the alignment score is:

$$
e_{t,i} = \mathbf{v}^\top \tanh\!\left(W_s\,\mathbf{s}_t + W_h\,\mathbf{h}_i\right)
$$

Applying softmax yields attention weights $\alpha_{t,i} > 0$ with $\sum_i \alpha_{t,i} = 1$, and the context vector $\mathbf{c}_t = \sum_i \alpha_{t,i} \mathbf{h}_i$ is a convex combination of all encoder states. In a financial summariser, when the decoder generates a sentence about net income, the attention weights concentrate on the tokens in the source where income figures appear.

Applying attention within a single sequence — each token attending to all others — yields self-attention, the core operation of the Transformer. Dot-product attention replaces the additive alignment score with a scaled inner product, reducing cost from $O(T d_a)$ to $O(T d_k)$ per step.

---

## Section 5 — Scaled Dot-Product Attention and Why $\sqrt{d_k}$ Matters

The Transformer's core operation maps input token representations through three projection matrices and computes:

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V
$$

Entry $(i, j)$ of the pre-softmax matrix $QK^\top$ is the dot product $\mathbf{q}_i^\top \mathbf{k}_j$. Row-wise softmax converts these scores into attention weights. The output for token $i$ is a weighted combination of value vectors: $\sum_j A_{ij} \mathbf{v}_j$.

Why divide by $\sqrt{d_k}$? Suppose query and key components are i.i.d. with mean zero and unit variance. Then each of the $d_k$ terms in the dot product has unit variance, so:

$$
\text{Var}\!\left(\mathbf{q}_i^\top \mathbf{k}_j\right) = d_k
$$

For large $d_k$, the dot products concentrate near $\pm\sqrt{d_k}$. These large logit magnitudes push the softmax into its saturated regions where the derivative $\sigma(z)(1 - \sigma(z)) \approx 0$ — exactly the vanishing-gradient problem we thought we escaped. Dividing by $\sqrt{d_k}$ normalises the variance to 1, keeping the softmax in its linear region where gradients flow.

For decoder-only models that must not see future tokens, a causal mask sets all pre-softmax scores where $j > i$ to $-\infty$, ensuring zero attention weight on future positions.

Multi-head attention runs $h$ parallel attention heads, each with its own learned projection matrices:

$$
\text{MultiHead}(X) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\,W^O
$$

The original Transformer used $h = 8$ heads with $d_k = d_v = 64$. Different heads specialise in different aspects of the input: lower heads capture syntactic dependencies, deeper heads capture semantic associations. In financial models, heads specialise on temporal expressions, entity-linking across long documents, and negation scope.

---

## Section 6 — Positional Encoding and the Rotation Property

Self-attention is permutation-equivariant: rearranging the tokens rearranges the output identically. Position must be injected explicitly. The original Transformer uses sinusoidal positional encodings:

$$
\text{PE}_{(\text{pos}, 2i)} = \sin\!\left(\frac{\text{pos}}{10000^{2i/d_{\text{model}}}}\right), \quad \text{PE}_{(\text{pos}, 2i+1)} = \cos\!\left(\frac{\text{pos}}{10000^{2i/d_{\text{model}}}}\right)
$$

For small index $i$, the frequency is high and the encoding oscillates rapidly (fine-grained position). For large $i$, the frequency is low (coarse position). The result is a multi-scale positional representation analogous to a Fourier basis.

A key property: for any fixed offset $k$, the encoding at position $\text{pos} + k$ is a rotation of the encoding at position $\text{pos}$:

$$
\begin{pmatrix} \text{PE}_{(\text{pos}+k,\,2i)} \\ \text{PE}_{(\text{pos}+k,\,2i+1)} \end{pmatrix} = R(\omega_i k) \begin{pmatrix} \text{PE}_{(\text{pos},\,2i)} \\ \text{PE}_{(\text{pos},\,2i+1)} \end{pmatrix}
$$

where $R(\omega_i k)$ is a $2 \times 2$ rotation matrix that depends only on the offset $k$, not on the absolute position. This means the model can represent relative positions through linear transformations, and that $\text{PE}_{\text{pos}}^\top \text{PE}_{\text{pos}'}$ depends only on $|\text{pos} - \text{pos}'|$. This property motivated Rotary Position Embeddings (RoPE), used in Llama, Mistral, and most modern open-weight models.

The full encoder block applies self-attention and a feed-forward network, both wrapped with residual connections and layer normalisation:

$$
Z^{(\ell)} = \text{LayerNorm}\!\left(X^{(\ell)} + \text{MultiHead}(X^{(\ell)})\right)
$$

$$
X^{(\ell+1)} = \text{LayerNorm}\!\left(Z^{(\ell)} + \text{FFN}(Z^{(\ell)})\right)
$$

The residual connections ensure direct gradient pathways all the way back to the input, largely eliminating the vanishing-gradient problem that plagued deep RNNs.

---

## Section 7 — BERT vs. GPT: Pre-training Objectives and Architecture Choice

The Transformer architecture supports two major pre-training philosophies, and the choice between them determines which downstream tasks the model is suited for.

BERT (Devlin et al., 2019) is an encoder-only model trained on Masked Language Modelling (MLM). At each training step, 15% of input tokens are selected: 80% are replaced with `[MASK]`, 10% with a random token, and 10% are left unchanged. The model predicts the original tokens at masked positions:

$$
\mathcal{L}_{\text{MLM}}(\theta) = -\sum_{i \in \mathcal{M}} \log p_\theta\!\left(w_i \mid \mathbf{x}_{\setminus \mathcal{M}}\right)
$$

Because the masking objective requires predicting from both left and right context, BERT's attention is fully bidirectional. This makes BERT ideal for classification, named entity recognition, and semantic similarity. It is poorly suited to generation because it has no natural autoregressive decoding mechanism.

GPT (Radford et al., 2018) and its successors are decoder-only models trained on Causal Language Modelling (CLM), which is next-token prediction:

$$
\mathcal{L}_{\text{CLM}}(\theta) = -\sum_{t=1}^{T} \log p_\theta(w_t \mid w_1, \ldots, w_{t-1})
$$

The causal mask ensures no token attends to positions ahead of it. This makes CLM a proper autoregressive density model with natural text-generation capability. The trade-off is that each token only sees left context, making CLM representations suboptimal for tasks requiring full bidirectional understanding.

For financial NLP, the choice follows from the task:

| Task | Architecture | Rationale |
|------|-------------|-----------|
| Sentiment classification | Encoder (BERT-type) | Requires full context; classification head on `[CLS]` |
| Named entity recognition in filings | Encoder (BERT-type) | Token-level labels; benefits from bidirectional context |
| Earnings call summarisation | Encoder-decoder (T5, BART) | Sequence-to-sequence; reads full input then generates |
| Report drafting, Q&A, instruction following | Decoder (GPT-type) | Generative; natural autoregressive output |
| Numerical reasoning over tables (FinQA) | Decoder with chain-of-thought | Needs multi-step generation and intermediate computation |

---

## Section 8 — The LLM Landscape: Model Families, Financial Specialists, and Reasoning Models

Standard autoregressive models generate one token at a time from $P(x_t \mid x_1, \ldots, x_{t-1})$. For tasks requiring multi-step deliberation — DCF valuation from a noisy earnings call, multi-jurisdiction regulatory reasoning, numerical table analysis — single-pass generation is ill-suited.

Reasoning models (OpenAI o1/o3, DeepSeek-R1, Claude extended thinking) are trained via reinforcement learning with verifiable rewards to generate an explicit chain-of-thought before their final answer. The distinguishing feature is not architecture but training objective: the model is rewarded for correct final answers, with the intermediate trace serving as a scratch-pad of potentially thousands of tokens. This dramatically improves performance on quantitative finance tasks involving numerical reasoning, but does not eliminate hallucination on factual retrieval tasks.

The major model families relevant to financial NLP:

| Model | Organisation | Architecture | Parameters | Finance-specific? |
|-------|-------------|-------------|-----------|-------------------|
| GPT-4o | OpenAI | Decoder-only | ~1T (est.) | No |
| Claude 3.x/4.x | Anthropic | Decoder-only | Undisclosed | No |
| Llama 3 (405B) | Meta | Decoder-only | 405B | No |
| Gemini 1.5 Pro | Google DeepMind | Decoder-only | Undisclosed | No |
| FinBERT | Araci (2019) | Encoder (BERT) | 110M | Yes |
| BloombergGPT | Bloomberg | Decoder-only | 50B | Yes |

FinBERT takes BERT-base and further pre-trains it on Reuters/Bloomberg news and earnings transcripts; on the FinancialPhraseBank all-agree split it achieves over 97% accuracy, roughly 8 percentage points above general BERT-base. BloombergGPT trained a 50B decoder-only model on 363B financial tokens plus 345B general tokens. Importantly, subsequent benchmarks showed that large general-purpose models often match or exceed BloombergGPT due to emergent financial knowledge at scale — scale compensates for domain specificity above a certain threshold.

---

## Section 9 — Financial Benchmarks: Measuring Progress

Five benchmarks are used throughout this course.

**FinancialPhraseBank** (Malo et al., 2014): 4,840 sentences from English-language financial news, labelled positive, negative, or neutral by 16 domain experts. The standard evaluation uses the 2,264-sentence "Agree-all" subset.

**FiQA** (Maia et al., 2018): Two subtasks — aspect-based sentiment analysis (SA-C) and question answering over financial documents (QA). The QA subtask requires retrieval before generation.

**ECTSum** (Mukherjee et al., 2022): 2,425 earnings-call transcript / expert-summary pairs, evaluated by ROUGE-L. The primary summarisation benchmark.

**FinQA** (Chen et al., 2021): 8,281 question-answer pairs requiring multi-step numerical reasoning over tables and prose from SEC filings. Clearly favours reasoning models.

**FLUE** (Shah et al., 2022): A multi-task NLU evaluation covering five financial tasks. The most comprehensive single-number evaluation.

All five benchmarks are constructed from English-language, North American documents. Models evaluated on these should not be assumed to generalise to other financial contexts without further validation.

---

## Section 10 — Sampling Strategies: Temperature, Nucleus, and Beam Search

At each generation step, the model produces logits $\mathbf{z} \in \mathbb{R}^{|\mathcal{V}|}$. Temperature scaling reshapes the distribution before sampling:

$$
p_i(\tau) = \frac{\exp(z_i / \tau)}{\sum_j \exp(z_j / \tau)}
$$

As $\tau \to 0^+$, the distribution concentrates on the highest-logit token (greedy decoding). At $\tau = 1$, the distribution equals the standard softmax. As $\tau \to \infty$, the distribution approaches uniform. The Shannon entropy is strictly increasing in $\tau$: raising temperature always increases output diversity.

Nucleus (top-$p$) sampling selects the smallest set of tokens whose cumulative probability reaches threshold $p$, then renormalises and samples. At each step, the sampling pool adapts to the model's confidence: a sharp distribution admits few tokens; a flat distribution admits many.

Beam search maintains the $B$ most probable partial sequences at each step and expands them in parallel. It was dominant for machine translation in the late 2010s and remains appropriate when output quality is measured by a deterministic metric (ROUGE, BLEU). For open-ended generation it tends to produce repetitive, generic text.

For financial applications, the appropriate strategy depends on what the output is for:

| Task | Temperature | Sampling | Rationale |
|------|------------|---------|-----------|
| Structured data extraction | $\tau = 0$ | greedy | Determinism essential; deviation is an error |
| Sentiment labelling | $\tau \approx 0.1$ | greedy or top-$k$ | Low variance needed |
| Document summarisation | $\tau \approx 0.3$–$0.5$ | top-$p = 0.9$ | Some lexical diversity; accuracy still critical |
| Regulatory Q&A | $\tau \approx 0.1$ | greedy with RAG | Low temperature plus retrieval |
| Scenario / stress-test narrative | $\tau \approx 0.7$–$1.0$ | top-$p = 0.95$ | Creative diversity is the objective |

---

## Section 11 — Structured Generation: Validity Masks, JSON Mode, and Pydantic

Financial NLP pipelines need schema-conformant output. Free-text generation fails in three systematic ways: numerical hallucination (plausible-looking but wrong figures), silent field omission (missing fields with no signal), and unit confusion (mixing monetary scales). The solution is constrained decoding via validity masks.

A validity mask $M_t \in \{0,1\}^{|\mathcal{V}|}$ is computed at each step from the grammar and the tokens generated so far:

$$
M_t[i] = \mathbf{1}\!\left[\text{token } i \text{ can extend } x_{<t} \text{ to a string in } \mathcal{L}(\mathcal{G})\right]
$$

Invalid tokens receive $-\infty$ log-probability before the softmax. This is not a post-hoc filter: the model always produces a valid continuation, renormalising only over valid tokens.

Modern APIs expose this through tool use and JSON mode. The Anthropic API accepts a Pydantic model's JSON Schema as a tool definition and guarantees a valid structured response:

```python
from pydantic import BaseModel
from typing import Optional
import anthropic

class EarningsReport(BaseModel):
    revenue_bn: Optional[float] = None
    net_income_bn: Optional[float] = None
    eps: Optional[float] = None
    guidance_bn: Optional[float] = None

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    tools=[{
        "name": "record_earnings",
        "description": "Record structured earnings figures from text.",
        "input_schema": EarningsReport.model_json_schema(),
    }],
    tool_choice={"type": "tool", "name": "record_earnings"},
    messages=[{"role": "user",
               "content": "Extract earnings: Revenue $4.2B, net income $820M, EPS $1.34."}],
)
result = EarningsReport(**message.content[0].input)
```

Setting `tool_choice` to a specific tool forces the model to always return the structured object. Three failure modes remain even with constrained decoding: wrong-but-valid numbers (pair with $\tau = 0$ and RAG), optional fields produce explicit `null` values rather than silent omission, and unit validation requires application-level logic outside the schema.

---

## Section 12 — API Usage: BPE Tokenisation, Cost Models, and Prompt Caching

Every production LLM workflow goes through an API with real cost and latency consequences.

Byte-Pair Encoding builds a sub-word vocabulary iteratively: initialise with individual characters, then repeatedly merge the most frequent adjacent pair until reaching the target vocabulary size. Common morphemes become single tokens ("earn", "ings"); rare terms are split more finely. As a practical rule, one English word corresponds to approximately 1.3 tokens.

API providers charge separately for input and output tokens:

$$
\text{cost} = N_{\text{in}} \cdot c_{\text{in}} + N_{\text{out}} \cdot c_{\text{out}}
$$

Approximate 2024 prices (USD per million tokens):

| Model | Input (\$/MTok) | Output (\$/MTok) |
|-------|----------------|-----------------|
| GPT-4o | \$5.00 | \$15.00 |
| Claude 3 Haiku | \$0.25 | \$1.25 |
| Llama 3 (self-hosted A100) | ~\$0 | ~\$0 (GPU cost only) |

For a workload of 10,000 transcripts, each 5,000 words ($\approx$6,500 tokens) with a 500-token system prompt and 400 output tokens per transcript:

$$
\text{cost}_{\text{GPT-4o}} = 10{,}000 \times \left(\frac{7{,}000}{10^6} \times 5.00 + \frac{400}{10^6} \times 15.00\right) = \$410
$$

The same workload on Claude 3 Haiku costs approximately \$20 — a twenty-fold reduction. The production strategy: use cheap, fast models for high-volume filtering; reserve expensive reasoning models for complex analytical steps.

Prompt caching (Anthropic and OpenAI) caches a shared prefix of the system prompt across requests, reducing the effective input-token price by roughly 90% on cache hits. For pipelines processing many documents under the same analytical framework, caching the shared system prompt is among the highest-ROI engineering optimisations available.

---

## Section 13 — RAG Pipelines: Dense, Sparse, Hybrid, and the FinanceBench Lesson

Retrieval-Augmented Generation (RAG) transfers factual accuracy from model parameters to a retrieval index. A RAG system operates in three stages: retrieval (score passages against the query and return top-$k$), augmentation (prepend retrieved passages to the query), and generation (produce the answer conditioned on the augmented prompt).

Dense retrieval uses cosine similarity between neural embeddings:

$$
s_{\text{dense}}(q, d_i) = \frac{\phi(q) \cdot \phi(d_i)}{\|\phi(q)\| \|\phi(d_i)\|}
$$

A bi-encoder model (SBERT or a fine-tuned variant) encodes both query and passage. At query time, FAISS or HNSW approximate nearest-neighbour search makes retrieval efficient over millions of passages.

Dense retrieval excels at semantic similarity but fails on exact-match queries common in finance: a specific CUSIP number, a filing section reference, or an exact ticker symbol. BM25 sparse lexical retrieval handles these via term-frequency matching. Hybrid retrieval combines both via reciprocal rank fusion:

$$
\text{RRF}(d) = \sum_{r \in \{\text{dense},\,\text{sparse}\}} \frac{1}{60 + \text{rank}_r(d)}
$$

For high-precision applications, a cross-encoder re-ranker scores the top-100 retrieved passages and returns the top-5.

The FinanceBench benchmark provides a sobering calibration: GPT-4-Turbo with a retrieval system incorrectly answers or refuses 81% of questions from SEC filings. Naive RAG pipelines are insufficient for high-stakes financial document QA. Careful chunking (paragraph-level, 512 tokens, 50-token overlap), hybrid retrieval, re-ranking, and answer verification are all necessary.

<!-- BOOK-ONLY: Knowledge distillation (KD loss equation), LoRA parameter reduction analysis, GPTQ and AWQ quantisation, and the lottery ticket hypothesis are in the chapter's deep-dive sections and exceed the 2-hour lecture scope. -->

---

## Section 14 — Hallucinations and Responsible Use

A language model hallucination is an output presented with apparent confidence that is not supported by the model's input or the external world. Three sub-types are particularly consequential for finance.

Numerical hallucination occurs when the model outputs a figure that differs from the source document — a debt-to-equity ratio of 1.8 summarised as 0.8 inverts the risk profile. Entity hallucination substitutes one company, person, or regulatory body for another. Citation hallucination fabricates a regulatory reference or court ruling that does not exist.

The root cause is intrinsic: models are trained to produce plausible text, and plausibility correlates with but is not identical to factual accuracy. Reducing temperature to zero eliminates stochasticity but does not eliminate hallucination; the most probable completion may still be factually wrong.

Detection methods: SelfCheckGPT draws $N$ independent samples and checks whether a claim is consistently reproduced (hallucinated claims are inconsistent across samples); FActScore decomposes the output into atomic claims and verifies each against a retrieval-backed knowledge source; inner confidence scoring (Chen et al., 2024) shows that high-confidence predictions are systematically more accurate.

Five mitigation techniques, applied together:

1. RAG: ground the context in verified retrieved passages; the model almost never fabricates figures absent from the retrieved text.
2. Self-consistency sampling: draw $K$ independent chains; take the majority-vote answer. Effective for numerical reasoning.
3. Chain-of-thought prompting: require explicit intermediate steps; each step is independently verifiable.
4. Claim decomposition and verification: break outputs into atomic claims; flag unsupported claims before human review.
5. Confidence elicitation and abstention: prompt the model to flag uncertainty; calibrate thresholds against accuracy curves.

On responsible use: the EU AI Act (Regulation 2024/1689, in force August 2024) classifies credit scoring, insurance pricing, and AI-assisted securities pricing as high-risk systems requiring conformity assessments and human oversight. Look-ahead bias from LLM memory is a genuine empirical risk: Didisheim et al. (2025) demonstrate that LLMs can reconstruct historical aggregate financial time series from parametric memory, producing spurious predictability in back-tests that do not account for this leakage. GDPR imposes obligations on fine-tuning or RAG over client data, including a right to erasure that a model trained on personal data cannot easily satisfy. Geographic bias is systematic: all five major financial benchmarks are built from North American English-language sources.

---

## Summary

This lecture traced the complete arc from document-level aggregation (mean embedding, TF-IDF, SBERT) through sequential models (RNN vanishing gradient, LSTM six gates, GRU, Bahdanau attention) to the Transformer architecture (scaled dot-product attention, the $\sqrt{d_k}$ proof, multi-head attention, sinusoidal positional encoding and the rotation property, the full encoder block). We contrasted BERT's MLM and GPT's CLM pre-training objectives and matched each architecture type to appropriate downstream tasks. We surveyed the modern LLM landscape including FinBERT, BloombergGPT, and reasoning models, and mapped five financial benchmarks to their task structures. We covered API mechanics (BPE, cost model, prompt caching), sampling strategy selection for five financial task types, structured generation via validity masks and Pydantic, a complete RAG pipeline design with the FinanceBench lesson, and a taxonomy of hallucinations with five mitigation techniques and the regulatory landscape (EU AI Act, look-ahead bias, GDPR, geographic bias).

The next lecture applies these foundations to sentiment analysis — the first and most-studied financial NLP task — using FinancialPhraseBank as the primary benchmark.
