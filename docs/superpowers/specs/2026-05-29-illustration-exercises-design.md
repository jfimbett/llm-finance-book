# Illustration Exercises Design

**Date:** 2026-05-29
**Project:** Large Language Models in Finance (book-course-template)
**Scope:** Chapters 01–07 (appendixes excluded)

---

## Goal

Add one flagship illustration exercise per chapter — a real-data plot embedded in the book PDF and the Python code that produced it living in the companion `exercises.ipynb` notebook. Students can reproduce and extend each figure.

---

## Approach

**Notebook-first (Approach B):** Figure generation code lives entirely in `exercises.ipynb`. A dedicated "Illustration Exercise" section downloads data, generates the plot, and saves a PDF to `book/chapters/NN-name/figures/fig_illustration.pdf`. The chapter `.tex` file embeds the PDF via `\includegraphics` and includes an exercise block pointing back to the notebook.

---

## Per-Chapter Illustration Plan

| Ch | Title | Illustration | Data Source |
|----|-------|-------------|-------------|
| 01 | Introduction | TF-IDF term-importance heatmap across AAPL/MSFT/JPM news headlines | `yfinance` news headlines |
| 02 | LLM Foundations | Transformer positional encoding heatmap (sinusoidal patterns across positions × dimensions) | Pure numpy (Vaswani et al. formula) |
| 03 | Training & Fine-tuning | Chinchilla scaling law — compute-optimal training tokens vs. parameter count with real model datapoints overlaid | Hardcoded from Hoffmann et al. 2022 + public model cards |
| 04 | LLM Agents | Cosine similarity matrix between a user query and SEC 10-K filing chunks (RAG retrieval illustration) | `requests` → SEC EDGAR full-text search API |
| 05 | Business Valuation | DCF sensitivity heatmap: enterprise value as a function of WACC × terminal growth rate using AAPL real FCF | `yfinance` financials (AAPL) |
| 06 | Credit Risk | ROC curve with AUROC + KS statistic highlighted for a logistic credit model | `requests` → UCI German Credit dataset |
| 07 | Applications & Future | Grouped bar chart of LLM accuracy on financial NLP benchmarks (FinQA, FPB, FiQA) across model families | Hardcoded from published papers |

---

## Notebook Structure

Each `exercises.ipynb` receives a new **"Illustration Exercise"** section prepended (existing exercise stubs remain unchanged):

```
# Illustration Exercise — [Chapter Title]

## Context        ← markdown: what the plot shows and why it matters
## Data           ← code cells: fetch real data from public APIs
## Figure         ← code cells: process data, generate plot, save PDF
## Your Turn      ← markdown: one open-ended extension prompt
```

Figure save pattern (end of Figure section):
```python
fig.savefig("../../book/chapters/NN-name/figures/fig_illustration.pdf",
            bbox_inches="tight", dpi=150)
```

Shared style preamble in every notebook:
```python
import scienceplots
plt.style.use(["science", "no-latex"])
```

---

## LaTeX Integration

Each `chapter.tex` receives two additions at the end of the most relevant section:

**Figure environment:**
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{figures/fig_illustration}
  \caption{[Descriptive caption.]}
  \label{fig:chNN-illustration}
\end{figure}
```

**Exercise block** (immediately after the figure):
```latex
\begin{exercise}[Illustration]
[Problem statement referencing Figure~\ref{fig:chNN-illustration}.]
See \texttt{code/notebooks/NN-name/exercises.ipynb}, Illustration Exercise.
\end{exercise}
```

The `figures/` directory already exists in each chapter folder.

---

## Dependencies

New packages (to be added to project requirements):
```
scienceplots
yfinance
requests
scikit-learn
pandas
numpy
matplotlib
jupyter
nbconvert
```

---

## Execution

Run all notebooks with:
```bash
jupyter nbconvert --to notebook --execute --inplace \
  code/notebooks/NN-name/exercises.ipynb
```

A master script `code/run_illustrations.sh` runs all 7 in sequence.

**Internet required at run time:** Ch01 (yfinance), Ch04 (SEC EDGAR), Ch05 (yfinance), Ch06 (UCI). Ch02, Ch03, Ch07 run fully offline.

---

## Out of Scope

- Appendixes
- Interactive/Plotly figures
- More than one illustration per chapter
- Synthetic/simulated data (all data is from free public sources)
