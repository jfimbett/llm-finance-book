# Lecture 3: Training and Fine-Tuning Large Language Models

---
Course: Large Language Models in Finance
Institution: Paris Dauphine -- PSL University
Instructor: Juan F. Imbet
Duration: 2 hours (plus 1-hour practical session)
Prerequisites: Lectures 1 (NLP foundations) and 2 (Transformer architecture)
---

## Learning Objectives

By the end of this lecture, students should be able to:

1. Describe the composition of major pre-training corpora and quantify the underrepresentation of financial text, articulating the consequences for domain performance.
2. Apply BPE tokenisation mechanics and compute the fertility of a tokeniser on a given financial corpus sample.
3. Reconstruct the Chinchilla scaling law and derive the compute-optimal allocation between model size and training tokens given a FLOP budget.
4. Contrast CLM, MLM, and span-corruption objectives and select the appropriate one for a downstream finance task.
5. Apply LoRA parameter counting to a concrete model (e.g., 7B LLaMA) and explain why LoRA is preferred over full fine-tuning for resource-constrained settings.
6. Trace the three-stage RLHF pipeline and identify where DPO simplifies it.
7. Compare FinBERT and BloombergGPT on standard financial NLP benchmarks, explain the domain-adaptation mechanisms behind their performance gains, and identify key limitations of each.
8. Describe what MiFID II Article 37, SR 11-7, and the EU AI Act require of LLM-assisted financial workflows, and apply the three-tier risk classification to a concrete deployment scenario.

---

## 1. Why Data Composition Determines LLM Capability

A large language model learns from the statistical patterns present in its pre-training corpus. This seemingly obvious observation has a deep practical consequence: the model cannot generate or reason about information whose distribution is absent or severely underrepresented in training data. For financial applications this matters enormously, because financial text constitutes a tiny fraction of the open web.

The intuition is straightforward. If a model has seen ten million examples of casual English prose and only fifty thousand examples of credit-default swap documentation, it will be far more fluent in prose than in financial contracts. Beyond raw frequency, the model also internalises the vocabulary, syntax, and implicit conventions of whatever domains dominate its training mix. Token fertility — defined formally below — is one quantitative indicator of this domain gap: a tokeniser trained on general web text will split financial terminology into more subword pieces than a tokeniser trained on financial text, increasing the effective sequence length and degrading downstream task performance.

The composition question is therefore the first design decision in any LLM project. Before choosing an architecture, before picking a fine-tuning recipe, practitioners must ask: what text did this model see, in what proportions, and how does that distribution compare to the text it will encounter at inference time?

---

## 2. Sources and Financial Data Underrepresentation

### Major Pre-training Corpora

Common Crawl is the dominant ingredient in most large open-source LLMs. It is a web archive updated monthly that covers approximately 200–400 TB per snapshot, with the total multi-year archive exceeding several petabytes. Despite its scale, raw Common Crawl is approximately 90% noise by most quality measures: boilerplate, duplicate content, machine-translated spam, and low-information pages vastly outnumber high-quality prose. Consequently, almost every serious LLM pipeline applies aggressive filtering before using Common Crawl data.

The Pile, assembled by EleutherAI, was an early attempt to construct a curated multi-source corpus. It combines 22 component datasets including books (Books3), code (GitHub), academic papers (PubMed, ArXiv), legal text (FreeLaw), and web text (OpenWebText2, Pile-CC). Its explicit component-level composition makes it a useful baseline for analysing domain mix effects. RefinedWeb, released by Mistral/Technology Innovation Institute, demonstrated that aggressive deduplication and quality filtering of Common Crawl alone can produce a corpus competitive with The Pile's hand-curated blend — an important lesson about the relative value of scale versus curation.

### Financial Text Underrepresentation

Across a typical filtered web crawl, financial text accounts for roughly 0.5% of tokens by volume. This figure aggregates all sources: news about corporate earnings, personal finance advice, macroeconomic commentary, academic finance papers, and regulatory disclosures together amount to half a percentage point of what a model sees during pre-training.

