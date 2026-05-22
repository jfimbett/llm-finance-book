# Dual-Mode Section Environments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two `tcolorbox` environments (`deepdive` / `context`) to the book's preamble and apply them across Chapters 1 and 2, rewriting `context` section openings as engaging narrative.

**Architecture:** A `deepdive` box (light blue) wraps mathematical derivations and formal definitions. A `context` box (warm ivory) wraps narrative, historical, and practical sections — with rewritten opening paragraphs using a concrete hook, present tense, and zero hedge language. Section headings stay in the main flow; only content between headings is boxed. Chapter Summary section (Ch2) is left unboxed.

**Tech Stack:** LaTeX, `tcolorbox` (skins + breakable), existing `mathpazo`/`Palatino` type­face, `pdflatex` + `biber` build chain.

---

## Task 1: Add tcolorbox environments to preamble

**Files:**
- Modify: `book/preamble.tex` (after the `% --- Colors ---` block, around line 73)

- [ ] **Step 1: Add three new color definitions**

In `book/preamble.tex`, after the existing `\definecolor{stringgreen}` line (line 80), add:

```latex
\definecolor{deepdivebg}{RGB}{235, 244, 255}
\definecolor{narrativebg}{RGB}{255, 252, 240}
\definecolor{narrativerule}{RGB}{180, 130, 40}
```

- [ ] **Step 2: Add tcolorbox package and define both environments**

In `book/preamble.tex`, after the `% --- Miscellaneous ---` block (after the `\setlist` lines, around line 188), add:

```latex
% --- Dual-mode section environments ---
\usepackage[skins, breakable]{tcolorbox}

\newtcolorbox{deepdive}{%
  enhanced, breakable,
  colback  = deepdivebg,
  colframe = linkblue,
  boxrule  = 0pt,
  toprule  = 1.5pt,
  bottomrule = 0.5pt,
  leftrule = 0pt,
  rightrule = 0pt,
  arc      = 0pt,
  before upper = {%
    \noindent\hfill
    {\footnotesize\scshape\color{linkblue}under the hood}%
    \par\smallskip\noindent},
  left = 10pt, right = 10pt, top = 6pt, bottom = 8pt,
}

\newtcolorbox{context}{%
  enhanced, breakable,
  colback  = narrativebg,
  colframe = narrativerule,
  boxrule  = 0pt,
  toprule  = 1.5pt,
  bottomrule = 0.5pt,
  leftrule = 0pt,
  rightrule = 0pt,
  arc      = 0pt,
  before upper = {%
    \setlength{\parskip}{5pt}%
    \noindent\hfill
    {\footnotesize\scshape\color{narrativerule}the bigger picture}%
    \par\smallskip\noindent},
  left = 10pt, right = 10pt, top = 6pt, bottom = 8pt,
}
```

- [ ] **Step 3: Compile once to verify no errors**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

Expected: exits without `!` errors (warnings are fine). If `tcolorbox` is missing from your TeX distribution, install it: `tlmgr install tcolorbox`.

- [ ] **Step 4: Commit**

```
git add book/preamble.tex
git commit -m "feat(config): add deepdive and context tcolorbox environments to preamble"
```

---

## Task 2: Wrap Chapter 1 — context sections (History + Why Text Matters)

**Files:**
- Modify: `book/chapters/01-intro/chapter.tex`

The wrapping rule throughout: the `\section{}` + `\label{}` lines stay in the main flow; `\begin{context}` goes on the blank line immediately after the label, and `\end{context}` goes on the blank line immediately before the next `\section{}` command.

- [ ] **Step 1: Wrap section 1.1 (A Brief History) in `context`**

After `\label{sec:history}` (line 28), add `\begin{context}`.

Before `\section{Why Text Matters in Finance}` (line 214), add `\end{context}`.

- [ ] **Step 2: Replace the opening paragraph of section 1.1**

Find and replace the existing paragraph that begins `Language is the medium through which` (lines 30–38) with:

```latex
It is the autumn of 2006 and Paul Tetlock, then a doctoral student, is staring
at a spreadsheet.  On one side: a column of numbers representing the daily
fraction of negative words in the \emph{Wall Street Journal}'s \emph{Abreast of
the Market} column, running back to 1984.  On the other: the next-day return on
the Dow Jones Industrial Average.  The correlation is small.  But it is
there---and according to the textbooks that line his shelves, it should not be.
If markets are efficient, prices should already reflect the sentiment of the
country's most widely-read financial column.  Tetlock would publish this finding
in the \emph{Journal of Finance} \cite{tetlock2007giving}, and the paper would
become a founding document of a new field.  But the deeper story began forty
years earlier, in a social science department with no interest in stock prices
whatsoever.
```

