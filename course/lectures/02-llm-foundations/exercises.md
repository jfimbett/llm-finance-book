# Exercises — Lecture 2: LLM Architecture and Practice

**Exercise 2.1 [B]** *(Temperature Sampling)*

Given logits $\mathbf{z} = [2.0,\ 1.0,\ 0.1]$ over a three-token vocabulary:
(a) Compute the softmax probabilities at $\tau = 1.0$.
(b) Compute the softmax probabilities at $\tau = 0.5$ and $\tau = 2.0$.
(c) Which $\tau$ would you use for deterministic financial data extraction, and why?

[Solution placeholder]

---

**Exercise 2.2 [I]** *(Structured Generation)*

Using the `instructor` library and the Anthropic API, write a Python function
`extract_earnings(text: str) -> EarningsReport` where `EarningsReport` is a
Pydantic model with fields `revenue`, `net_income`, `eps`, `guidance` (all floats,
nullable). Test it on the sentence: "Revenue came in at \$4.2B, net income was
\$820M, EPS of \$1.34, and the company raised full-year guidance to \$5.1B."

[Placeholder]

---

**Exercise 2.3 [A]** *(RAG Pipeline)*

Build a minimal RAG pipeline for 10-K filings:
(a) Chunk a sample 10-K into 512-token passages.
(b) Embed each passage with `sentence-transformers/all-MiniLM-L6-v2`.
(c) Store in a FAISS index.
(d) Given the query "What are the company's main risk factors?", retrieve the
    top-3 passages and use them as context to answer with Claude.
(e) Measure answer faithfulness: do all factual claims in the answer appear in
    the retrieved passages?

[Placeholder]
