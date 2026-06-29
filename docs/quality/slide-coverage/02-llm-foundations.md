# Slide Coverage — 02-llm-foundations

Generated from `book/chapters/02-llm-foundations/chapter.tex` (2,966 lines).

---

## Concept Checklist

### §1 Document-Level Representations
- [x] \section{Document-Level Representations} — overview of aggregation problem
- [x] \subsection{Averaging Word Vectors} — mean embedding definition
- [x] Mean embedding = BoW (Proposition + proof)
- [x] Mean embedding weaknesses: equal weighting, no order, corpus-mean convergence, OOV
- [x] \subsection{Weighted Aggregation and Sentence Transformers}
- [x] TF-IDF weighted embedding (Definition)
- [x] SIF — Smooth Inverse Frequency (Arora et al., 2017) — weight α=a/(a+p(w)) + first-PC removal
- [x] Static embedding limitation: polysemy — bank/yield/default/position examples
- [x] Contextual Embeddings — ELMo (Peters et al., 2018)
- [x] BERT contextual embeddings — context-dependent token representations
- [x] Sentence-BERT (SBERT) — Siamese fine-tuning on NLI; mean pooling vs [CLS] pooling
- [x] Mean Pooling in SBERT (Definition, masked mean)
- [x] [CLS] vs mean pooling — mean pooling consistently outperforms without explicit fine-tuning
- [x] SBERT applications: earnings-call similarity, 10-K product-proximity, regulatory semantic search, guidance credibility
- [x] Context window limits — BERT: 512 tokens; Longformer (Beltagy et al., 2020): 4,096+
- [x] Long-document strategies: truncation, chunking (overlapping windows), hierarchical encoding

### §2 Sequential Models: From RNNs to Attention
- [x] \section{Sequential Models} — motivation: financial text is sequential
- [x] \subsection{Recurrent Neural Networks} — vanilla RNN definition (Definition)
- [x] BPTT formula for gradient (eq. bptt-chain)
- [x] Vanishing and Exploding Gradients Proposition (spectral norm bound)
- [x] Gradient clipping remedy (Pascanu et al., 2013)
- [x] Finance implication: 10,000-token earnings call makes long-range dependencies unlearnable
- [x] \subsection{LSTMs and GRUs} — LSTM (Definition, 6 equations: f,i,g,c,o,h)
- [x] LSTM gate intuitions: forget/input/candidate/output
- [x] Additive cell state — constant error carousel (Hochreiter & Schmidhuber, 1997)
- [x] Cell-state gradient analysis
- [x] GRU (Cho et al., 2014) — Definition (4 equations: z,r,h̃,h); GRU vs LSTM tradeoffs (Chung et al., 2014)
- [x] Bidirectional LSTM (Schuster & Paliwal, 1997) — concatenate forward + backward hidden states
- [x] BiLSTM finance applications: credit-event NER, earnings-surprise prediction
- [x] \subsection{The Attention Mechanism} — bottleneck in seq2seq models
- [x] Bahdanau additive attention (Definition): alignment score, attention weights, context vector
- [x] Attention weights form probability distribution (Proposition)
- [x] Self-attention: apply attention within a single sequence

### §3 The Transformer Architecture
- [x] "Attention Is All You Need" (Vaswani et al., 2017) — historical significance
- [x] Three RNN failure modes: vanishing gradients, sequential bottleneck, fixed-capacity memory
- [x] Encoder–Decoder architecture overview (Figure ch02-transformer-pipeline)
- [x] Encoder: bidirectional multi-head self-attention + FFN
- [x] Decoder: masked self-attention + cross-attention + FFN; causal mask
- [x] \subsection{Self-Attention} — scaled dot-product attention (Definition)
- [x] Q, K, V projection matrices; QK⊤ scores; row-wise softmax; output = convex combination of values
- [x] sqrt(dk) scaling proposition — normalises pre-softmax variance to 1
- [x] Causal mask (eq. causal-mask) — -inf for j>i
- [x] \subsection{Multi-Head Attention} — Definition (h heads, concat, W^O)
- [x] Original Transformer: h=8, d_model=512, d_k=d_v=64
- [x] Complexity O(n² d_model); FlashAttention (Dao et al., 2022) motivation
- [x] Head specialisation probing studies (Clark et al., 2019) — syntactic vs semantic heads
- [x] Kernel trick connection (Tsai et al., 2019); Performers / random feature attention O(n)
- [x] \subsection{Positional Encoding} — permutation equivariance problem
- [x] Sinusoidal PE (Definition, sin/cos formulas) — multi-scale Fourier basis
- [x] Rotation property Proposition (Shaw et al., 2018) — relative positions linearly decodable
- [x] RoPE — Rotary Position Embeddings (Su et al., 2024); used in Llama, Mistral, Qwen
- [x] fig_illustration.png embedded — heatmap d_model=64, seq_len=50
- [x] \subsection{Encoder–Decoder Structure} — encoder layer equations (LayerNorm + residual)
- [x] FFN sub-layer — ReLU (later GELU, Hendrycks & Gimpel 2016); d_ff = 4 d_model
- [x] Decoder cross-attention equation
- [x] Base model: L=6; large: L=24; modern LLMs: L=32–96
- [x] \subsection{Special Tokens} — [CLS], [SEP], [MASK], <pad>, <eos>, <bos>, <unk>
- [x] Finance consequences of misusing special tokens
- [x] \subsection{Numerical Walk-Through} — step-by-step tiny GPT forward pass (7 steps) [added 2026-06-28: "Seven steps from tokens to next-word probability" slide; numeric trace in underhood]
- [x] \subsection{Pre-training, Fine-tuning, BERT vs GPT}
- [x] Pre-training definition; fine-tuning definition
- [x] BERT MLM loss (15% masking: 80/10/10 protocol); encoder-only; bidirectional
- [x] NSP objective; RoBERTa (Liu et al., 2019) removed NSP
- [x] GPT CLM loss; causal mask; autoregressive factorisation
- [x] KV-cache explanation
- [x] Encoder-only vs decoder-only vs enc-dec task suitability table
- [x] FinBERT — two independently trained variants: Araci (2019) on Reuters/Bloomberg/10-K; Huang (2023) on analyst labels
- [x] BloombergGPT (Wu et al., 2023) — 50B params, 363B fin + 345B general tokens

