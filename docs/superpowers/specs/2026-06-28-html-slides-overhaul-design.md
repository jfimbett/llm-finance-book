# HTML Slides Overhaul — Design

**Date:** 2026-06-28
**Status:** Approved (design)
**Owner:** Juan Imbett

## Problem

The HTML slide decks in `course/slides-html/` have three issues:

1. **Wrong audience framing.** The decks (and the shared engine/spec) were authored as
   "MBA-facing" with details collapsed. The real audience is a **summer school** of mixed
   grad students and practitioners — not MBAs. There are 55 "MBA" mentions across decks,
   plus references in `AUTHORING.md`, `slides.js`, and `slides.css`.
2. **No figures.** Not a single `<img>` or `<svg>` figure exists in any of the 34 decks,
   even though figures are pedagogically important and the book contains them.
3. **Incomplete coverage.** The decks skip material. Each chapter needs one complete deck
   that covers every major concept from the book chapter — faithful and complete, but not a
   verbatim copy-paste of the book.

Additionally, the legacy Beamer PDF decks are no longer wanted and should be deleted.

## Goals

- Reframe all decks for a **summer school** audience (mixed grad/practitioner). Keep the
  collapsed-details affordance; drop all MBA framing.
- Embed a meaningful **figure** in every chapter's deck.
- Achieve **complete coverage**: every major concept from the corresponding book chapter is
  present in slide form.
- **Delete** all legacy Beamer artifacts; HTML becomes the single source of truth.

## Non-Goals

- No changes to book chapters (`book/chapters/**`) — the book is the *source*, not a target.
- No redesign of the HTML slide engine's navigation/UX behavior. Engine edits are limited to
  removing MBA wording and supporting figures if needed.
- No unrelated refactoring of unrelated tooling.

## Scope

All **34 HTML decks**:
- 17 lesson decks: `course/slides-html/<NN>-name/index.html`
- 17 practical decks: `course/slides-html/<NN>-name/practical.html`

There is a clean 1:1 name mapping between `course/slides-html/<NN>` and `book/chapters/<NN>`
for all 17 chapters (verified).

## Decisions (from brainstorming)

| Question | Decision |
|---|---|
| Figures | **Embed real + author new** — embed the 13 real matplotlib figures as web images, AND create proper figures for chapters that only have placeholders, so every chapter has a meaningful figure. |
| Delete scope | **All Beamer artifacts** — `slides.pdf`, `practical.pdf`, `slides.tex`, Beamer `.tex` sources, and `build-slides` tooling. HTML is the single source of truth. |
| Deck scope | **Lesson + practical** — all 34 decks get the de-MBA + figures + completeness pass. |
| Completeness source/bar | **Cover every book-chapter concept** — each lesson deck presents every major concept/section from the corresponding book chapter; faithful, nothing omitted, not verbatim. |
| Audience | **Mixed grad/practitioner** — keep plain-language lead + collapsed details, but the surface may carry slightly more formalism than the old exec-level framing. |

## Design

### A. Audience reframe (de-MBA)

- Remove all 55 "MBA" mentions across the 34 decks.
- Update `course/slides-html/AUTHORING.md`: replace "MBA-facing" intent and "the MBA story"
  description of `.bigpicture` with summer-school / mixed grad-practitioner language. The
  *design intent* is preserved (plain-language surface, math one click away in
  `aside.underhood`); only the audience label and tone target change.
- Remove MBA references from `course/slides-html/assets/slides.js` and `assets/slides.css`
  (these are wording/comments only — no behavioral change).
- `course/slides-html/index.html` (landing page) reframed to summer school.
- Tone target on the surface: comprehensible to a quantitatively comfortable but not
  CS/ML-expert reader; formulas and derivations stay in `aside.underhood`.

### B. Figures

- **Location:** `course/slides-html/assets/figures/<NN>/` — PNG for matplotlib output,
  SVG for hand-authored conceptual diagrams. Referenced via relative paths from each deck.
