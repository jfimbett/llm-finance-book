# CLAUDE.md — Master AI Instructions

This file is loaded at the start of every AI session. It tells the AI assistant
what this project is, how it is structured, and how to behave.

---

## What This Project Is

This is a book-course template. It contains:
- A LaTeX book (`book/`) — deep treatment with proofs and references
- A course (`course/`) — lectures, slides, and exercises (a subset of the book)
- Companion code (`code/`) — Jupyter notebooks + a shared Python package
- AI agents (`.claude/agents/`) — role-based personas for specific tasks
- AI skills (`.claude/skills/`) — workflow scripts that orchestrate agents

The subject matter, audience, and quality settings are defined in `TOPIC.md`.
**Always read `TOPIC.md` at the start of any content task.**

---

## Project Conventions

1. **Numbering:** Chapter N and Lecture N cover the same topic. The book goes deeper.
   `book/chapters/01-intro/` ↔ `course/lectures/01-intro/` ↔ `code/notebooks/01-intro/`

2. **Quality gate:** Before committing any `.tex` or `.md` content file, the quality
   score for each dimension (clarity, rigor, completeness, pedagogy, style) must be
   ≥ `quality_threshold` from `TOPIC.md`. Run `/score-content` to check.

3. **Auto-commit:** If `auto_commit: true` in `TOPIC.md`, stage and commit after
   every file write with a structured message: `feat(ch01): [summary]`

4. **Agents are single-purpose:** When asked to do a task, invoke the right agent.
   Do not merge roles. The scorer scores; the editor edits; the proofreader proofs.

5. **Skills are workflows:** Run a skill when the user invokes it by name (e.g.,
   `/draft-chapter`). Follow the skill's steps exactly.

6. **Exercise difficulty tags:** Exercises use `[B]` (beginner), `[I]` (intermediate), `[A]` (advanced). Every exercises.md file should include at least one of each.

---

## Directory Quick Reference

```
.claude/agents/     Role-based AI personas — read the relevant one before acting
.claude/skills/     Workflow scripts — follow step by step
.claude/hooks/      Shell hooks — do not modify unless updating hook behavior
book/               LaTeX source — compile from book/ directory: cd book && pdflatex main.tex && biber main && pdflatex main.tex
course/             Lecture materials — markdown notes + HTML slide decks (course/slides-html/)
code/               Python package + Jupyter notebooks
docs/quality/       JSON score reports — read these to see what needs improvement
docs/STATUS.md      Auto-generated chapter status table
TOPIC.md            Project configuration — read this first on every content task
```

---

## How to Use Agents

Agents are in `.claude/agents/`. Each is a markdown file describing a role.
To use an agent: read its file, adopt its persona, then perform its task.

Example: to review math in a chapter —
1. Read `.claude/agents/math-checker.md`
2. Adopt the math-checker persona
3. Review the target file as instructed

---

## How to Use Skills

Skills are in `.claude/skills/`. Each describes a multi-step workflow.
To run a skill: read its file, follow its steps in order.

Common entry points:
- `/interview-me` — configure this project (run first)
- `/new-topic` — scaffold a new chapter/lecture/notebook unit
- `/draft-chapter` — write a chapter
- `/draft-lecture` — write a lecture from a chapter
- `/score-content [file]` — score a file and write a quality report
- `/refine-until-threshold [file]` — iteratively improve until quality passes
- `/split-dual-mode [chNN]` — wrap each section in a context or deepdive box
- `/topic-status` — print the status of all chapters
- `/ssrn-enrich [chNN]` — search SSRN for recent working papers and weave them into the chapter
- `/audit-hallucinations` — detect fabricated content and synthetic data across all chapters in parallel
- `/audit-chapter-quality [chNN]` — multi-agent 14-dimension (0–100) audit of one chapter (no edits)
- `/audit-book-quality` — book-wide fan-out audit in `main.tex` reading order + book-level reports (no edits)
- `/iterate-book-quality [chNN]` — editor→chapter-surgeon→re-score loop until ≥90 on every dimension
- `/book-quality-regression` — final gate: build + bib + cross-ref + ordering + repetition + score roll-up

The book-quality goal system is anchored by `docs/quality/RUBRIC.md` and
`docs/quality/BOOK_QUALITY_GOAL.md` (target: every chapter ≥90/100 on all 14 dimensions).

---

## Commit Message Format

```
<type>(<scope>): <summary>

Types: feat | fix | refine | chore | docs
Scope: ch01 | lec01 | code01 | agents | skills | hooks | config
```

Examples:
- `feat(ch01): draft introduction section`
- `refine(ch01): improve clarity score from 6 to 8`
- `chore: scaffold chapter 02`