### §4 The Modern LLM Landscape
- [x] Autoregressive language model (Definition, product factorisation)
- [x] \subsection{Generative Models vs Reasoning Models}
- [x] Reasoning model (Definition, CoT trace, marginalisation, single-sample MC approximation)
- [x] Self-consistency decoding (Wang et al., 2022)
- [x] Merger valuation example contrasting standard vs reasoning model
- [x] \subsection{Major Model Families} — GPT-4/4o, Claude 3/4, Llama 3, Gemini 1.5 Pro, FinBERT, BloombergGPT (Table)
- [x] LopezLira & Tang (2023) — ChatGPT headline sentiment predicts next-day returns; predictability increases with scale
- [x] Emergent capabilities (Wei et al., 2022) — scale compensates for domain specificity
- [x] Instruction tuning + RLHF (Ouyang et al., 2022, InstructGPT) — reward model, PPO
- [x] \subsection{Financial NLP Benchmarks} — FinancialPhraseBank, FiQA, ECTSum, FinQA, FLUE (Table)
- [x] Geographic bias remark — all five benchmarks North American/English

### §5 Temperature, Sampling, and Controlled Generation
- [x] Temperature-scaled softmax (Definition)
- [x] Shannon entropy strictly increasing in τ
- [x] Top-k Sampling (Definition)
- [x] Nucleus (Top-p) Sampling (Definition, Holtzman et al., 2020)
- [x] Beam Search (Definition, score = accumulated log-prob, top-B hypotheses)
- [x] Beam search degeneration on open-ended generation
- [x] \subsection{Sampling Strategy Selection for Financial Tasks} — table (Table sampling-strategies)

### §6 Structured Generation
- [x] Token-Level Validity Mask (Definition, pre-softmax -inf)
- [x] JSON Mode and Tool Use — Anthropic tool use; Pydantic model; tool_choice parameter
- [x] Grammar-Based Generation — outlines library; EBNF; GBNF for llama.cpp; XBRL/MiFID II
- [x] Three failure modes: numerical hallucination, field omission, unit confusion

### §7 Working with LLMs via API
- [x] Token definition (Definition) — sub-word, BPE, WordPiece
- [x] BPE algorithm (4 steps: init chars → count pairs → merge most frequent → repeat)
- [x] BPE example: "earnings" → ["earn","ings"]; "EBITDA" → ["EB","IT","DA"]; 1.3 tokens/word
- [x] Context window (Definition) — max tokens in single forward pass
- [x] Context window growth: GPT-3 4K → GPT-4-turbo 128K → Claude 200K → Gemini 1M
- [x] Cost model equation (N_in * c_in + N_out * c_out)
- [x] API pricing table (GPT-4o $5/$15; Claude Haiku $0.25/$1.25; Llama self-hosted ~$0)
- [x] Worked cost example: 10,000 transcripts; GPT-4o ≈$410; Haiku ≈$20
- [x] Python walkthrough: OpenAI, Anthropic, HuggingFace/FinBERT — API comparison table
- [x] Prompt Caching (Remark) — 90% discount on cached prefix; up to 90% cost reduction

### §8 Retrieval-Augmented Generation
- [x] RAG Pipeline (Definition, 3 stages: retrieval, augmentation, generation)
- [x] Dense retrieval — cosine similarity, SBERT bi-encoder, FAISS/HNSW ANN
- [x] Chunking strategy — 512-token passages with 50-token overlap
- [x] BM25 sparse retrieval — exact-match; CUSIPs, clause references, tickers
- [x] Hybrid retrieval — Reciprocal Rank Fusion (Cormack et al., 2009), k_rrf=60
- [x] Re-ranking — cross-encoder; ColBERT (Khattab & Zaharia, 2020) late-interaction MaxSim
- [x] FinanceBench (Zhang et al., 2024) — GPT-4-Turbo incorrectly answers/refuses 81% of SEC questions

