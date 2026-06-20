# /slides-from-chapter

## Purpose

Turn a finished book chapter into a **professional two-deck lecture unit**:

1. `slides.tex` — the **lesson** deck (~22–26 frames), covering every core
   concept of the chapter at graduate / practitioner depth.
2. `practical.tex` — the **practice session** deck (~12–15 frames): guided
   problems, a worked Python case study, and discussion.

Both decks use the shared style `course/lectures/_style/finance-beamer.tex`
and carry the book's **"the bigger picture" / "under the hood"** scaffold onto
the slides. Less-central material lives in a slides **appendix**, not the core
talk.

## When to Invoke

After a chapter in `book/chapters/NN-name/chapter.tex` has real, audited
content. Run per chapter, or fan out across chapters in parallel.

## Inputs Required

- Chapter number/name (e.g., `08-domain-specific-llms`)
- `book/chapters/NN-name/chapter.tex` with real content
- `course/lectures/_style/finance-beamer.tex` (shared style)

## The Standard (non-negotiable)

**Structure of every deck.** Begin with:
```latex
\documentclass{beamer}
\input{../_style/finance-beamer.tex}
\title{...}\subtitle{Lecture N — ...}\author{Juan F. Imbet}
\institute{Paris Dauphine -- PSL University}\date{\today}
\begin{document}
\begin{frame}\titlepage\end{frame}
\begin{frame}{Outline}\tableofcontents\end{frame}
```

**Lesson deck (`slides.tex`):**
- One `\section{...}` per major chapter section; 2–5 frames per section.
- Cover **every** book section's core idea. Nothing essential is dropped —
  it is either on a core frame or moved to the appendix.
- Use `\begin{bigpicture}...\end{bigpicture}` to open or frame a topic with
  the intuition / why-it-matters (mirrors the book's `context` box).
- Use `\begin{underhood}...\end{underhood}` for the mechanism: the equation,
  the algorithm, the architecture detail (mirrors the book's `deepdive` box).
- Use `block`, `alertblock`, `exampleblock`, `columns`, `booktabs` tables.
- Real equations and real numbers from the chapter — no invented figures.
- Any frame with code/verbatim must be `\begin{frame}[fragile]`.
- **Appendix:** after the core talk call `\appendixstart{Topic}` then put
  optional/extra material in `\begin{frame}[noframenumbering]{...}` frames
  (extended derivations, secondary benchmarks, edge cases, deep tangents).

**Practice deck (`practical.tex`):**
- Opens with a "Session Overview" frame: timed agenda (recap → problems →
  case study → discussion → solutions), ~1 hour.
- 1–2 recap frames (key formulas), 2–3 guided problems (with solutions),
  one Python case study tied to `code/notebooks/NN-name/`, a discussion frame.
- Same shared style; code frames `[fragile]`; may also use an appendix for
  bonus/stretch problems.

**Audience:** graduate students + industry practitioners (quants, engineers,
data scientists). Precise, not chatty. Assume calculus/linear-algebra/basic ML.

## Steps

1. Read `book/chapters/NN-name/chapter.tex` and `TOPIC.md`.
2. If the chapter is still a placeholder, stop and tell the user to draft it.
3. Map chapter sections → deck sections; decide core vs. appendix per topic.
4. Write `course/lectures/NN-name/slides.tex` (lesson) to the standard above.
5. Write `course/lectures/NN-name/practical.tex` (practice) to the standard.
6. Compile each from its directory:
   `pdflatex -interaction=nonstopmode slides.tex` (run twice for the TOC),
   same for `practical.tex`. Fix any `! ` errors (usually a missing
   `[fragile]` on a code frame) and recompile.
7. Verify coverage: every `\section{` in the chapter has a corresponding
   slide or appendix frame. Report any gap.
8. Commit: `feat(lecNN): full lesson + practical decks for [topic]`.

## Expected Output

- `slides.tex` + `slides.pdf` — full lesson deck, appendix included.
- `practical.tex` + `practical.pdf` — practice session deck.
- Both compile clean; every core chapter concept is represented.

## Error Handling

- `Illegal parameter number in definition of \iterate` → a code/verbatim
  frame is missing `[fragile]`. Add it and recompile.
- Undefined `bigpicture`/`underhood`/`\appendixstart` → the deck did not
  `\input{../_style/finance-beamer.tex}`. Add it after `\documentclass`.
- TOC/refs blank → run `pdflatex` a second time.
