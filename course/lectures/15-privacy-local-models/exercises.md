# Exercises — Lecture 15: LLMs and Privacy

**Difficulty tags:** [B] = Beginner, [I] = Intermediate, [A] = Advanced

---

**Exercise 15.1 [B]** *(Section 4 — Text Anonymisation and De-identification)*

You are given the following excerpt from a synthetic loan application:

> "John Smith, residing at 14 Rue de Rivoli, Paris 75001, is applying for a mortgage
> of €450,000. His IBAN is FR76 3000 6000 0112 3456 7890 189."

(a) List every piece of personally identifiable information (PII) in the excerpt.
Classify each item by PII category (name, address, financial identifier, etc.).

(b) Apply a masking strategy: replace each PII item with a typed placeholder, e.g.
`[NAME]`, `[ADDRESS]`, `[IBAN]`.

(c) Explain why simple keyword-based masking would fail to catch the IBAN, and
describe what kind of pattern matcher or model you would need instead.

[Solution placeholder — invoke /draft-exercises to generate worked solution]

---

**Exercise 15.2 [I]** *(Section 4 — Named Entity Recognition for Sensitive Data)*

Using the `spaCy` library and a fine-tuned NER model of your choice:

(a) Write a Python function `anonymise(text: str, entities: list[str]) -> str` that
detects entities of the specified types in `text` and replaces each span with a
deterministic surrogate (e.g., the first occurrence of a `PERSON` entity becomes
`PERSON_001`, the second `PERSON_002`, and so on).

(b) Apply your function to the five synthetic earnings-call sentences provided in
`code/practicals/15-privacy-local-models/`. Report which entity spans
were detected and which were missed.

(c) Propose two strategies to improve recall for financial entity types (e.g., ticker
symbols, account numbers) that general-purpose NER models typically miss.

[Placeholder]

---

**Exercise 15.3 [A]** *(Section 5 — Privacy-Preserving Training Techniques)*

A bank wants to fine-tune a summarisation LLM on 10,000 internal credit reports
distributed across five branches, each subject to data-residency requirements that
prevent raw data from leaving the branch.

(a) Sketch a federated learning architecture that satisfies the data-residency
constraint. Specify: (i) what each client computes locally, (ii) what is aggregated
at the server, and (iii) how the global model is broadcast back.

(b) Explain how adding Gaussian noise to the gradients before aggregation (DP-SGD)
provides a ($\varepsilon$, $\delta$)-differential privacy guarantee. What is the
privacy--utility trade-off as $\varepsilon \to 0$?

(c) Suppose the bank also wants to verify that none of the branch-level gradient
updates leak raw training examples. Describe one cryptographic protocol (e.g.,
secure aggregation) that achieves this and outline its communication cost.

[Placeholder]
