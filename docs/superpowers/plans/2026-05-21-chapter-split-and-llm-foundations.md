# Chapter Split + LLM Foundations Chapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the current monolithic Chapter 1 into two focused chapters — a concise Introduction (history through embeddings) and a new Chapter 2 covering LLM architecture and practice — then add four new sections: Temperature & Sampling, Structured Generation, Retrieval-Augmented Generation, and Knowledge Distillation, and expand the Hallucinations section with SOTA mitigation techniques.

**Architecture:** Chapter 1 keeps sections 1–4 (lines 1–1257 of the current file) plus a new closing "Looking Ahead" section. Chapter 2 receives the moved sections 5–11 plus the five new/expanded sections, fully scaffolded with lecture notes, slides, exercises, and notebooks. All new LaTeX content is written by the book-writer agent persona with no `\paragraph{}` labels.

**Tech Stack:** LaTeX (pdflatex + biber), biblatex authoryear, mathpazo, titlesec, fancyhdr. Python 3.11 for notebooks.

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Modify | `book/chapters/01-intro/chapter.tex` | Trim to sections 1–4; replace old sections 5–11 with a 1-page "Looking Ahead" closing section |
| Create | `book/chapters/02-llm-foundations/chapter.tex` | New chapter: moved sections 5–11 + 5 new sections |
| Create | `book/chapters/02-llm-foundations/figures/.gitkeep` | Placeholder |
| Create | `course/lectures/02-llm-foundations/notes.md` | Lecture notes skeleton |
| Create | `course/lectures/02-llm-foundations/slides.tex` | Beamer skeleton |
| Create | `course/lectures/02-llm-foundations/exercises.md` | 3 exercises (B/I/A) |
| Create | `course/lectures/02-llm-foundations/solutions.md` | 3 solution placeholders |
| Create | `code/notebooks/02-llm-foundations/demo.ipynb` | Notebook skeleton |
| Create | `code/notebooks/02-llm-foundations/exercises.ipynb` | Exercises notebook |
| Modify | `book/main.tex` | Add `\include{chapters/02-llm-foundations/chapter}` |
| Modify | `docs/STATUS.md` | Add row for Chapter 2 |
| Modify | `book/bibliography.bib` | Add new references for RAG, distillation, structured gen, self-consistency |

---

## Task 1: Trim Chapter 1 — Keep Sections 1–4, Add "Looking Ahead"

**Files:**
- Modify: `book/chapters/01-intro/chapter.tex` (lines 1257 onward)

The chapter currently ends after 11 sections. Keep lines 1–1256 intact (sections 1–4 through the end of the Word Embeddings / PCA case study). Delete everything from line 1258 onward and replace with a new closing section.

- [ ] **Step 1.1: Delete sections 5–11 from chapter.tex**

Open `book/chapters/01-intro/chapter.tex`. Lines 1258–end contain sections 5–11. Remove all content from line 1258 to end-of-file.

- [ ] **Step 1.2: Add "Looking Ahead" closing section**

Append the following to the trimmed file:

```latex
% ---------------------------------------------------------------
\section{Looking Ahead}
\label{sec:intro-looking-ahead}

The representations developed in this chapter treat language as bags of tokens or
low-dimensional geometric objects.  They capture lexical similarity and rudimentary
document structure, but they cannot model syntax, long-range dependencies, or the
meaning of a word in context.  Chapter~\ref{ch:llm-foundations} addresses these
limitations directly.  It derives the recurrent architectures that first brought
sequential order into text modelling, shows why they fail at the scales demanded by
modern financial corpora, and then builds up the Transformer---the architecture
underlying every large language model in use today---from first principles.  It
continues with the practical layer: how to control generation through temperature
and structured decoding, how to ground model outputs in retrieved documents, how to
compress large models into deployable ones, and how to measure and mitigate the
hallucinations that remain the central reliability challenge for LLMs in finance.
```

- [ ] **Step 1.3: Compile to verify Chapter 1 still builds**

```
cd book
pdflatex -interaction=nonstopmode main.tex
```
Expected: exit 0, no `!` errors.

- [ ] **Step 1.4: Commit**

```
git add book/chapters/01-intro/chapter.tex
git commit -m "refine(ch01): trim to introduction scope — sections 1-4 + looking-ahead closing"
```

---