- [ ] **Step 3: Wrap section 1.2 (Why Text Matters) in `context`**

After `\label{sec:motivation}` (line 215), add `\begin{context}`.

Before `\section{Classical Text Representations}` (line 446), add `\end{context}`.

- [ ] **Step 4: Replace the opening paragraph of section 1.2**

Find and replace the existing paragraph that begins `Financial economics is built on the notion` (lines 217–222) with:

```latex
Every quarter, thousands of companies assemble their executives on a conference
call, dial in a few hundred sell-side analysts, and spend an hour narrating the
past three months.  The ritual is called the earnings call.  The transcript is
published within days and largely forgotten---except by the people who have
learned to listen to what is not in the numbers.  The word \emph{challenges}
appearing where \emph{headwinds} used to appear.  The CFO's sentences getting
shorter.  The count of hedge words---\emph{approximately}, \emph{roughly},
\emph{we believe}---ticking upward.  None of this information lives in the
earnings per share figure.  All of it lives in the transcript.  This section
asks why that matters, and how we know it does.
```

- [ ] **Step 5: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

Expected: clean compile; the two context boxes appear with warm ivory background and amber top rule.

- [ ] **Step 6: Commit**

```
git add book/chapters/01-intro/chapter.tex
git commit -m "feat(ch01): wrap History and Why Text Matters sections in context boxes, rewrite openings"
```

---

## Task 3: Wrap Chapter 1 — deepdive sections + Looking Ahead

**Files:**
- Modify: `book/chapters/01-intro/chapter.tex`

- [ ] **Step 1: Wrap section 1.3 (Classical Text Representations) in `deepdive`**

After `\label{sec:classical}` (line 447), add `\begin{deepdive}`.

Before `\section{Word Embeddings}` (line 815), add `\end{deepdive}`.

- [ ] **Step 2: Wrap section 1.4 (Word Embeddings) in `deepdive`**

After `\label{sec:embeddings}` (line 816), add `\begin{deepdive}`.

Before `\section{Looking Ahead}` (line 1259), add `\end{deepdive}`.

- [ ] **Step 3: Wrap section 1.5 (Looking Ahead) in `context`**

After `\label{sec:intro-looking-ahead}` (line 1260), add `\begin{context}`.

At the very end of the file (after the last line of section 1.5 content), add `\end{context}`.

- [ ] **Step 4: Replace the opening paragraph of Looking Ahead**

Find and replace the paragraph beginning `The representations developed in this chapter treat language` (line 1262) with:

```latex
We have come a long way from Tetlock's spreadsheet.  A word, it turns out, is
not just a symbol: it is a point in a geometric space whose neighbourhood
encodes meaning.  A document is not just a bag of tokens; it is a trajectory
through that space.  But the representations built in this chapter still miss
something fundamental.  They treat language as a static inventory of symbols
rather than a sequence of choices.  \emph{Equity} and \emph{stock} remain
synonyms only by the accident of co-occurrence statistics; they are not linked
by any model of grammar or syntax.  The sentence \emph{earnings did not
disappoint} scores the same sentiment as \emph{earnings disappointed} in any
dictionary model, because the word \emph{not} earns no category in the Harvard
IV-4 list.  The next chapter is about what happens when we take order
seriously---and what becomes possible once we do.
```

- [ ] **Step 5: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

Expected: clean compile; Chapter 1 now shows blue deepdive boxes for sections 1.3–1.4 and ivory context boxes for 1.1–1.2 and 1.5.

- [ ] **Step 6: Commit**

```
git add book/chapters/01-intro/chapter.tex
git commit -m "feat(ch01): wrap Classical Representations, Word Embeddings in deepdive; Looking Ahead in context"
```

---

## Task 4: Wrap Chapter 2 — deepdive sections group 1 (Doc Repr + Sequential + Transformer)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

Section 2.1 starts immediately after the learning-objectives remark (line 21 ends the remark). The wrapping rule is the same: label stays outside, content wraps.

