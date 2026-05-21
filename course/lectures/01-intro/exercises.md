# Exercises — Lecture 1: Introduction to LLMs in Finance

**Difficulty tags:** [B] = Beginner, [I] = Intermediate, [A] = Advanced

---

**Exercise 1.1 [B]** *(Section 3 — Classical Text Representations)*

Given the following three sentences from earnings call transcripts:

1. "Revenue growth was strong this quarter."
2. "Strong revenue growth was observed."
3. "The quarter showed weak performance."

(a) Build the vocabulary (unique tokens, lowercase, ignore punctuation).
(b) Construct the bag-of-words matrix (documents × vocabulary).
(c) Compute TF-IDF scores manually for the word "strong" across all three documents.

[Solution placeholder — invoke /draft-exercises to generate worked solution]

---

**Exercise 1.2 [I]** *(Section 4 — Word Embeddings / PCA Case Study)*

Using the pre-trained `finance-word2vec` embeddings provided in `code/notebooks/01-intro/demo.ipynb`:

(a) Retrieve the embeddings for the words: `profit`, `loss`, `dividend`, `risk`, `volatility`, `merger`.
(b) Compute pairwise cosine similarities and display as a heatmap.
(c) Apply PCA to reduce to two dimensions and plot. Label each point with the word.
(d) Interpret the clusters: which words end up close together, and why?

[Placeholder]

---

**Exercise 1.3 [A]** *(Section 7 — Transformer Architecture)*

Implement a single-head self-attention layer from scratch in NumPy (no PyTorch/TensorFlow).

(a) Write a function `self_attention(Q, K, V, mask=None)` that computes
    $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$.
(b) Test it on a toy sequence of five tokens with $d_k = d_v = 8$.
(c) Add an optional causal mask (upper-triangular $-\infty$) and verify that future tokens are masked out.
(d) Explain in one paragraph why masking is necessary for autoregressive generation but not for BERT-style encoders.

[Placeholder]