## Task 2: Scaffold Chapter 2 Directory

**Files:**
- Create all paths listed under `02-llm-foundations/` in the file map above.

- [ ] **Step 2.1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force "book/chapters/02-llm-foundations/figures"
New-Item -ItemType Directory -Force "course/lectures/02-llm-foundations"
New-Item -ItemType Directory -Force "code/notebooks/02-llm-foundations"
New-Item -ItemType File "book/chapters/02-llm-foundations/figures/.gitkeep"
```

- [ ] **Step 2.2: Create chapter.tex skeleton**

Create `book/chapters/02-llm-foundations/chapter.tex` with:

```latex
\chapter{Large Language Models: Architecture and Practice}
\label{ch:llm-foundations}

\begin{remark}[Learning Objectives]
After completing this chapter, the reader should be able to:
\begin{enumerate}
  \item Derive the vanishing-gradient bound for RNNs and explain how the LSTM cell
        state resolves it.
  \item State the scaled dot-product attention formula, prove the $\sqrt{d_k}$
        variance normalisation, and describe multi-head attention.
  \item Explain temperature sampling, top-$p$ nucleus sampling, and beam search,
        and choose the right scheme for a given financial NLP task.
  \item Describe constrained decoding and implement structured JSON extraction
        from an LLM using Python.
  \item Build a retrieval-augmented generation pipeline for financial documents.
  \item Explain knowledge distillation, LoRA fine-tuning, and quantisation.
  \item Apply at least three state-of-the-art hallucination-mitigation techniques
        to a financial analysis task.
\end{enumerate}
\end{remark}

% Sections will be added in Tasks 3–8.
% Placeholder — invoke /draft-chapter to generate content.
```

- [ ] **Step 2.3: Create course and notebook skeletons**

`course/lectures/02-llm-foundations/notes.md`:
```markdown
# Lecture 2: Large Language Models — Architecture and Practice

**Paired chapter:** `book/chapters/02-llm-foundations/chapter.tex`

**Learning objectives:**
- [ ] Derive vanishing gradient bound; explain LSTM fix
- [ ] State and prove scaled dot-product attention
- [ ] Choose sampling strategy for a given task
- [ ] Implement structured generation with Pydantic + instructor
- [ ] Build a RAG pipeline for a 10-K filing
- [ ] Explain LoRA and quantisation
- [ ] Apply SOTA hallucination mitigation

---

## 1. Sequential Models: From RNNs to Attention
[Placeholder]
## 2. The Transformer Architecture
[Placeholder]
## 3. Temperature, Sampling, and Generation
[Placeholder]
## 4. Structured Generation
[Placeholder]
## 5. Working with LLMs via API
[Placeholder]
## 6. Retrieval-Augmented Generation
[Placeholder]
## 7. Knowledge Distillation and Model Compression
[Placeholder]
## 8. Hallucinations: Detection and Mitigation
[Placeholder]
## 9. The Modern LLM Landscape
[Placeholder]
## 10. Limitations and Responsible Use
[Placeholder]

---
## Further Reading
See Chapter 2 of the companion book for full mathematical derivations.
```

`course/lectures/02-llm-foundations/exercises.md`:
```markdown
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
```

`course/lectures/02-llm-foundations/solutions.md`:
```markdown
# Solutions — Lecture 2: LLM Architecture and Practice

**Solution 2.1** [Placeholder]

**Solution 2.2** [Placeholder]

**Solution 2.3** [Placeholder]
```

`code/notebooks/02-llm-foundations/demo.ipynb` and `exercises.ipynb`: minimal valid notebooks with one markdown cell describing the chapter topic (same JSON structure as `01-intro` notebooks).

- [ ] **Step 2.4: Update main.tex and STATUS.md**

In `book/main.tex`, add after the Chapter 1 include:
```latex
\include{chapters/02-llm-foundations/chapter}
```

In `docs/STATUS.md`, add:
```
| 02 | LLM Foundations | No | No | — | — | — | — | — | No |
```

- [ ] **Step 2.5: Compile to verify scaffold builds**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```
Expected: exit 0.

- [ ] **Step 2.6: Commit scaffold**

```
git add book/chapters/02-llm-foundations/ course/lectures/02-llm-foundations/ \
        code/notebooks/02-llm-foundations/ book/main.tex docs/STATUS.md
git commit -m "chore: scaffold chapter 02-llm-foundations"
```