- [ ] **Step 1: Wrap section 2.1 (Document-Level Representations) in `deepdive`**

After `\label{sec:doc-repr}` (line 25), add `\begin{deepdive}`.

Before `\section{Sequential Models: From RNNs to Attention}` (line 318), add `\end{deepdive}`.

- [ ] **Step 2: Wrap section 2.2 (Sequential Models) in `deepdive`**

After `\label{sec:sequential}` (line 319), add `\begin{deepdive}`.

Before `\section{The Transformer Architecture}` (line 582), add `\end{deepdive}`.

- [ ] **Step 3: Wrap section 2.3 (The Transformer Architecture) in `deepdive`**

After `\label{sec:transformer}` (line 583), add `\begin{deepdive}`.

Before `\section{The Modern LLM Landscape}` (line 933), add `\end{deepdive}`.

- [ ] **Step 4: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

Expected: clean compile; sections 2.1–2.3 appear in light blue deepdive boxes.

- [ ] **Step 5: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): wrap Doc Representations, Sequential Models, Transformer in deepdive boxes"
```

---

## Task 5: Wrap Chapter 2 — context section (Modern LLM Landscape)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 1: Wrap section 2.4 (The Modern LLM Landscape) in `context`**

After `\label{sec:landscape}` (line 934), add `\begin{context}`.

Before `\section{Temperature, Sampling, and Controlled Generation}` (line 1192), add `\end{context}`.

- [ ] **Step 2: Replace the opening paragraph of section 2.4**

Find and replace the paragraph beginning `The preceding sections established the architectural foundations` (lines 936–939) with:

```latex
In November 2022, a chatbot launched with almost no fanfare.  Within sixty days
it had a hundred million users---the fastest consumer adoption of any product in
history.  ChatGPT did not introduce any fundamentally new technology; the
Transformer architecture had existed since 2017, GPT-3 since 2020.  What it
introduced was \emph{interface}: a fluent, patient, conversational layer over a
raw language model that made the underlying capability legible to people who had
never written a line of code.  For finance, the question was not whether this was
impressive.  The question was more specific and more urgent: what, exactly, can
these models do, and what will they get confidently, catastrophically wrong?  The
answer begins with understanding what is actually being deployed.
```

- [ ] **Step 3: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 4: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): wrap Modern LLM Landscape in context box, rewrite opening"
```

---

## Task 6: Wrap Chapter 2 — mixed section (Temperature/Sampling)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

Section 2.5 is split: the intro paragraph and subsections 2.5.1–2.5.3 (Temperature, Top-k/Nucleus, Beam Search) are `deepdive`; subsection 2.5.4 (Sampling Strategy Selection) is `context`.

- [ ] **Step 1: Wrap section 2.5 intro + subsections 2.5.1–2.5.3 in `deepdive`**

After `\label{sec:sampling}` (line 1193), add `\begin{deepdive}`.

Before `\subsection{Sampling Strategy Selection for Financial Tasks}` (line 1319), add `\end{deepdive}`.

- [ ] **Step 2: Wrap subsection 2.5.4 in `context`**

After `\label{sec:sampling-finance}` (line 1320), add `\begin{context}`.

Before `\section{Structured Generation}` (line 1368), add `\end{context}`.

- [ ] **Step 3: Replace the opening of subsection 2.5.4**

Find and replace the paragraph beginning `The choice of decoding strategy should be driven by the nature` (lines 1322–1324) with:

```latex
A risk analyst asks an LLM to summarise a credit agreement.  She runs the same
prompt twice and gets two different answers.  Not wrong answers---two reasonable
answers, each emphasising different clauses.  This is not a bug; it is a feature
she did not ask for.  Temperature is the dial that governs how much the model
wanders from its most probable completion.  Set it too high and the model
fabricates; set it too low and it becomes a repetition engine, parroting training
data verbatim.  The right setting is not a universal constant: it depends on what
you need the model to do, and on the consequences if it gets it wrong.
Table~\ref{tab:sampling-strategies} translates this principle into concrete
recommendations for five common financial NLP tasks.
```