- **Real data figures (13 chapters with `gen_*.py`):** re-run the existing generator scripts
  (they already emit `.png` at 160 dpi) and copy/emit the PNG into the figures dir; embed on
  the relevant slide with a caption and a source/credit line.
- **Placeholder chapters** (only `fig_illustration.pdf` exists): author a *new* figure —
  - a new matplotlib `gen_*.py` when the concept is data/plot-shaped, OR
  - an inline **SVG/CSS diagram** when the concept is structural (architecture, pipeline,
    flow). Diagrams follow the deck's visual style.
- **Result:** every chapter's deck contains at least one meaningful, on-topic figure with a
  caption.
- Embedding markup: a figure block (`<figure>` with `<img>`/inline `<svg>` + `<figcaption>`)
  that fits the existing slide component vocabulary.

### C. Completeness pass (per chapter)

Source of truth = the **book chapter `.tex`** (`book/chapters/<NN>/**.tex`).

For each chapter:
1. **Extract a concept checklist** from the chapter: sections, named results/methods, key
   numbers, citations (Author, year).
2. **Diff** the checklist against the current deck to find omissions.
3. **Rewrite** the deck so every checklist item is covered: one idea per slide, split dense
   frames, plain-language lead, equations/derivations in `aside.underhood`, citations and
   numbers preserved. Faithful and complete — not a verbatim copy of the book.
4. **Practical decks** (`practical.html`) receive the same de-MBA + figures treatment and
   cover the chapter's applied / worked material.

All authoring follows the (updated) `course/slides-html/AUTHORING.md` component vocabulary
and editorial rules.

### D. Execution model

- Process **chapter by chapter** (lesson + practical together). Use parallel subagents to
  scale across the 17 chapters; each subagent follows `AUTHORING.md` and this spec.
- **Per-deck validation gate** (headless Chrome, the existing approach): page loads with no JS
  console errors, KaTeX renders, all figures resolve (no broken image links), first slide has
  `current`, deck navigates.
- **Deletion of Beamer artifacts is the final dedicated step**, performed only after the HTML
  decks are confirmed good — so nothing is lost prematurely. Targets:
  - `course/lectures/<NN>/slides.pdf`, `course/lectures/<NN>/practical.pdf`
  - `course/lectures/<NN>/slides.tex` and any Beamer `.tex` sources for slides
  - `build-slides` tooling/skill that builds the Beamer PDFs
  - `course/lectures/_style` only if it is exclusively Beamer slide styling (verify before
    deleting; keep if shared with other lecture materials)
- Update `AUTHORING.md` to reflect the new audience + figure conventions (part of step A).

## Acceptance Criteria

1. Zero "MBA" occurrences anywhere under `course/slides-html/` (decks, assets, AUTHORING.md,
   landing page).
2. Every one of the 34 decks contains at least one embedded, on-topic figure that loads
   without error.
3. Every lesson deck covers every major concept from its book chapter (verified against the
   per-chapter concept checklist); no checklist item omitted.
4. All 34 decks pass the headless-Chrome validation gate (no JS errors, KaTeX renders,
   figures resolve).
5. All legacy Beamer artifacts (`slides.pdf`, `practical.pdf`, Beamer `.tex` sources,
   `build-slides` tooling) are deleted; no dangling references remain.
6. `AUTHORING.md` reflects the summer-school audience and figure conventions.

## Risks & Mitigations

- **Premature deletion of Beamer sources** loses content that may not yet be in HTML.
  *Mitigation:* delete only as the final step, after HTML decks pass the gate and a content
  diff confirms coverage.
- **Figure generation environment** (matplotlib deps) may not be set up.
  *Mitigation:* verify the figure toolchain runs before fanning out; fall back to inline SVG
  diagrams where a generator can't run.
- **Scale (34 decks)** risks inconsistency.
  *Mitigation:* single shared `AUTHORING.md` + this spec as the contract; per-deck validation
  gate; concept checklist per chapter as the completeness contract.
- **Working-tree integrity** — `auto_commit` is on and a mass deletion has happened before.
  *Mitigation:* review `git diff --stat` before committing; stage deletions deliberately.