---

## Task 3: Move Sections 5–11 from Chapter 1 into Chapter 2

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

The content for Document Representations, RNNs, Transformer Architecture, LLM Landscape, API, Limitations, and Roadmap was already written in the old Chapter 1. It needs to be transplanted and re-labelled.

- [ ] **Step 3.1: Extract lines 1258–end of old Chapter 1**

Read `book/chapters/01-intro/chapter.tex` (after the Task 1 trim it ends at the "Looking Ahead" section). The full moved content was committed before the trim — recover it from git:

```powershell
git show HEAD~1:book/chapters/01-intro/chapter.tex |
  Select-String -Pattern "Document-Level" -List
```

Use `git show <commit>:book/chapters/01-intro/chapter.tex` to extract lines 1258 onward from the pre-trim commit (the commit before Task 1.4).

- [ ] **Step 3.2: Paste extracted content into chapter 2**

Replace the `% Sections will be added in Tasks 3–8` placeholder in `02-llm-foundations/chapter.tex` with the extracted sections. Update the chapter label comment block at the top and add `% --- moved from ch01 ---` comment.

Note: the `\section{Roadmap of This Book}` at the end of the moved content now needs to be renamed to `\section{Chapter Summary}` since the book-wide roadmap lives in Chapter 1. Update its `\label` to `sec:ch2-summary`.

- [ ] **Step 3.3: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
```
Expected: exit 0. Check page count increased.

- [ ] **Step 3.4: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex book/chapters/01-intro/chapter.tex
git commit -m "refine: move sections 5-11 from ch01 into ch02-llm-foundations"
```

---

## Task 4: New Section — Temperature, Sampling, and Generation

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex` (insert before the "Working with LLMs via API" section)

This section must be written with full mathematical rigour. No `\paragraph{}`. All theorems/definitions in proper environments.

- [ ] **Step 4.1: Write the section and insert it**

Insert the following LaTeX block before the `\section{Working with LLMs via API}` section:

```latex
% ---------------------------------------------------------------
\section{Temperature, Sampling, and Controlled Generation}
\label{sec:sampling}

Autoregressive generation produces text one token at a time.  At each step $t$,
the model computes a vector of \emph{logits}
$\mathbf{z}^{(t)} \in \mathbb{R}^{|\mathcal{V}|}$ and converts them to a
probability distribution from which the next token is drawn.  The mapping from
logits to a distribution, and the sampling rule applied to that distribution,
jointly determine the character of the output.  For financial applications this
choice is not cosmetic: it determines whether the model produces a reliable,
deterministic extraction of numerical facts or a plausible-but-fictitious
narrative.

\subsection{Temperature Scaling}
\label{sec:sampling-temperature}

\begin{definition}[Temperature-Scaled Softmax]
\label{def:temperature}
Let $\mathbf{z} = (z_1,\ldots,z_{|\mathcal{V}|}) \in \mathbb{R}^{|\mathcal{V}|}$
be the logit vector at a given generation step and $\tau > 0$ a scalar
\emph{temperature}.  The temperature-scaled probability distribution is
\begin{equation}
  p_i(\tau) = \frac{\exp(z_i / \tau)}{\sum_{j=1}^{|\mathcal{V}|} \exp(z_j / \tau)},
  \quad i = 1,\ldots,|\mathcal{V}|.
  \label{eq:temperature-softmax}
\end{equation}
\end{definition}

[PROSE: explain τ→0 (greedy), τ=1 (standard), τ→∞ (uniform); finance implication]

\subsection{Top-$k$ and Nucleus (Top-$p$) Sampling}
\label{sec:sampling-topk-topp}

[PROSE + DEFINITIONS for top-k and top-p with equations]

\subsection{Beam Search}
\label{sec:sampling-beam}

[PROSE + definition of beam search with score equation]

\subsection{Sampling Strategy Selection for Financial Tasks}
\label{sec:sampling-finance}