Practitioners rely on four main financial-text sources to address this deficit. EDGAR (the SEC's Electronic Data Gathering, Analysis, and Retrieval system) provides machine-readable full texts of 10-K annual reports, 10-Q quarterly filings, 8-K material event disclosures, proxy statements, and registration documents. A full EDGAR scrape for the period 1996–present covers tens of millions of documents and constitutes the most comprehensive source of regulatory-grade financial English available in the public domain. Earnings-call transcripts — either purchased from data vendors or scraped from financial portals — provide spoken-register financial language, which differs markedly from the written register of regulatory filings. Bloomberg news archives, where licensed, supply high-density financial news with entity linking and temporal coverage. Alternative data sources, including satellite imagery metadata, credit-card transaction summaries, job-posting feeds, and shipping manifests, increasingly appear in specialised financial NLP models, though their unstructured textual components are sparse.

---

## 3. Tokenisation: BPE and Fertility

### Byte-Pair Encoding

Byte-pair encoding (BPE) constructs a subword vocabulary by iteratively merging the most frequent adjacent pair of symbols in a training corpus. Starting from a character-level vocabulary, each merge step replaces the most frequent bigram with a new single token. After a fixed number of merges, the resulting vocabulary of 30,000–100,000 subword units can represent any input text via a sequence of known tokens.

BPE balances two competing pressures. A purely character-level vocabulary (size 256 for bytes) produces very long sequences that make attention mechanisms expensive. A purely word-level vocabulary cannot handle out-of-vocabulary terms and grows unmanageably large across multilingual corpora. BPE occupies a productive middle ground: common words appear as single tokens, rare or domain-specific words are segmented into recognisable subword components.

For financial text, BPE vocabularies derived from general web corpora perform poorly on specialised terminology. Tickers like "MSFT" or "AAPL" may or may not appear as single tokens depending on whether they were frequent enough in training. Regulatory phrases like "material adverse change" or "safe harbour statement" may be fragmented unpredictably.

### The Fertility Formula

The fertility of a tokeniser $\tau$ on a corpus $C$ measures how many tokens the tokeniser produces per word:

$$F(\tau, C) = \frac{\text{number of tokens produced by } \tau \text{ on } C}{\text{number of whitespace-separated words in } C}$$

A fertility close to 1.0 indicates the tokeniser handles the corpus vocabulary efficiently (most words map to single tokens). A fertility above 1.5 indicates fragmentation: the tokeniser is splitting many words into multiple pieces, lengthening sequences and increasing computational cost. In practice, a BPE tokeniser trained on general web text achieves fertility around 1.10–1.20 on standard English prose but 1.40–1.60 on dense financial text containing tickers, CUSIP numbers, basis-point notation, and regulatory acronyms. This fertility gap is one motivation for training domain-specific tokenisers alongside domain-specific weights.

---

## 4. Data Quality: Deduplication and Filtering

Raw web text requires a multi-stage quality pipeline before it can serve as pre-training data. The stages are applied in sequence: language identification, heuristic filtering, perplexity filtering, deduplication, and PII scrubbing.

Language identification assigns each document a language label, most commonly using fastText classifiers. For a finance-focused corpus, retaining only English-language documents is a reasonable first pass, though ignoring non-English financial text — particularly Mandarin, Japanese, and German — introduces a geographic bias discussed in Section 12.

Heuristic filters remove documents based on measurable surface properties: fraction of lines ending in punctuation, ratio of alphanumeric characters to total characters, presence of repeated n-grams indicating template spam, minimum token count, and symbol-to-word ratio. These rules, while crude, eliminate a large fraction of low-quality web pages without requiring expensive model inference.

Perplexity filtering uses a small reference language model — typically a 5-gram KenLM or a small neural LM — to assign each document a perplexity score. Documents with very high perplexity relative to the reference distribution are discarded as likely noise. The threshold is set empirically to retain a target fraction of documents; too aggressive a filter removes legitimate but unusual text.

Deduplication is arguably the highest-impact quality intervention. Neural LLMs trained on duplicated content memorise repeated passages and generalise poorly. The standard approach is MinHash deduplication. For a document $d$, MinHash estimates the Jaccard similarity between any two documents using a small set of hash functions. The Jaccard similarity between documents $A$ and $B$ is defined as:

$$J(A, B) = \frac{|S(A) \cap S(B)|}{|S(A) \cup S(B)|}$$

where $S(d)$ is the set of $k$-gram shingles extracted from document $d$. Documents with Jaccard similarity above a threshold (typically 0.8) are considered near-duplicates, and all but one copy is removed. Exact-match deduplication (SHA-256 hash comparison) is also applied to remove identical documents. For financial corpora, deduplication is critical because press releases, regulatory filings, and earnings-call boilerplate are frequently reproduced verbatim across hundreds of downstream sources.

PII scrubbing identifies and removes personally identifiable information: email addresses, telephone numbers, physical addresses, social security numbers, and similar sensitive fields. Beyond privacy compliance, PII scrubbing prevents models from memorising and reproducing personal data at inference time — a regulatory concern under GDPR and related regimes.

---

## 5. Data Mixing and Curriculum Strategies

### Proportional versus Up-Sampling

Given a collection of source datasets $\{D_1, D_2, \ldots, D_K\}$ with sizes $\{n_1, n_2, \ldots, n_K\}$, the simplest mixing strategy samples each source in proportion to its size. Under proportional sampling, source $i$ contributes a fraction $n_i / \sum_j n_j$ of training tokens. For a finance LLM, this would give financial text its natural 0.5% share — clearly insufficient.

Up-sampling corrects domain imbalance by oversampling smaller sources. A common parameterisation uses a smoothing exponent $\alpha \in (0,1]$: the effective sampling weight for source $i$ is proportional to $n_i^\alpha$. The corresponding token budget for source $i$ is:

$$T_i = T \cdot \frac{n_i^\alpha}{\sum_j n_j^\alpha}$$

where $T$ is the total token budget. At $\alpha = 1$ this recovers proportional sampling. At $\alpha < 1$, smaller sources receive a larger share relative to their natural size. Typical values range from $\alpha = 0.7$ (mild up-sampling of rare domains) to $\alpha = 0.3$ (aggressive equalisation). The trade-off is that heavy up-sampling of small financial corpora increases the risk of overfitting to the repeated examples in those sources.

<!-- BOOK-ONLY: A rigorous derivation of the optimal α under a finite-data regime, including the bias-variance decomposition and empirical calibration against downstream task performance, is given in the companion chapter. -->

### Curriculum Learning and Replay Buffers

Curriculum learning draws on the educational intuition that learning is more efficient when examples are presented in a progression from simple to complex. In LLM pre-training, this most commonly manifests as staging data quality: training begins on a large but lower-quality corpus, then transitions to a smaller high-quality corpus in later stages. The early exposure to scale provides broad vocabulary and distributional coverage; the late exposure to quality sharpens generation and factual accuracy.

Replay buffers address catastrophic forgetting during continued pre-training or domain adaptation. When a model trained on general text is further trained on a domain-specific corpus, it risks overwriting general capabilities. A replay buffer retains a fraction of the original training distribution and periodically mixes it into the fine-tuning stream, maintaining performance on general benchmarks while the model adapts to the new domain. Typical replay fractions range from 5% to 20% of the domain-adaptation batch.

---

## 6. Pre-training Objectives: CLM, MLM, and Span Corruption

### Causal Language Modelling

The causal language model (CLM) objective, used by GPT-family models, trains the model to predict each token given all preceding tokens. For a sequence $(x_1, x_2, \ldots, x_T)$, the training loss is the negative log-likelihood:

$$\mathcal{L}_{\text{CLM}} = -\sum_{t=1}^{T} \log P(x_t \mid x_1, \ldots, x_{t-1}; \theta)$$

The left-to-right autoregressive structure makes CLM models natural generators: sampling from the model one token at a time yields coherent continuations of any prompt. The structural constraint is that each token attends only to its left context, implemented via causal (lower-triangular) masking of the self-attention matrix. CLM is the dominant objective for modern large language models.

### Masked Language Modelling

The masked language model (MLM) objective, introduced by BERT, randomly masks 15% of input tokens and trains the model to predict the original values from bidirectional context. Because each position can attend to all other positions, MLM encoders build richer contextual representations for classification and extraction tasks. The trade-off is that MLM models are not generative: sampling requires a separate decoding strategy. For finance-specific classification tasks — sentiment analysis, named entity recognition, financial event detection — MLM encoder models trained or fine-tuned on domain text remain competitive with much larger generative models.

### Span Corruption

T5 (Text-to-Text Transfer Transformer) introduced span corruption as a generalisation of MLM. Rather than masking individual tokens independently, the model replaces contiguous spans of tokens with single sentinel tokens (e.g., `<extra_id_0>`) and trains a sequence-to-sequence model to reconstruct all masked spans in order. Span corruption encourages the model to learn richer contextual dependencies than token-level masking, and the encoder-decoder architecture naturally supports both understanding and generation tasks within a unified framework.

---

## 7. The Chinchilla Scaling Laws

### Setup

Scaling laws describe how model performance changes as a function of model size $N$ (number of trainable parameters), training data size $D$ (number of tokens), and compute $C$ (number of floating-point operations). Hoffmann et al. (2022) — the "Chinchilla" paper — established the following empirical relationship for the cross-entropy validation loss of an autoregressive language model:

$$L(N, D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$$

where $E$ is an irreducible entropy floor (the best any model could achieve), $A$ and $B$ are fitted constants, and $\alpha, \beta > 0$ govern the rates at which additional parameters and data reduce loss. Training a transformer model requires approximately $C \approx 6ND$ floating-point operations (the factor 6 accounts for the forward pass, backward pass, and parameter updates in standard mixed-precision training).

<!-- BOOK-ONLY: Full derivation of N*(C) and D*(C) by Lagrange multipliers, sensitivity analysis of the α and β exponents, and the connection to the bias-variance decomposition are developed in the companion chapter. The derivation below is presented in outline form for lecture purposes. -->

### The Compute-Optimal Result

Given a fixed compute budget $C = 6ND$, the goal is to find the model size $N^*(C)$ and dataset size $D^*(C)$ that minimise $L(N, D)$ subject to the constraint. Setting up the Lagrangian and solving the first-order conditions (details in the book), one obtains:

$$N^*(C) \propto C^{\beta/(\alpha + \beta)}, \qquad D^*(C) \propto C^{\alpha/(\alpha + \beta)}$$

With the empirical Chinchilla estimates $\alpha \approx 0.34$ and $\beta \approx 0.28$, both exponents are close to 0.5, meaning model size and data size should scale roughly in proportion with compute. The key practical result is:

$$\frac{D^*}{N^*} \approx 20$$

that is, each parameter should be trained on approximately 20 tokens. At a compute budget of $C \approx 10^{23}$ FLOPs (roughly the budget for GPT-3), the Chinchilla result implies a compute-optimal model of approximately 70B parameters trained on approximately 1.4T tokens. GPT-3, by contrast, trained a 175B-parameter model on only 300B tokens — over-parameterised and under-trained by a factor of roughly 4 by this criterion.

For a 7B-parameter model, the compute-optimal training run requires approximately $7\text{B} \times 20 = 140\text{B}$ tokens. LLaMA-2 (7B) trained on 2T tokens deliberately exceeded the Chinchilla budget to produce a smaller model with strong inference-time performance — a pragmatic choice reflecting the reality that inference costs often dominate total-cost-of-ownership in production deployments.

*Practical 3b applies the Chinchilla rule: given $C = 10^{22}$ FLOPs, students derive $N^*$ and $D^*$ and determine whether a 50B-token financial corpus is a binding constraint.*

---

## 8. Distributed Training at Scale

Training modern LLMs requires distributing computation across hundreds to thousands of accelerators. Three complementary parallelism strategies address different bottlenecks.

Data parallelism replicates the full model on each device, partitions the training batch across devices, and aggregates gradients using ring-AllReduce — a communication pattern in which each device sends and receives gradient shards in a ring topology, achieving bandwidth-optimal all-reduce in $O(K)$ communication steps for $K$ devices. Data parallelism is the easiest form of parallelism to implement but is limited by the requirement that the full model fit in a single device's memory.

Model parallelism (also called tensor parallelism) partitions the weight matrices of each layer across devices. A common column-wise partition splits the weight matrix $W \in \mathbb{R}^{d \times k}$ into column blocks $[W_1 \mid W_2 \mid \cdots]$, each stored on a separate device. Each device computes $xW_i$ independently; the results are concatenated (or all-reduced, depending on the layer) before the next operation. This approach allows models larger than a single device's memory to be trained but introduces intra-layer communication overhead.

Pipeline parallelism partitions the model depth-wise, assigning groups of consecutive layers to successive devices. The fraction of time spent in "bubble" (devices idle while waiting for upstream stages to produce activations) is approximately $(p - 1)/(m + p - 1)$, where $p$ is the number of pipeline stages and $m$ is the number of micro-batches per step. Large $m$ reduces bubble fraction but increases memory for stored activations.

ZeRO (Zero Redundancy Optimizer), developed by Microsoft, addresses the memory redundancy inherent in data-parallel training. In standard data parallelism, each device stores the full model weights, gradients, and optimiser states. ZeRO Stage 1 partitions optimiser states across devices; Stage 2 additionally partitions gradients; Stage 3 partitions the model weights themselves. Stage 3 achieves nearly linear memory reduction with device count, at the cost of additional communication.

<!-- BOOK-ONLY: Full memory accounting for ZeRO stages 1/2/3 with mixed-precision training (bfloat16 weights, fp32 master weights, Adam optimiser moments), FlashAttention tiled SRAM computation and IO complexity analysis, and gradient checkpointing O(√L) memory reduction derivation are given in the companion chapter. -->

Mixed-precision training (bfloat16 weights with float32 master copies) and gradient checkpointing further reduce memory requirements and are universally applied in practice. FlashAttention tiles the $QK^\top$ computation into SRAM-resident blocks, avoiding materialising the full $T \times T$ attention matrix in HBM and enabling sequence lengths of 32K–100K tokens that would otherwise be memory-prohibitive.

<!-- BOOK-ONLY: Full memory accounting for bfloat16 mixed-precision (fp32 master weights, Adam optimiser moments), gradient checkpointing O(√L) memory derivation, and FlashAttention IO complexity analysis (HBM reads scale as O(N²d/M) vs O(N²d) naive) are treated in the companion chapter. -->

---

## 9. The Adaptation Spectrum: Zero-Shot to Full Fine-Tuning

After pre-training, a model can be applied to downstream tasks along a spectrum of adaptation intensity, each point on the spectrum representing a different trade-off between resource cost, data requirements, and task performance.

Zero-shot inference requires no task-specific training data: the user describes the task in natural language (a "prompt") and the model responds. Performance depends entirely on what the model learned during pre-training and any prior instruction tuning. Zero-shot is appropriate when labelled data is unavailable and the task is well within the model's pre-training distribution.

Few-shot or in-context learning inserts a small number of labelled examples directly into the prompt. The model conditions on these examples to infer the pattern and generalise to a held-out query. In-context learning requires no gradient updates and is reversible — the model's weights are unchanged. Its limitations are the context window size (bounding how many examples can fit) and sensitivity to example order and phrasing.

Parameter-efficient fine-tuning (PEFT) introduces a small number of trainable parameters while keeping the pre-trained weights frozen. LoRA and adapters (detailed in Section 10) are the dominant PEFT methods. PEFT reaches within a few percentage points of full fine-tuning on most tasks while requiring only 0.1–1% of the trainable parameters.

Full fine-tuning updates all model weights on a task-specific dataset. It achieves the strongest in-distribution performance but requires substantial data (typically tens of thousands of labelled examples), compute (proportional to model size), and careful regularisation to prevent catastrophic forgetting of general capabilities. The "adaptation tax" refers to the empirical observation that full fine-tuning on a narrow domain can degrade performance on adjacent tasks — a relevant concern when deploying finance LLMs that must also handle general client communication.

---

## 10. Parameter-Efficient Fine-Tuning: LoRA, Prefix Tuning, and Adapters

### LoRA

Low-Rank Adaptation (LoRA), introduced by Hu et al. (2021), hypothesises that the change in weights during fine-tuning has low intrinsic rank. For a pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA parameterises the update as:

$$W = W_0 + BA$$

where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with $r \ll \min(d, k)$. The matrices $B$ and $A$ are initialised so that $BA = 0$ at the start of training (typically by initialising $A$ with a random Gaussian and $B$ with zeros). Only $B$ and $A$ are updated during fine-tuning; $W_0$ is frozen. The number of trainable parameters introduced per adapted layer is $r(d + k)$.

A worked example grounds the arithmetic. LLaMA-7B has 32 transformer layers. Each layer contains four projection matrices (Q, K, V, O) of size $d = k = 4096$. Applying LoRA with rank $r = 8$ to all four projections in all 32 layers gives:

$$32 \times 4 \times 8 \times (4096 + 4096) = 32 \times 4 \times 8 \times 8192 = 8{,}388{,}608 \approx 8.4\text{M parameters}$$

This is $8.4\text{M} / 7000\text{M} \approx 0.12\%$ of the total model. Training this on an A100 (40 GB VRAM) takes approximately 90 minutes on a standard instruction-following dataset, versus roughly 40 hours for full fine-tuning of the same model on the same hardware. At inference time, LoRA introduces no additional overhead because $W_0 + BA$ can be merged into a single weight matrix before deployment.

### QLoRA

QLoRA combines LoRA with 4-bit quantisation of the frozen base model weights. The base model is quantised to NF4 (normal float 4-bit, optimised for normally distributed weights) and stored on-device in compressed form; LoRA adapters are trained in bfloat16. This combination fits a 65B-parameter model into a single 48 GB GPU for fine-tuning — a hardware requirement that would otherwise demand eight or more A100s.

### Prefix Tuning

Prefix tuning prepends a set of learnable "prefix" vectors to the key and value matrices of every attention layer. If the original key matrix for a sequence of length $n$ is $K \in \mathbb{R}^{n \times d_k}$, prefix tuning extends it to $K' = [P_K; K] \in \mathbb{R}^{(l+n) \times d_k}$ where $P_K \in \mathbb{R}^{l \times d_k}$ are the $l$ trainable prefix vectors and similarly for values. The model attends over both the prefix and the actual sequence. Only the prefix matrices are trained. Prefix tuning is particularly effective for generation tasks, where the soft prefix can steer the model's output distribution without modifying any weights.

### Adapters

Adapter modules insert small bottleneck networks after each sub-layer of the transformer. A typical adapter applies a down-projection $W_{\text{down}} \in \mathbb{R}^{d \times m}$ (with $m \ll d$), a non-linearity, and an up-projection $W_{\text{up}} \in \mathbb{R}^{m \times d}$, with a residual connection bypassing the bottleneck. Only the adapter parameters are trained. The primary disadvantage of adapters relative to LoRA is that they add sequential computation at inference time, increasing latency unless the adapter weights are fused into the base model (which requires additional engineering effort).

### Practical Preference for LoRA

LoRA is preferred in most production settings because: (1) it introduces zero inference overhead when the $BA$ product is merged; (2) multiple LoRA adapters for different tasks can be swapped in and out without changing the base model; (3) QLoRA extends it to settings where the base model is too large for standard fine-tuning; (4) it is well-supported by libraries such as HuggingFace PEFT, making implementation straightforward.

*Practical 3a asks you to reproduce the 7B LoRA parameter count for different values of $r$ and different module selections, and to fine-tune FinBERT with LoRA for financial sentiment.*

---

## 11. Instruction Tuning, RLHF, and DPO

### Instruction Tuning

A model trained only with a CLM objective on web text generates plausible continuations of any prefix but does not necessarily respond helpfully to instructions. Instruction tuning (also called supervised fine-tuning on demonstrations) addresses this by training on a dataset of (instruction, response) pairs. FLAN (Finetuned Language Models, Wei et al. 2021) demonstrated that covering a large number of task formats — classification, translation, summarisation, question answering, and more — dramatically improves zero-shot performance on held-out tasks. The key insight is format diversity: a model that has seen many ways of being instructed generalises better to novel phrasings of familiar tasks.

### RLHF

Reinforcement Learning from Human Feedback (RLHF) aligns model outputs with human preferences through three stages. First, supervised fine-tuning (SFT) trains the base model on high-quality human-written demonstrations to produce an initial policy. Second, a reward model is trained on pairwise human preference data: given two model responses to the same prompt, a human annotator indicates which is preferred. The reward model is trained with the Bradley-Terry loss, which models the probability that response $y_w$ is preferred over $y_l$ as:

$$P(y_w \succ y_l) = \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))$$