- [ ] **Step 4: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 5: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): split Temperature section into deepdive (math) and context (strategy), rewrite opening"
```

---

## Task 7: Wrap Chapter 2 — context sections (Structured Generation + API)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 1: Wrap section 2.6 (Structured Generation) in `context`**

After `\label{sec:structured-gen}` (line 1369), add `\begin{context}`.

Before `\section{Working with LLMs via API}` (line 1507), add `\end{context}`.

- [ ] **Step 2: Replace the opening paragraph of section 2.6**

Find and replace the paragraph beginning `Financial applications rarely need free prose` (lines 1371–1377) with:

```latex
A bank's model risk team has a problem.  Their junior analysts are using an LLM
to extract covenants from loan agreements, and the model keeps producing prose---
long, fluent, accurate-sounding prose---when what the downstream system needs is
a JSON object with three fields.  The analysts copy-paste.  The pipeline breaks.
Escalation follows.  The answer is not a better prompt.  The answer is
\emph{constrained decoding}: making it structurally impossible for the model to
output anything that does not conform to a predefined schema.  Financial
applications rarely need the model to be creative.  They need it to be
\emph{precise}.
```

- [ ] **Step 3: Wrap section 2.7 (Working with LLMs via API) in `context`**

After `\label{sec:api}` (line 1508), add `\begin{context}`.

Before `\section{Retrieval-Augmented Generation}` (line 1803), add `\end{context}`.

- [ ] **Step 4: Replace the opening paragraph of section 2.7**

Find and replace the paragraph beginning `The transition from understanding how LLMs work to using them in practice` (lines 1510–1513) with:

```latex
Every LLM workflow that matters in production goes through an API.  The model you
choose, the temperature you set, the number of tokens you send---these are not
academic parameters.  They are engineering decisions with real cost, latency, and
risk consequences.  A 10,000-token prompt sent to a frontier model costs roughly
twenty cents.  Run that prompt a thousand times a day and you have spent
\$73,000 in a year on a single workflow.  This section covers the concepts and
Python code you need to build that workflow correctly from the start.
```

- [ ] **Step 5: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 6: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): wrap Structured Generation and API sections in context, rewrite openings"
```

---

## Task 8: Wrap Chapter 2 — context sections (RAG + Hallucinations + Limitations)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 1: Wrap section 2.8 (RAG) in `context`**

After `\label{sec:rag}` (line 1804), add `\begin{context}`.

Before `\section{Knowledge Distillation and Model Compression}` (line 1965), add `\end{context}`.

- [ ] **Step 2: Replace the opening paragraph of section 2.8**

Find and replace the paragraph beginning `Large language models are trained on a fixed corpus` (lines 1806–1812) with:

```latex
An asset manager wants an LLM that can answer questions about their portfolio
companies' recent filings.  They try prompting a frontier model directly.  The
model knows Apple and Microsoft---their 10-Ks are woven into its training
data---but their portfolio includes thirty mid-cap industrials the model has
never encountered.  Every answer about those companies is a confident
hallucination, decorated with plausible-looking numbers.  The solution is not a
bigger model or a better prompt.  The solution is \emph{retrieval-augmented
generation}: instead of asking the model what it remembers, you hand it the
document and ask it to read.
```

- [ ] **Step 3: Wrap section 2.10 (Hallucinations) in `context`**

After `\label{sec:hallucinations}` (line 2097), add `\begin{context}`.

Before `\section{Limitations and Responsible Use}` (line 2250), add `\end{context}`.

- [ ] **Step 4: Replace the opening paragraph of section 2.10**

Find and replace the paragraph beginning `A language model \emph{hallucination} is an output that is fluent, confident, and wrong` (lines 2099–2105) with:

```latex
In 2023, a New York attorney submitted a legal brief citing six case precedents
that did not exist.  ChatGPT had generated them, complete with plausible docket
numbers and verbatim quotations.  The attorney was sanctioned and the incident
made international headlines.  But the more instructive story is quieter: the
hundreds of financial analysts who asked LLMs about earnings figures, covenant
terms, and regulatory thresholds, received confident wrong answers, and did not
catch them.  A language model \emph{hallucination} is an output that is fluent,
confident, and wrong.  In general text generation this is a nuisance.  In finance
it is a liability.  This section classifies hallucinations by origin, surveys
modern detection methods, and presents the mitigation techniques that should be
deployed before any LLM touches a production financial system.
```

- [ ] **Step 5: Wrap section 2.11 (Limitations and Responsible Use) in `context`**

After `\label{sec:limitations}` (line 2251), add `\begin{context}`.

Before `\section{Chapter Summary}` (line 2330), add `\end{context}`.