[TABLE: task type → recommended τ and sampling strategy with rationale]
% e.g. structured extraction: τ=0, greedy; summarisation: τ=0.3, top-p=0.9;
%      creative scenario generation: τ=0.7, top-p=0.95
```

- [ ] **Step 4.2: Replace `[PROSE...]` and `[TABLE...]` placeholders with full content**

The book-writer agent writes the full prose and table. Each subsection should be 1–2 paragraphs. The table must cover at least: structured data extraction, sentiment labelling, document summarisation, scenario/stress-test narrative generation, and regulatory Q&A.

Key equations to include:
- Entropy of $p(\tau)$: $H(\tau) = -\sum_i p_i(\tau)\log p_i(\tau)$, show $H$ is monotone increasing in $\tau$.
- Top-p formal definition: $\mathcal{V}_p = \arg\min_{S \subseteq \mathcal{V}} \{|S| : \sum_{i \in S} p_i \geq p\}$

- [ ] **Step 4.3: Compile**

Expected: exit 0.

- [ ] **Step 4.4: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): add temperature and sampling section"
```

---

## Task 5: New Section — Structured Generation

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex` (insert after Temperature section)

- [ ] **Step 5.1: Write and insert the section**

```latex
% ---------------------------------------------------------------
\section{Structured Generation}
\label{sec:structured-gen}

Financial applications rarely need free prose.  A risk-management system extracting
covenant violations from loan agreements needs a precise structured record, not a
narrative.  A trading signal pipeline processing earnings call transcripts requires
numerically reliable fields, not approximate summaries.  \emph{Structured generation}
refers to techniques that constrain the output of a language model to conform to a
predefined schema, grammar, or format.

\subsection{Constrained Decoding}
\label{sec:structured-gen-constrained}

[PROSE: at each generation step, compute a binary mask M_t ∈ {0,1}^{|V|} where M_t[i]=0
if token i cannot appear at position t given the partial output and the target schema.
Apply as: z̃_i = z_i + log(M_t[i]) (i.e., -∞ for invalid tokens). Define formally.]

\begin{definition}[Token-Level Validity Mask]
\label{def:validity-mask}
Given a target grammar $\mathcal{G}$ and partial output $x_{<t}$, the
\emph{validity mask} $M_t \in \{0,1\}^{|\mathcal{V}|}$ is defined by
\begin{equation}
  M_t[i] = \mathbf{1}[\text{token } i \text{ can extend } x_{<t}
            \text{ to a string in } \mathcal{L}(\mathcal{G})],
  \label{eq:validity-mask}
\end{equation}
where $\mathcal{L}(\mathcal{G})$ is the language defined by $\mathcal{G}$.
The masked logits are $\tilde{z}_i = z_i + \log M_t[i]$, so invalid tokens
receive $-\infty$ before softmax.
\end{definition}

\subsection{JSON Mode and Function Calling}
\label{sec:structured-gen-json}

[PROSE: OpenAI JSON mode, Anthropic tool_use, how they implement constrained decoding
internally; example of calling with response_format={"type":"json_object"}]

\begin{lstlisting}[language=Python, caption={Structured extraction with the Anthropic API.}]
import anthropic, json
from pydantic import BaseModel
from typing import Optional

class EarningsReport(BaseModel):
    revenue_bn: Optional[float]
    net_income_bn: Optional[float]
    eps: Optional[float]
    guidance_bn: Optional[float]

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    tools=[{
        "name": "record_earnings",
        "description": "Record structured earnings figures",
        "input_schema": EarningsReport.model_json_schema(),
    }],
    tool_choice={"type": "tool", "name": "record_earnings"},
    messages=[{"role": "user",
               "content": "Extract earnings: Revenue $4.2B, net income $820M, "
                          "EPS $1.34, guidance raised to $5.1B."}]
)
result = EarningsReport(**message.content[0].input)
print(result)
\end{lstlisting}

\subsection{Grammar-Based Generation}
\label{sec:structured-gen-grammar}

[PROSE: EBNF grammars, Outlines library, GBNF in llama.cpp; when to use over JSON mode
(complex nested structures, domain-specific financial formats like XBRL)]

\subsection{Why Structured Generation Is Critical in Finance}
\label{sec:structured-gen-finance}

