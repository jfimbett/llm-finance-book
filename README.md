# Book-Course Template

An AI-assisted template for creating a structured course, companion LaTeX book, and runnable code.

## Quick Start

1. Clone this repository
2. Open it in Claude Code (or any AI assistant)
3. Run `/interview-me` — this configures the entire project in one interactive session
4. Run `/new-topic` — scaffold your first chapter
5. Run `/draft-chapter` — start writing

## Structure

```
book/          LaTeX book (deeper treatment)
course/        Lecture notes, slides, exercises
code/          Jupyter notebooks + per-chapter figure generators
.claude/       AI agents, skills, and hooks
docs/          Design specs, quality reports, status
hooks/         Symlink → .claude/hooks (one source of truth; also lets non-Claude runners find them)
```

## Requirements

- pdflatex + biber (TeX Live or MiKTeX)
- Python 3.9+
- Jupyter

## Running the code (Jupyter / Google Colab)

Every runnable Python file ships with a matching Jupyter notebook so students can
run it in **Google Colab** (which only runs notebooks) without a local setup:

- `code/figures/**/gen_*.ipynb` — reproduce each book figure (the figure shows
  inline and is also saved under a local `outputs/` folder).
- `code/practicals/<NN>/practical.ipynb` — run that practical's reference pipeline
  end to end, fully offline, on the bundled data. (Practicals 04–17 are *also*
  agentic Claude Code / Cline projects; the notebook is the Colab-friendly way to
  watch the reference tools run when you can't use those assistants.)

**Install the dependencies** — pick one:

```bash
# conda (creates an environment named `llmfinance`)
conda env create -f environment.yml && conda activate llmfinance

# or plain pip / virtualenv
pip install -r requirements.txt
```

**In Google Colab:** open the `.ipynb`, then run the first cell — each notebook
installs exactly what it needs (`%pip install ...`) and, for the practicals, clones
this repo automatically so the bundled data and `tools/` are available. Everything
runs offline after that; nothing calls a paid API.

## Documentation

See `docs/superpowers/specs/` for the full design specification.