where $r_\theta(x, y)$ is the scalar reward assigned to response $y$ given prompt $x$. Third, the SFT policy is further trained by PPO (Proximal Policy Optimisation) to maximise the reward model score subject to a KL-divergence penalty that prevents the policy from deviating too far from the SFT baseline:

$$\mathcal{L}_{\text{RL}}(\theta) = \mathbb{E}_{(x,y) \sim \pi_\theta}\bigl[r_\phi(x, y) - \beta \cdot \mathrm{KL}(\pi_\theta(\cdot|x) \| \pi_{\text{ref}}(\cdot|x))\bigr]$$

where $\pi_{\text{ref}}$ is the frozen SFT policy and $\beta$ controls the KL penalty strength.

### DPO

Direct Preference Optimisation (Rafailov et al. 2023) eliminates the reward model entirely by directly optimising the policy on preference pairs. DPO re-parameterises the reward in terms of the policy log-ratios and derives a simplified training objective:

$$\mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E}_{(x, y_w, y_l)}\!\left[\log \sigma\!\left(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]$$

DPO is simpler to implement, more stable to train, and empirically competitive with or superior to RLHF on standard alignment benchmarks. Its adoption has accelerated rapidly since publication.

<!-- BOOK-ONLY: Full derivation of the DPO objective from the KL-regularised reward maximisation problem, including the closed-form optimal policy and the substitution that eliminates the reward model, is presented in the companion chapter. -->

---

## 12. Finance Models, Evaluation, Safety, and Governance

### Finance-Specific Pre-trained Models

FinBERT, introduced by Yang et al. (2020), adapts BERT-large by continuing pre-training on approximately 4.9 billion tokens of Reuters news, Financial PhraseBank, and analyst reports, then fine-tuning for sentiment classification with a CLS-head:

$$\hat{y} = \mathrm{softmax}(W_c \cdot h_{\mathrm{[CLS]}} + b_c)$$

where $h_{\mathrm{[CLS]}}$ is the final-layer representation of the `[CLS]` token. FinBERT achieves 88.5% accuracy on the Financial PhraseBank (all-agree split), versus 80.7% for a general BERT-large baseline — a substantial margin for a task where even human annotators do not always agree. This gain comes almost entirely from domain-specific continued pre-training, not architectural changes.

BloombergGPT (Wu et al. 2023) trained a 50B-parameter decoder model on a corpus of 363B tokens: 363B tokens split approximately 51% Bloomberg financial data and 49% general web and book text. Rather than absolute positional embeddings, BloombergGPT uses ALiBi (Attention with Linear Biases), which adds a position-dependent bias to the attention logit:

$$\text{score}(q_i, k_j) = q_i^\top k_j / \sqrt{d_k} - m \cdot (i - j)$$

where $m$ is a head-specific slope and $(i - j)$ is the distance between query and key positions. ALiBi extrapolates more gracefully to sequences longer than those seen during training. However, analysis by independent researchers suggests BloombergGPT falls below the Chinchilla compute-optimal frontier: its 363B-token training run is under-scaled relative to a 50B-parameter model, which by Chinchilla should see approximately 1T tokens. This is a practical lesson about the importance of the $D^*/N^* \approx 20$ heuristic.

PIXIU and FinMA (Xie et al. 2023) address the instruction-following deficit in finance by assembling 136K financial instruction samples across NLP and prediction tasks, fine-tuning LLaMA to produce FinMA. Task-specific finance models include NER systems using BIO tagging heads (Beginning-Inside-Outside labelling of entity spans), FinQA program executors that generate structured calculation programs alongside natural-language reasoning, and summarisation models with factuality-aware objectives that penalise hallucination of numerical values.

### Evaluation Metrics

Perplexity measures a language model's average surprise on a test corpus. For a test sequence of $T$ tokens, it is defined as:

$$\text{PPL} = 2^H, \qquad H = -\frac{1}{T}\sum_{t=1}^{T} \log_2 p(x_t \mid x_{<t})$$

Perplexity has three important limitations: it is not directly interpretable as a task performance metric; it can be gamed by models that assign probability mass to rare but unimportant tokens; and it requires access to token-level probabilities, which API-only models may not provide.

For classification tasks, macro-averaged F1 aggregates per-class precision and recall unweighted by class frequency:

$$\text{Macro-F1} = \frac{1}{K}\sum_{k=1}^{K} \frac{2 \cdot P_k \cdot R_k}{P_k + R_k}$$

For summarisation, ROUGE-N measures n-gram overlap between a generated summary and one or more reference summaries:

$$\text{ROUGE-N} = \frac{\sum_{\text{ref}} \sum_{g \in \text{ngrams}(ref, N)} \text{count}_{\text{match}}(g)}{\sum_{\text{ref}} \sum_{g \in \text{ngrams}(ref, N)} \text{count}(g)}$$

FinBen (Xie et al. 2024) is the most comprehensive finance-specific benchmark at time of writing, covering 42 datasets, 24 tasks, and evaluating 21 models. A consistent finding across the FinBen evaluations is that LLMs perform well on information extraction and classification tasks but struggle on forecasting and decision-support tasks — precisely the tasks of greatest practical interest to finance practitioners.

### Red-Teaming and Financial Failure Modes

Systematic red-teaming of finance LLMs identifies four recurring failure modes: generating plausible but incorrect price forecasts (factual hallucination); reproducing outdated regulatory requirements as current (temporal hallucination); providing what appears to be personalised investment advice without the required licensing disclosures (regulatory compliance failure); and amplifying consensus analyst views while suppressing dissenting signals (herd-bias amplification). Lopez-Lira and Tang (2023) document an empirical illustration of this trajectory: a long-short strategy based on ChatGPT sentiment scores achieved a Sharpe ratio above 6 in 2021, declining toward 1 by late 2024 as the signal was widely adopted and arbitraged away — a reminder that any data-driven alpha source degrades as it becomes public knowledge.

### Bias Sources

Four categories of bias are particularly important in financial LLMs. Survivorship bias arises when training corpora overrepresent successful firms and outcomes (public companies file with EDGAR; bankrupt or never-public firms do not). Temporal bias emerges when models trained on historical data are deployed in structurally different market regimes. Geographic bias follows from the dominance of English-language, US-centric financial text in open web corpora. Analyst consensus bias reflects the tendency of financial commentary to echo dominant views, which are overrepresented in the training distribution.

### Hallucination Mitigations

Four principal mitigations address LLM hallucination in financial applications. Retrieval-augmented generation (RAG) grounds model outputs in retrieved passages from a verified document store, reducing the model's reliance on parametric memory for factual claims. Confidence calibration trains models to express appropriate uncertainty by comparing predicted confidence to empirical accuracy; well-calibrated models say "I am not sure" when they are in fact likely to be wrong. Output verification applies a separate verification model or rule-based checker to flag responses that contain claims inconsistent with a structured knowledge base. Human-in-the-loop workflows route low-confidence or high-stakes outputs to a human expert before they are delivered to end users.

### Regulatory Governance

MiFID II Article 37 establishes that research produced or distributed by investment firms must be independent from commercial pressures and clearly identified as such. When an LLM contributes to investment research, the firm must demonstrate that the model's outputs satisfy suitability (the analysis is appropriate for the recipient's stated risk profile) and explainability requirements (the reasoning behind a recommendation is traceable and auditable). Attention weight visualisations, while sometimes used to argue for explainability, do not satisfy these requirements because they reflect token-level co-occurrence patterns, not causal reasoning chains.