[PROSE: three concrete failure modes of unstructured generation in finance — (1) number
hallucination in earnings extraction, (2) missing fields silently set to null vs. omitted,
(3) unit confusion ($M vs $B); show how constrained decoding eliminates these; reference
to regulatory reporting requirements (SEC EDGAR XBRL, MiFID II structured reporting)]
```

- [ ] **Step 5.2: Fill all `[PROSE...]` placeholders with full content**

Key points to include:
- The definition must be precise — validity mask is not a post-hoc filter but applied pre-softmax
- The Python listing must compile and run (no syntax errors, Pydantic v2 compatible)
- The finance section must cite at least one empirical failure case

- [ ] **Step 5.3: Compile. Expected: exit 0.**

- [ ] **Step 5.4: Commit**

```
git commit -m "feat(ch02): add structured generation section"
```

---

## Task 6: New Section — Retrieval-Augmented Generation (RAG)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 6.1: Write and insert after the API section**

```latex
% ---------------------------------------------------------------
\section{Retrieval-Augmented Generation}
\label{sec:rag}

Large language models are trained on a fixed corpus with a knowledge cutoff.
In finance, the most relevant information is almost always recent: a 10-K filed
last quarter, a central bank statement from this morning, or a credit agreement
amended last week.  \emph{Retrieval-augmented generation} (RAG) addresses this
by augmenting the model's prompt with passages retrieved at inference time from
an external corpus, combining the reasoning ability of the LLM with up-to-date,
verifiable source material.

\subsection{The RAG Pipeline}
\label{sec:rag-pipeline}

\begin{definition}[Retrieval-Augmented Generation]
\label{def:rag}
Let $\mathcal{D} = \{d_1,\ldots,d_N\}$ be a corpus of documents (or passages),
$q$ a user query, and $k \in \mathbb{N}$ the number of retrieved passages.
A RAG system operates in three stages:
\begin{enumerate}
  \item \textbf{Retrieval:} compute a relevance score $s(q, d_i)$ for each
        $d_i \in \mathcal{D}$ and return the top-$k$ passages
        $\mathcal{R}(q) = \{d_{(1)},\ldots,d_{(k)}\}$.
  \item \textbf{Augmentation:} construct the augmented prompt
        $\tilde{q} = [d_{(1)},\ldots,d_{(k)},\, q]$.
  \item \textbf{Generation:} produce the answer
        $a \sim P_\theta(\,\cdot \mid \tilde{q})$.
\end{enumerate}
\end{definition}

\subsection{Dense Retrieval and Vector Databases}
\label{sec:rag-dense}

[PROSE: embedding-based retrieval; cosine similarity as relevance score;
FAISS, Pinecone, Chroma, Weaviate; approximate nearest-neighbour search (HNSW, IVF);
chunking strategies for long financial documents (512-token chunks with 50-token overlap)]

\subsection{Sparse Retrieval and Hybrid Methods}
\label{sec:rag-sparse}

[PROSE: BM25 as the classical baseline; TF-IDF retrieval score formula;
hybrid retrieval = linear combination of dense and sparse scores;
reciprocal rank fusion; when sparse beats dense in finance (exact ticker symbols,
CUSIP numbers, specific clause references)]

\subsection{Re-Ranking}
\label{sec:rag-reranking}

[PROSE: cross-encoder re-ranker; retrieve top-100, re-rank to top-5;
why this matters for long 10-K filings; ColBERT late-interaction model]

\subsection{RAG for Financial Documents}
\label{sec:rag-finance}

[PROSE + EXAMPLE: pipeline for answering questions about a 10-K filing;
(1) parse PDF to text, (2) chunk by paragraph/section, (3) embed with SBERT,
(4) store in FAISS, (5) at query time embed question, retrieve top-5 passages,
(6) prompt LLM with passages + question, (7) require model to cite passage numbers;
code listing showing the FAISS index construction and query]

\begin{lstlisting}[language=Python, caption={Minimal RAG pipeline for a 10-K filing.}]
from sentence_transformers import SentenceTransformer
import faiss, numpy as np, anthropic

def build_index(passages: list[str]) -> tuple:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(passages, normalize_embeddings=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings.astype("float32"))
    return index, model

def rag_query(query: str, passages: list[str],
              index, embed_model, k: int = 5) -> str:
    q_emb = embed_model.encode([query], normalize_embeddings=True)
    _, ids = index.search(q_emb.astype("float32"), k)
    context = "\n\n".join(
        f"[{i+1}] {passages[ids[0][i]]}" for i in range(k))
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=512,
        system="Answer using only the provided passages. "
               "Cite passage numbers as [N].",
        messages=[{"role": "user",
                   "content": f"{context}\n\nQuestion: {query}"}])
    return msg.content[0].text
