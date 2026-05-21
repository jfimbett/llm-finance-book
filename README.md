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
code/          Jupyter notebooks + shared Python package
.claude/       AI agents, skills, and hooks
docs/          Design specs, quality reports, status
hooks/         Portable hook copies for non-Claude AI runners
```

## Requirements

- pdflatex + biber (TeX Live or MiKTeX)
- Python 3.9+
- Jupyter

## Documentation

See `docs/superpowers/specs/` for the full design specification.
