# Editor Feedback — book/chapters/01-intro/chapter.tex

**Review date:** 2026-05-31  
**Reviewer:** Full-review pipeline (scorer + critic + peer-reviewer agents)  
**Status:** READY_TO_RELEASE

---

## Quality Scores

| Dimension    | Score | Pass (≥8)? |
|--------------|------:|:----------:|
| Clarity      |   9   | ✓          |
| Rigor        |   8   | ✓          |
| Completeness |   5   | ✗          |
| Pedagogy     |   9   | ✓          |
| Style        |   8   | ✓          |
| **Overall**  | **7.8** | **FAIL** |

**Threshold:** 8/10 — chapter FAILS because Completeness = 5/10.

---

## Issue Checklist

Track each item as `[ ]` open → `[x]` resolved.

### BLOCKERs (must fix before release)

- [x] **BLOCKER-1** — Learning Objectives 4–8 entirely absent  
  **Location:** The opening Learning Objectives box lists 8 objectives; sections covering LOs 4–8 are missing.  
  **Missing sections:**
  - LO4: LSTM networks and the vanishing gradient problem
  - LO5: Transformer attention mechanism with full `1/√d_k` scaling derivation
  - LO6: Survey of major LLM families (GPT, BERT, T5, LLaMA, Bloomberg-family)
  - LO7: Python API code for at least one LLM provider (OpenAI, Anthropic, or HuggingFace)
  - LO8: LLM limitations and regulatory landscape in finance  
  **Fix:** Invoke **book-writer** agent to draft the five missing sections. Each should include at least one Definition or Theorem environment, one working code listing (where applicable), and a financial application example. Also invoke **exercise-designer** for at least one [B]/[I]/[A] exercise per new section.  
  **Agent:** book-writer + exercise-designer  

- [x] **BLOCKER-2** — Placeholder PCA figure (`fig:embeddings-pca`)  
  **Location:** Section 4.3 ("Case Study: PCA on Financial Vocabulary"), the figure is a TikZ gray rectangle.  
  **Impact:** Prose in §4.3 makes specific empirical claims ("rates cluster is well-separated from equities cluster") that are unverifiable without the actual figure.  
  **Fix:** Replace the TikZ placeholder with a real `minted` Python code listing that generates the PCA scatter plot, wrapping it in a `\begin{figure}` with proper caption and label; or produce a real PGFPlots/TikZ figure with the actual cluster data.  
  **Agent:** figure-designer (or code-writer if a matplotlib code listing is preferred)

---

### MAJORs (fix before release)

- [x] **MAJOR-1** — Broken cross-reference `\ref{sec:intro-classical}`  
  **Location:** Line 1302 in chapter.tex (TF-IDF forward reference).  
  **Problem:** Produces `??` in the compiled PDF. The correct label is `\ref{sec:classical}`.  
  **Fix:** Replace `\ref{sec:intro-classical}` → `\ref{sec:classical}` throughout the file.  
  **Agent:** chapter-surgeon  

- [x] **MAJOR-2** — Wrong citation for Bloomberg Word2Vec (`\cite{liu2018}`)  
  **Location:** Bloomberg Word2Vec paragraph; a LaTeX comment in the source explicitly flags this as the wrong paper.  
  **Problem:** `liu2018` refers to a different paper. The correct citation for Bloomberg's domain-adapted word embeddings should reference the Bloomberg NLP work (Tsai et al. or the specific Bloomberg Word2Vec paper).  
  **Fix:** Find or create the correct bibliography entry and replace `\cite{liu2018}` with the correct key.  
  **Agent:** fact-checker (to identify correct citation), then chapter-surgeon (to apply the fix)  

- [x] **MAJOR-3** — No Python API code for any LLM provider (LO7 unmet)  
  **Location:** Missing — no section on API usage exists.  
  **Fix:** Covered by BLOCKER-1 resolution (LO7 section). Ensure the new section includes at minimum: a working code listing for either `openai`, `anthropic`, or `transformers` that makes a completion call and parses the response.  
  **Agent:** book-writer + code-writer  

- [x] **MAJOR-4** — No LLM limitations or regulatory landscape section (LO8 unmet)  
  **Location:** Missing — no section on hallucinations, context limits, bias, or EU AI Act / SEC guidance exists.  
  **Fix:** Covered by BLOCKER-1 resolution (LO8 section). Should cover: hallucination taxonomy, context window limitations, model bias, regulatory touch-points (EU AI Act Article 52, SEC 2023 AI guidance).  
  **Agent:** book-writer  

---

### MINORs (fix if time allows, required before final release)

- [x] **MINOR-1** — Notation inconsistency in one-hot vectors  
  **Location:** Section 3.2 (One-Hot Encoding).  
  **Problem:** One-hot vectors denoted inconsistently (sometimes bold `\mathbf{e}_i`, sometimes plain `e_i`).  
  **Fix:** Standardise to `\mathbf{e}_i \in \{0,1\}^{|V|}` throughout.  
  **Agent:** chapter-surgeon  

- [x] **MINOR-2** — Unexplained norm equality in cosine similarity derivation  
  **Location:** Section 4.2 (cosine similarity), equation block.  
  **Problem:** The step `\|\mathbf{a}\| \cdot \|\mathbf{b}\| = 1` is assumed without stating that vectors are normalised.  
  **Fix:** Add a one-sentence remark: "Assuming unit-normalised embeddings, $\|\mathbf{v}\|=1$ for all $\mathbf{v}$, the denominator equals 1."  
  **Agent:** math-checker → chapter-surgeon  

- [x] **MINOR-3** — Thin "Looking Ahead" section (Section 1.5)  
  **Location:** Final section of the chapter.  
  **Problem:** The section is one short paragraph with no explicit pointers to later chapters.  
  **Fix:** Expand to 3–4 sentences naming the specific chapter and section where each topic introduced here (BoW, embeddings, attention) reappears, e.g., "The attention mechanism previewed here is developed formally in §2.3."  
  **Agent:** editor  

- [x] **MINOR-4** — Ambiguous FinBERT citations  
  **Location:** FinBERT discussion.  
  **Problem:** The text cites both Araci (2019) and Yang et al. (2020) for "FinBERT" without clarifying these are two distinct models with the same name.  
  **Fix:** Add a parenthetical: "(Note: two models share the name FinBERT — Araci (2019) fine-tuned BERT on financial text; Yang et al. (2020) retrained BERT from scratch on financial corpora. This chapter refers to \cite{yang2020finbert}.) "  
  **Agent:** chapter-surgeon  

---

## Peer Review Verdict

**MAJOR_REVISION** — the chapter's existing content (history, textual signal framework, BoW/TF-IDF, word embeddings) is high quality and merits inclusion, but the chapter cannot function as a complete introduction to LLMs in finance until the five missing learning objectives are written and the two BLOCKERs are resolved.

---

## Priority Resolution Order

1. BLOCKER-1 (missing LOs 4–8) — largest single gap; subsumes MAJOR-3 and MAJOR-4
2. BLOCKER-2 (PCA figure placeholder)
3. MAJOR-1 (broken `\ref`)
4. MAJOR-2 (wrong Word2Vec citation)
5. MINOR-1 through MINOR-4 (polish pass)

---

## Re-review Trigger

After all BLOCKERs and MAJORs are resolved, run `/full-review book/chapters/01-intro/chapter.tex` to get an updated verdict. The target exit condition is:
- Quality score ≥ 8.0 on **all five dimensions**
- 0 BLOCKERs
- Peer verdict: ACCEPT or MINOR_REVISION
- Recommendation: READY_TO_RELEASE