\end{lstlisting}
```

- [ ] **Step 6.2: Fill all `[PROSE...]` placeholders.**

Key equations to include:
- BM25 score: $\text{BM25}(q,d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t,d)(k_1+1)}{f(t,d)+k_1(1-b+b\cdot|d|/\text{avgdl})}$
- Reciprocal rank fusion: $\text{RRF}(d) = \sum_r \frac{1}{k + \text{rank}_r(d)}$

- [ ] **Step 6.3: Compile. Expected: exit 0.**

- [ ] **Step 6.4: Commit**

```
git commit -m "feat(ch02): add retrieval-augmented generation section"
```

---

## Task 7: New Section — Knowledge Distillation and Model Compression

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 7.1: Write and insert after the RAG section**

```latex
% ---------------------------------------------------------------
\section{Knowledge Distillation and Model Compression}
\label{sec:distillation}

Deploying a 70-billion-parameter model in a latency-sensitive trading system
is impractical.  \emph{Knowledge distillation} and its companion techniques ---
parameter-efficient fine-tuning, quantisation, and pruning --- are the tools
that bridge the gap between frontier model quality and production deployment
constraints.

\subsection{Knowledge Distillation}
\label{sec:distillation-kd}

\begin{definition}[Knowledge Distillation]
\label{def:kd}
Let $\mathcal{T}$ be a \emph{teacher} model with parameters $\theta_T$ and
$\mathcal{S}$ a \emph{student} model with parameters $\theta_S$,
where $|\theta_S| \ll |\theta_T|$.  Given a training set
$\{(\mathbf{x}_i, y_i)\}_{i=1}^N$, knowledge distillation minimises
\begin{equation}
  \mathcal{L}_{\mathrm{KD}} = \alpha \mathcal{L}_{\mathrm{CE}}(\mathbf{p}_S, y)
    + (1-\alpha) \tau^2 \mathcal{L}_{\mathrm{KL}}(\mathbf{p}_T^\tau \| \mathbf{p}_S^\tau),
  \label{eq:kd-loss}
\end{equation}
where $\mathbf{p}_T^\tau$ and $\mathbf{p}_S^\tau$ are the teacher and student
softmax distributions at temperature $\tau$, $\alpha \in [0,1]$ balances the
hard-label and soft-label terms, and $\mathcal{L}_\mathrm{KL}$ is the
Kullback--Leibler divergence.
\end{definition}

