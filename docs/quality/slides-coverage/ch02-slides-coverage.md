# Slides Coverage Audit — Chapter 2: Large Language Models: Architecture and Practice

> **✅ RESOLVED (commit `e83346f`).** Both minor gaps below were closed in the lesson
> deck: *prompted self-critique* added as the 6th hallucination defense, and a
> *US / SEC fiduciary duty* bullet added to the responsible-use slide. Report retained
> as the historical audit record.

**Verdict:** GAPS FOUND (0 critical, 2 minor) — *both resolved*
**Slides-only student:** Can follow the entire chapter end to end — every load-bearing concept (architecture arc, self-attention math, sampling, RAG, compression, hallucination) is on the slides, often with the full formula in an under-the-hood panel; only two secondary governance/mitigation items are thinner than the book.

---

## CRITICAL — load-bearing concepts a slides-only student would miss

None. The lesson and practical decks together cover all core, load-bearing units: document representations (mean/TF-IDF/SBERT, polysemy, long-doc strategies), the RNN→LSTM→GRU→BiLSTM→attention→Transformer progression with the vanishing-gradient proposition, scaled dot-product + √dₖ (proof in the appendix), causal mask, multi-head, sinusoidal PE + rotation property + RoPE, residual/LayerNorm/FFN/cross-attention, special tokens, the seven-step tiny-GPT forward pass with the numeric trace, BERT(MLM)/GPT(CLM)/pretraining-finetuning, reasoning vs. generative models, RLHF, the model-family and benchmark tables, temperature/top-k/nucleus/beam, constrained decoding + tool use + the three failure modes, BPE/cost/context/prompt-caching, the three-stage RAG pipeline with dense/BM25/hybrid-RRF/re-ranking and FinanceBench, and KD/LoRA/QLoRA/GPTQ/AWQ/pruning.

---

## MINOR — present but under-explained

### Finding 1 — Self-critique / Constitutional-AI mitigation — ✅ RESOLVED (`e83346f`)
- **On the slides:** The lesson "stack five defenses" slide (§05) lists RAG, self-consistency, chain-of-thought, claim decomposition (FActScore), and confidence elicitation + abstention. The book lists a sixth — Constitutional AI / its inference-time analogue **prompted self-critique** (Sec `sec:hallucinations-mitigation`), where a second pass instructs the model to verify each claim against the source and retract unlocatable assertions.
- **What is thin:** Prompted self-critique is the one mitigation a closed-API practitioner can actually deploy without weights, and it is absent from the deck. The "layer complementary defenses" principle survives, but a slides-only student misses a practical, named technique.
- **Suggested slide treatment:** Add one fragment bullet to the defenses slide: "Prompted self-critique — a second pass that re-checks every claim against the source and retracts unsupported ones (inference-time analogue of Constitutional AI, Bai et al. 2022)."

### Finding 2 — Fiduciary responsibility / US (SEC) regulatory exposure — ✅ RESOLVED (`e83346f`)
- **On the slides:** The responsible-use slide (§05) covers EU AI Act, look-ahead bias (Didisheim et al.), GDPR, and geographic bias well. The book's `sec:limitations-ethics` additionally develops the **fiduciary-duty** theme: SEC staff guidance, the unresolved question of whether an LLM output is a "recommendation," and the consensus that the human adviser/firm retains full responsibility for AI outputs — a thread the chapter flags as recurring (into the agents chapter).
- **What is thin:** For the industry/North-American half of the audience this is a load-bearing governance takeaway (who is liable), and it is missing; the deck's regulatory framing is EU-only.
- **Suggested slide treatment:** Add a bullet to the responsible-use slide: "US / fiduciary duty — SEC posture holds the human adviser fully responsible for AI-generated outputs; 'the model said so' is not a defense."

---

## OK-to-omit — book-only depth, correctly left off the slides

- Full BPTT chain-rule derivation and the vanishing-gradient proof — slide states the bound and its consequence; derivation is reference depth.
- The three-ecosystem API comparison table (OpenAI vs. Anthropic vs. HuggingFace system-prompt/output-access differences) — practical deck shows working Anthropic code, which suffices.
- Forward-vs-reverse-KL mean-seeking/mode-seeking argument — the lesson under-the-hood panel gives the KD loss and the "mean-seeking" one-liner; the full equivalence proof is correctly book-only.
- Niszczota (GPT-4 99% financial-literacy) and other secondary corroborating citations — the emergent-knowledge point is already made on the RLHF slide via Lopez-Lira & Tang.
- The full inline matrices of the tiny-GPT trace (E, W^V, W₁, W₂) — the slide's numeric summary conveys the same intuition.

---

## Coverage Summary Table

| Chapter concept (load-bearing) | Slides status | Tier |
|--------------------------------|---------------|------|
| Doc reps: mean / TF-IDF / SBERT, polysemy, long-doc strategies | COVERED | — |
| RNN vanishing-gradient proposition; LSTM/GRU/BiLSTM; Bahdanau attention | COVERED | — |
| Scaled dot-product + √dₖ, causal mask, multi-head | COVERED | — |
| Positional encoding, rotation property, RoPE | COVERED | — |
| Encoder/decoder layer, residual+LayerNorm, FFN, cross-attention, special tokens | COVERED | — |
| Tiny-GPT seven-step forward pass (numeric trace) | COVERED | — |
| Pretraining/finetuning, BERT MLM vs GPT CLM, FinBERT, BloombergGPT | COVERED | — |
| Generative vs reasoning models, RLHF, benchmarks, model families | COVERED | — |
| Temperature / top-k / nucleus / beam + finance selection table | COVERED | — |
| Constrained decoding, tool use, grammar-based, three failure modes | COVERED | — |
| BPE, cost model, context windows, prompt caching | COVERED | — |
| RAG pipeline, dense/BM25/hybrid-RRF/re-rank/ColBERT, FinanceBench | COVERED | — |
| KD (+KL direction), LoRA/QLoRA, GPTQ/AWQ, pruning/lottery ticket | COVERED | — |
| Hallucination taxonomy + SelfCheckGPT/FActScore/inner confidence | COVERED | — |
| Hallucination mitigation: prompted self-critique / Constitutional AI | COVERED (`e83346f`) | ✅ resolved |
| Responsible use: EU AI Act, look-ahead bias, GDPR, geographic bias | COVERED | — |
| Responsible use: SEC guidance / fiduciary responsibility | COVERED (`e83346f`) | ✅ resolved |
