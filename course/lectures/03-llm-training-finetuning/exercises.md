# Exercises — Lecture 3: Training and Fine-Tuning Large Language Models

---

**Exercise 1 [B] — Chinchilla Scaling**

Using the Chinchilla scaling law $N_{\text{opt}} \propto C^{0.5}$ and $D_{\text{opt}} \propto C^{0.5}$, estimate the optimal number of parameters and training tokens for a model trained with a compute budget of $10^{23}$ FLOPs. Assume a standard transformer where one forward pass costs approximately $6N$ FLOPs per token. Compare your answer to the GPT-3 training run ($175\text{B}$ parameters, $300\text{B}$ tokens) and comment on whether GPT-3 is compute-optimal.

*(Covers Section 2: Pre-training Objectives and Scaling)*

---

**Exercise 2 [I] — LoRA Fine-Tuning on FinSentiment**

You are given a pre-trained `bert-base-uncased` model and the Financial PhraseBank dataset (sentences labelled positive/neutral/negative). Apply LoRA fine-tuning with rank $r \in \{4, 8, 16\}$ to the attention weight matrices $W_Q$ and $W_V$. For each rank:

1. Report the number of trainable parameters as a fraction of total parameters.
2. Report accuracy and macro-F1 on the held-out test set.
3. Plot the training loss curves.

Discuss the trade-off between model capacity (rank) and regularisation. Compare against a full fine-tuning baseline and a frozen-encoder linear probe.

*(Covers Sections 3 and 4: Transfer Learning, Fine-Tuning, and Finance Models)*

---

**Exercise 3 [A] — Evaluating Hallucination Under Distribution Shift**

Fine-tune a small generative model (e.g., `GPT-2` or `Mistral-7B-Instruct`) on a set of historical earnings call transcripts from S\&P~500 companies. Then prompt it to generate summaries for transcripts from a sector and time period it has not seen during training.

1. Build an automated factuality checker using named-entity extraction: compare entities mentioned in the generated summary against those in the source transcript.
2. Report a hallucination rate (fraction of generated facts unsupported by the source) for in-distribution vs out-of-distribution prompts.
3. Apply at least one mitigation strategy (e.g., retrieval-augmented grounding, constrained decoding, or self-consistency sampling) and report the improvement.
4. Discuss the implications for a compliance officer relying on LLM-generated summaries under MiFID~II requirements.

*(Covers Sections 5 and 6: Evaluation, Safety, and Responsible AI)*