[PROSE: intuition — soft labels carry more information than hard one-hot labels
(the teacher's near-zero probabilities encode similarity structure);
the $\tau^2$ factor re-scales gradients; finance application — distilling a
large generalist model into a small domain-specific one for real-time use]

\subsection{Parameter-Efficient Fine-Tuning: LoRA}
\label{sec:distillation-lora}

[PROSE: LoRA (Hu et al. 2022); instead of full fine-tuning, inject low-rank
updates; formal definition below; finance application: fine-tuning on earnings
call transcripts without updating all 7B parameters]

\begin{definition}[Low-Rank Adaptation (LoRA)]
\label{def:lora}
For a pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA
parameterises the weight update as
\begin{equation}
  W = W_0 + \Delta W = W_0 + BA,
  \label{eq:lora}
\end{equation}
where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$,
and $r \ll \min(d,k)$ is the \emph{rank}.  During training, $W_0$ is frozen
and only $A$ and $B$ are updated.  The number of trainable parameters reduces
from $dk$ to $r(d+k)$.
\end{definition}

[PROSE: QLoRA — apply LoRA on top of 4-bit quantised weights; memory savings
calculation; rank selection heuristics; typical finance fine-tuning setup]

\subsection{Quantisation}
\label{sec:distillation-quant}

[PROSE: INT8 post-training quantisation; GPTQ (Frantar et al. 2022) layer-wise
quantisation; AWQ (Lin et al. 2023) activation-aware quantisation; latency vs.
accuracy trade-off table for financial NLP tasks; deployment considerations
on commodity hardware vs. cloud inference]

\subsection{Model Pruning}
\label{sec:distillation-pruning}

[PROSE: structured (remove entire attention heads or layers) vs. unstructured
(zero individual weights) pruning; magnitude-based criteria; the lottery ticket
hypothesis; practical relevance — pruning rarely used standalone in LLMs today,
more relevant for edge/on-premises compliance systems]
```

- [ ] **Step 7.2: Fill all `[PROSE...]` placeholders.**

Required references: `hu2022lora`, `hinton2015distilling`, `frantar2022gptq`, `lin2023awq` — add to bibliography.

- [ ] **Step 7.3: Add bibliography entries for new references**

Add to `book/bibliography.bib`:
```bibtex
@article{hinton2015distilling,
  author  = {Hinton, Geoffrey and Vinyals, Oriol and Dean, Jeffrey},
  title   = {Distilling the Knowledge in a Neural Network},
  journal = {arXiv preprint arXiv:1503.02531},
  year    = {2015},
}
@article{hu2022lora,
  author  = {Hu, Edward J. and Shen, Yelong and Wallis, Phillip and
             Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and
             Wang, Lu and Chen, Weizhu},
  title   = {{LoRA}: Low-Rank Adaptation of Large Language Models},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year    = {2022},
}
@article{frantar2022gptq,
  author  = {Frantar, Elias and Ashkboos, Saleh and Hoefler, Torsten and Alistarh, Dan},
  title   = {{GPTQ}: Accurate Post-Training Quantization for Generative Pre-trained Transformers},
  journal = {arXiv preprint arXiv:2210.17323},
  year    = {2022},
}
@article{lin2023awq,
  author  = {Lin, Ji and Tang, Jiaming and Tang, Haotian and Yang, Shang and
             Dang, Xingyu and Han, Song},
  title   = {{AWQ}: Activation-aware Weight Quantization for {LLM} Compression and Acceleration},
  journal = {arXiv preprint arXiv:2306.00978},
  year    = {2023},
}
```

- [ ] **Step 7.4: Compile. Expected: exit 0.**

- [ ] **Step 7.5: Commit**

```
git commit -m "feat(ch02): add knowledge distillation and model compression section"
```

---

## Task 8: Expand Hallucinations Section with SOTA Mitigation

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex` (the moved Section 10.1 which is now in Ch.2)

The existing hallucinations subsection is brief. This task expands it to a full section with detection methods and SOTA mitigation techniques.

- [ ] **Step 8.1: Locate and replace the existing hallucination subsection**

Find the `\subsection{Hallucinations in Financial Contexts}` block in `ch02`. Replace it with:

```latex
\section{Hallucinations: Detection and Mitigation}
\label{sec:hallucinations}

A language model \emph{hallucination} is an output that is fluent, confident,
and wrong.  In general text generation this is a nuisance; in finance it is a
liability.  A model that fabricates a debt-to-equity ratio, invents a regulatory
citation, or confuses two companies with similar names can cause material harm.
This section classifies hallucinations, surveys detection methods, and presents
the state-of-the-art mitigation techniques that practitioners should deploy
before using LLMs in production financial systems.

\subsection{A Taxonomy of Hallucinations}
\label{sec:hallucinations-taxonomy}

[PROSE: intrinsic (contradicts source) vs. extrinsic (unverifiable); factual vs.
numerical vs. entity hallucinations; the particular severity of numerical hallucination
in finance (wrong EPS figure looks just as plausible as a correct one)]

\subsection{Detection}
\label{sec:hallucinations-detection}

[PROSE + methods:]
% SelfCheckGPT (Manakul et al. 2023): sample N responses, measure consistency
% NLI-based detection: use an entailment model to check each claim against source
% LLM-as-judge: use a second model to verify claims
% Verbalized uncertainty: prompt model to express confidence; calibration
% Formal definition of SelfCheckGPT:
%   score(s) = (1/N) sum_{n=1}^N (1 - P(s | sample_n))
%   high score = inconsistent = likely hallucination

\subsection{SOTA Mitigation Techniques}
\label{sec:hallucinations-mitigation}

[Subsections for each technique:]

\subsubsection*{Retrieval-Augmented Generation}
[PROSE: cross-reference Section~\ref{sec:rag}; grounding claims in retrieved passages
is the single most effective mitigation for factual hallucination in finance]

\subsubsection*{Self-Consistency Sampling}
[PROSE: Wang et al. (2022); sample $K$ reasoning chains, take majority vote on final
answer; formally: $\hat{a} = \arg\max_a \sum_{k=1}^K \mathbf{1}[a_k = a]$;
effective for numerical reasoning tasks in financial analysis]

\subsubsection*{Chain-of-Thought and Scratchpad Prompting}
[PROSE: step-by-step reasoning forces intermediate verifiable claims;
particular value for multi-step financial calculations (DCF, ratio analysis)]

\subsubsection*{Claim Decomposition and Verification}
[PROSE: decompose answer into atomic claims; verify each claim against structured data
sources (EDGAR, Bloomberg, Refinitiv); cite FActScore (Min et al. 2023)]

\subsubsection*{Constitutional AI and Critique Loops}
[PROSE: Anthropic Constitutional AI; model critiques its own output against principles;
finance-specific principles: "All numerical figures must be sourced from the provided document"]

\subsubsection*{Confidence Elicitation and Abstention}
[PROSE: prompt the model to refuse or flag uncertainty when below a threshold;
"If you are not certain, say so and cite the passage you would need to answer";
calibration curve; ECE metric]
```

- [ ] **Step 8.2: Fill all `[PROSE...]` placeholders.**

Required references to add to bib: `manakul2023selfcheckgpt`, `wang2022selfconsistency`, `min2023factscore`.

```bibtex
@article{manakul2023selfcheckgpt,
  author  = {Manakul, Potsawee and Liusie, Adian and Gales, Mark J.F.},
  title   = {{SelfCheckGPT}: Zero-Resource Black-Box Hallucination Detection
             for Generative Large Language Models},
  booktitle = {Proceedings of EMNLP},
  year    = {2023},
}
@article{wang2022selfconsistency,
  author  = {Wang, Xuezhi and Wei, Jason and Schuurmans, Dale and Le, Quoc V. and
             Chi, Ed H. and Narang, Sharan and Chowdhery, Aakanksha and Zhou, Denny},
  title   = {Self-Consistency Improves Chain of Thought Reasoning in Language Models},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year    = {2023},
}
@article{min2023factscore,
  author  = {Min, Sewon and Krishna, Kalpesh and Lyu, Xinxi and Lewis, Mike and
             Yih, Wen-tau and Koh, Pang Wei and Iyyer, Mohit and Zettlemoyer, Luke
             and Hajishirzi, Hannaneh},
  title   = {{FActScore}: Fine-grained Atomic Evaluation of Factual Precision
             in Long Form Text Generation},
  booktitle = {Proceedings of EMNLP},
  year    = {2023},
}
```

- [ ] **Step 8.3: Compile. Expected: exit 0.**

- [ ] **Step 8.4: Commit**

```
git commit -m "feat(ch02): expand hallucinations to full section with SOTA mitigation"
```

---

## Task 9: Final Compile, Score, and Push

- [ ] **Step 9.1: Full compile sequence**

```
cd book
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
Expected: exit 0 on all passes. Check page count > 100.

- [ ] **Step 9.2: Verify zero `\paragraph{}` in Chapter 2**

```powershell
Select-String "\\paragraph\{" book/chapters/02-llm-foundations/chapter.tex
```
Expected: no output.

- [ ] **Step 9.3: Run /score-content on Chapter 2**

Invoke scorer agent on `book/chapters/02-llm-foundations/chapter.tex`.
All dimensions must score ≥ 8. If pedagogy < 8, add learning objectives block.

- [ ] **Step 9.4: Update STATUS.md**

```
| 02 | LLM Foundations | Yes | Yes | [scores] | No |
```

- [ ] **Step 9.5: Final commit and push**

```
git add -A
git commit -m "feat(ch02): complete LLM foundations chapter — temperature, structured gen, RAG, distillation, hallucinations"
git push origin master
```

---

## Spec Coverage Self-Review

| Requirement | Task |
|-------------|------|
| Introduction covers up to embeddings example | Task 1 |
| Temperature concept properly added | Task 4 |
| Structured generation + why crucial in finance | Task 5 |
| RAG section | Task 6 |
| Knowledge distillation properly explained | Task 7 |
| Hallucinations with SOTA mitigation (search only modern techniques) | Task 8 |
| Chapter 2 scaffold (notes, slides, exercises, notebooks) | Task 2 |
| Sections 5–11 moved from Ch.1 to Ch.2 | Task 3 |
| Compile and quality gate | Task 9 |
| No `\paragraph{}` labels | All write tasks (enforced by instruction) |

No gaps found. All requirements covered.