### §9 Knowledge Distillation and Model Compression
- [x] Deployment problem: 70B model needs 140 GB VRAM, seconds of latency
- [x] Knowledge Distillation (Definition) — teacher/student; KD loss = α*CE + (1-α)*τ²*KL
- [x] Soft labels encode inter-class similarity invisible in hard labels
- [x] Forward vs Reverse KL (Remark) — forward is mean-seeking; reverse is mode-seeking
- [x] LoRA — Low-rank adaptation (Hu et al., 2022) — ΔW=BA, r<<min(d,k), 128x param reduction
- [x] QLoRA (Dettmers et al., 2023) — 4-bit NF4 frozen weights; BF16 adapters; 7B on one A100
- [x] Quantisation — PTQ without gradient updates; works on downloaded weights
- [x] GPTQ (Frantar et al., 2022) — layer-wise second-order; INT4 matches FP16 perplexity
- [x] AWQ (Lin et al., 2023) — protect high-activation weight channels; better accuracy-compression
- [x] Pruning — unstructured (zero weights) vs structured (remove heads/blocks)
- [x] Lottery ticket hypothesis (Frankle & Carlin, 2019) — sparse winning subnetworks

### §10 Hallucinations: Detection and Mitigation
- [x] Intrinsic vs extrinsic hallucination (Maynez et al., 2020)
- [x] Numerical hallucination — D/E 1.8 reported as 0.8
- [x] Entity hallucination — wrong company/regulatory body
- [x] Citation hallucination — fabricated regulation/ruling/standard (Ji et al., 2023)
- [x] Root cause: trained for plausibility, not accuracy; τ=0 removes randomness not hallucination
- [x] Kang et al. (2023) — systematic empirical hallucination study in financial tasks
- [x] SelfCheckGPT (Manakul et al., 2023) — N samples; NLI consistency score
- [x] FActScore (Min et al., 2023) — decompose into atomic claims; verify against source
- [x] Inner confidence (Chen et al., 2024) — entropy-based; Sharpe +20% on high-confidence signals
- [x] Mitigation 1: RAG — most effective for extrinsic hallucination
- [x] Mitigation 2: Self-consistency (Wang et al., 2022) — K chains, majority vote
- [x] Mitigation 3: Chain-of-thought (Wei et al., 2022) — explicit steps, verifiable
- [x] Mitigation 4: Claim decomposition (FActScore) — atomic claim verification
- [x] Mitigation 5: Confidence elicitation + abstention — calibration curves

### §11 Limitations and Responsible Use
- [x] EU AI Act (Reg. 2024/1689, Aug 2024) — high-risk: credit scoring, insurance pricing, algo trading
- [x] SEC guidance on AI — fiduciary duty; advisers responsible for AI-generated outputs
- [x] Look-ahead bias (Didisheim et al., 2025) — LLMs reconstruct historical time series from memory
- [x] GDPR (EU 2016/679) — right to erasure; data-transfer restrictions; retraining required
- [x] Geographic bias — five benchmarks all North American/English; sentiment models misread Asian markets

---

## Omissions

All items in the checklist above were gaps relative to the original deck. The following were added in the P3 rewrite:

- [x] Polysemy section with finance examples (bank/yield/default/position)
- [x] Long-document strategies (truncation, chunking, hierarchical)
- [x] BiLSTM slide — bidirectional concatenation, finance pre-2018 applications
- [x] Special tokens slide — [CLS]/[SEP]/[MASK]/<pad>/<eos>/<unk> with finance consequences
- [x] Reasoning models dedicated slide — CoT, RL reward, o1/o3/DeepSeek-R1, merger valuation example
- [x] RLHF + instruction tuning slide — reward model, PPO, LopezLira & Tang (2023)
- [x] Section 06 (Model compression) — knowledge distillation slide
- [x] Section 06 (Model compression) — LoRA/QLoRA slide
- [x] Section 06 (Model compression) — GPTQ/AWQ/Pruning slide
- [x] fig_illustration.png embedded on positional encoding slide
- [x] Badge changed to "Summer school · math one click away — press m or click ⚙ Under the hood"
- [x] "MBA" references removed from heading and badge in both decks
- [x] GPT-4o params cell corrected from "~1T" (unsubstantiated rumour) to "n/d" to match chapter.tex line 1685 [fix 2026-06-28]
- [x] Numerical walk-through slide added (index.html): 7-step forward pass with plain-language lead + underhood numeric trace faithful to chapter §3.6 [fix 2026-06-28]
- [x] practical.html BPE example updated from "CUSIP"→["C","US","IP"] to "earnings"→["earn","ings"] to match chapter examples [fix 2026-06-28]