SR 11-7, the US Federal Reserve's supervisory guidance on model risk management, requires a tiered validation framework proportional to model risk. High-risk models (those influencing credit, capital, or trading decisions) require independent validation, documentation of assumptions, and periodic performance monitoring. LLMs used in any of these capacities fall under this guidance.

The EU AI Act, with high-risk system provisions becoming enforceable in August 2026, classifies certain financial AI applications as high-risk and mandates conformity assessments, technical documentation, human oversight mechanisms, and registration in an EU database. A four-component governance framework appropriate for financial LLM deployment comprises: (1) risk classification (Low/Medium/High) based on the decision being supported and the autonomy given to the model; (2) audit trails capturing input prompts, retrieved context, model outputs, and user actions; (3) ongoing monitoring of output distributions for drift and degradation; and (4) an incident response process for rapid mitigation when model failures are detected.

*The discussion exercise in Practical 3 asks you to assign tier-risk classifications to three concrete financial LLM deployments and justify each classification using these four components.*

---

## Summary

This lecture has traced the full lifecycle of a finance LLM, from the raw text it is trained on to the governance frameworks that surround its deployment. Data composition and quality determine the model's domain vocabulary and factual coverage; the Chinchilla scaling laws prescribe how to allocate a compute budget between model size and training tokens; distributed training makes it practical to execute those budgets; and parameter-efficient fine-tuning methods such as LoRA make domain adaptation accessible without the hardware demands of full fine-tuning. Instruction tuning and RLHF align the model's outputs with human preferences, while DPO provides a simpler path to the same goal. Finance-specific models like FinBERT and BloombergGPT demonstrate both the gains achievable through domain adaptation and the pitfalls of under-training relative to Chinchilla optima. Evaluation must go beyond perplexity to task-specific metrics and red-teaming, and governance frameworks — MiFID II, SR 11-7, and the EU AI Act — are not optional overlays but structural requirements for any production deployment.

Lecture 4 builds on this foundation by examining how trained and fine-tuned LLMs are composed into agents: systems that can plan multi-step workflows, call external tools, retrieve from databases, and operate autonomously within bounded decision environments. The shift from a single model producing a single response to an orchestrated network of models and tools introduces new challenges around reliability, cost management, and oversight that are directly relevant to financial process automation.

---

## Further Reading

See the companion book chapter: *Chapter 3 — Training and Fine-Tuning Large Language Models* for full derivations, proofs, extended examples, and references.

Key papers: Hoffmann et al. (2022) "Training Compute-Optimal Large Language Models" (Chinchilla); Hu et al. (2021) "LoRA: Low-Rank Adaptation of Large Language Models"; Rafailov et al. (2023) "Direct Preference Optimization"; Yang et al. (2020) "FinBERT: A Pretrained Language Model for Financial Communications"; Wu et al. (2023) "BloombergGPT: A Large Language Model for Finance"; Xie et al. (2023) "PIXIU: A Large Language Model, Instruction Data and Evaluation Benchmark for Finance"; Lopez-Lira and Tang (2023) "Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models".
