# Design Spec: Dual-Mode Section Environments
**Date:** 2026-05-22
**Scope:** Chapters 1 and 2 (extensible to all future chapters)

---

## Goal

Create a clear visual and tonal distinction between two kinds of content in the book:

1. **Technical deep-dives** — formal definitions, propositions, proofs, mathematical derivations. For readers who want full rigour.
2. **Narrative/context sections** — engaging stories, real-world financial scenarios, conceptual motivation. Written to hook and retain a practitioner who may not follow every equation.

The distinction is realised through two `tcolorbox` LaTeX environments plus rewritten prose in the narrative environment. Labels deliberately avoid the words "mathematics" or "practitioner".

---

## LaTeX Environment Design

### `deepdive` environment
- **Background:** `#EBF4FF` (RGB 235, 244, 255) — very light steel blue
- **Top/bottom rule:** 1.5pt, `linkblue` = RGB(14, 75, 140)
- **Label:** "Under the Hood" — small caps, right-aligned in the top rule strip
- **Font:** standard body font (Palatino); no change — proofs and math require clean upright Roman
- **Use for:** Definitions, Propositions, Theorems, derivations, algorithm descriptions, formal proofs

### `context` environment
- **Background:** `#FFFCF0` (RGB 255, 252, 240) — warm ivory/cream
- **Top/bottom rule:** 1.5pt, amber = RGB(180, 130, 40)
- **Label:** "The Bigger Picture" — small caps, right-aligned in the top rule strip
- **Font:** standard body font with `\setlength{\parskip}{5pt}` inside the box — slightly more generous spacing to signal a different reading pace
- **Use for:** historical narrative, real-world financial scenarios, conceptual motivation, regulatory/ethical discussion, practical API walkthroughs

### New colors to add to preamble
```latex
\definecolor{deepdivebg}{RGB}{235, 244, 255}
\definecolor{narrativebg}{RGB}{255, 252, 240}
\definecolor{narrativerule}{RGB}{180, 130, 40}
```

### tcolorbox implementation sketch
```latex
\tcbuselibrary{skins, breakable}

\newtcolorbox{deepdive}{
  enhanced, breakable,
  colback=deepdivebg,
  colframe=linkblue,
  boxrule=0pt,
  toprule=1.5pt,
  bottomrule=1.5pt,
  leftrule=0pt,
  rightrule=0pt,
  arc=0pt,
  before upper={\hfill\textsc{\footnotesize under the hood}\par\smallskip},
  left=8pt, right=8pt, top=6pt, bottom=6pt,
}

\newtcolorbox{context}{
  enhanced, breakable,
  colback=narrativebg,
  colframe=narrativerule,
  boxrule=0pt,
  toprule=1.5pt,
  bottomrule=1.5pt,
  leftrule=0pt,
  rightrule=0pt,
  arc=0pt,
  before upper={\setlength{\parskip}{5pt}\hfill\textsc{\footnotesize the bigger picture}\par\smallskip},
  left=8pt, right=8pt, top=6pt, bottom=6pt,
}
```

---

## Section Mapping — Chapter 1

| Section / Subsection | Environment |
|---|---|
| 1.1 A Brief History of Textual Analysis | `context` |
| 1.1.1 Early Approaches: Keyword Counting and Dictionary Methods | `context` |
| 1.1.2 The Shift to Statistical and Neural Methods | `context` |
| 1.2 Why Text Matters in Finance | `context` |
| 1.2.1 The Information Content of Earnings Calls, News, and Filings | `context` |
| 1.2.2 Text as a Signal: Evidence from the Literature | `context` |
| 1.3 Classical Text Representations | `deepdive` |
| 1.3.1 Vocabulary, Tokens, and the Bag-of-Words Model | `deepdive` |
| 1.3.2 One-Hot Encoding | `deepdive` |
| 1.3.3 TF-IDF Weighting | `deepdive` |
| 1.4 Word Embeddings | `deepdive` |
| 1.4.1 Distributional Semantics and the Embedding Idea | `deepdive` |
| 1.4.2 Word2Vec and GloVe | `deepdive` |
| 1.4.3 Case Study: PCA on Financial Vocabulary | `deepdive` |

---

## Section Mapping — Chapter 2

| Section / Subsection | Environment |
|---|---|
| 2.1 Document-Level Representations | `deepdive` |
| 2.2 Sequential Models (RNNs, LSTMs, GRUs, Attention) | `deepdive` |
| 2.3 The Transformer Architecture | `deepdive` |
| 2.4 The Modern LLM Landscape | `context` |
| 2.5 Temperature, Sampling (math subsections) | `deepdive` |
| 2.5.4 Sampling Strategy Selection for Financial Tasks | `context` |
| 2.6 Structured Generation + Why It Matters in Finance | `context` |
| 2.7 Working with LLMs via API | `context` |
| 2.8 Retrieval-Augmented Generation | `context` |
| 2.9 Knowledge Distillation, LoRA, Quantisation, Pruning | `deepdive` |
| 2.10 Hallucinations: Detection and Mitigation | `context` |
| 2.11 Limitations and Responsible Use | `context` |

---

## Prose Rewriting — Narrative Style Guide for `context` Boxes

All sections wrapped in `context` must be rewritten to meet this standard:

- **Tense:** Present tense preferred ("A portfolio manager opens the earnings call transcript…"), past only for documented historical events.
- **Concreteness:** Name real events, real companies, real market episodes where possible. Avoid generic "a firm" — say "Goldman Sachs" or "a mid-cap industrial."
- **Hook:** Each `context` block opens with a scene or question that creates stakes. Not "This section discusses…" but a moment or a problem.
- **No hedge language:** Replace "it could be argued that" / "one might consider" / "it is worth noting" with direct assertions.
- **Rhythm:** Vary sentence length. Short sentences for emphasis. Longer ones for context and nuance.
- **Register:** Think Michael Lewis meets a well-written Economist briefing — not a survey paper, not a pop-science book.
- **Rigor stays:** The narrative is not a simplification. It is the full argument told through the texture of real events. Equations and definitions live in `deepdive`; the *meaning* of those equations lives in `context`.

---

## Implementation Steps

1. Add three new color definitions to `book/preamble.tex`
2. Add `\usepackage{tcolorbox}` with `skins` and `breakable` libraries to `book/preamble.tex`
3. Define `deepdive` and `context` environments in `book/preamble.tex`
4. Wrap `context` sections in Chapter 1 with `\begin{context}...\end{context}` and rewrite prose to narrative style
5. Wrap `deepdive` sections in Chapter 1 with `\begin{deepdive}...\end{deepdive}`
6. Repeat for Chapter 2
7. Compile `book/main.tex` and verify PDF renders correctly

---

## Success Criteria

- PDF compiles without errors
- `context` boxes visually distinct from `deepdive` boxes and from body text
- All `context` prose passes narrative style guide (hook, concrete, no hedge language)
- All math/theorem environments render correctly inside `deepdive` boxes
- No content is removed — only visual wrapping and prose rewriting