- [ ] **Step 6: Replace the opening paragraph of section 2.11**

Find and replace the paragraph beginning `The preceding sections present LLMs as powerful tools` (lines 2253–2255) with:

```latex
In 2024, the EU's AI Act came into force, classifying certain AI applications in
finance---credit scoring, insurance pricing, certain forms of algorithmic
trading---as high-risk.  The regulation does not ban these applications.  It
requires documentation, explainability, human oversight, and ongoing monitoring.
These requirements are not obstacles to using LLMs in finance; they are the
engineering specification.  An LLM deployed without explainability
infrastructure is not a regulatory problem waiting to happen.  It is a model
risk problem that has already happened, quietly, on every inference.  This
section provides the vocabulary and framework for thinking about those risks
rigorously.
```

- [ ] **Step 7: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 8: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): wrap RAG, Hallucinations, Limitations in context boxes, rewrite openings"
```

---

## Task 9: Wrap Chapter 2 — deepdive section (Knowledge Distillation)

**Files:**
- Modify: `book/chapters/02-llm-foundations/chapter.tex`

- [ ] **Step 1: Wrap section 2.9 (Knowledge Distillation and Model Compression) in `deepdive`**

After `\label{sec:distillation}` (line 1966), add `\begin{deepdive}`.

Before `\section{Hallucinations: Detection and Mitigation}` (line 2096), add `\end{deepdive}`.

- [ ] **Step 2: Compile and verify**

```
cd book && pdflatex -interaction=nonstopmode main.tex
```

Expected: clean compile; distillation section appears in a blue deepdive box.

- [ ] **Step 3: Commit**

```
git add book/chapters/02-llm-foundations/chapter.tex
git commit -m "feat(ch02): wrap Knowledge Distillation section in deepdive box"
```

---

## Task 10: Full build, visual spot-check, and final commit

**Files:** No changes — verification only.

- [ ] **Step 1: Run full build**

```
cd book && pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
```

Expected: exits with no `!` errors and produces `main.pdf`.

- [ ] **Step 2: Spot-check the PDF**

Open `book/main.pdf` and verify:
- Chapter 1 has alternating ivory (context) and blue (deepdive) boxes
- Chapter 2 shows blue boxes for sections 2.1–2.3, ivory for 2.4, blue for 2.5 math, ivory for 2.5.4, ivory for 2.6–2.8, blue for 2.9, ivory for 2.10–2.11, unboxed for Chapter Summary
- All `\begin{theorem}`, `\begin{definition}`, `\begin{proposition}` environments render correctly inside deepdive boxes
- Page breaks inside boxes are handled cleanly (no orphaned box edges)
- The "under the hood" and "the bigger picture" labels appear right-aligned at the top of each box

- [ ] **Step 3: Commit final state**

```
git add -u
git commit -m "feat(ch01,ch02): complete dual-mode section environments — deepdive and context boxes applied"
```

---

## Spec Coverage Check

| Spec requirement | Task |
|---|---|
| `deepdive` tcolorbox: light blue bg, steel-blue rule, "Under the Hood" label | Task 1 |
| `context` tcolorbox: ivory bg, amber rule, "The Bigger Picture" label | Task 1 |
| Ch1 History sections → `context` | Task 2 |
| Ch1 Why Text Matters → `context` | Task 2 |
| Ch1 Classical Text Representations → `deepdive` | Task 3 |
| Ch1 Word Embeddings → `deepdive` | Task 3 |
| Ch1 Looking Ahead → `context` | Task 3 |
| Ch2 Doc Repr + Sequential + Transformer → `deepdive` | Task 4 |
| Ch2 Modern LLM Landscape → `context` | Task 5 |
| Ch2 Temperature math subsections → `deepdive` | Task 6 |
| Ch2 Sampling Strategy Selection → `context` | Task 6 |
| Ch2 Structured Generation → `context` | Task 7 |
| Ch2 Working with LLMs via API → `context` | Task 7 |
| Ch2 RAG → `context` | Task 8 |
| Ch2 Hallucinations → `context` | Task 8 |
| Ch2 Limitations and Responsible Use → `context` | Task 8 |
| Ch2 Knowledge Distillation → `deepdive` | Task 9 |
| Narrative style guide applied to all `context` openings | Tasks 2, 3, 5, 6, 7, 8 |
| Final full build verification | Task 10 |
