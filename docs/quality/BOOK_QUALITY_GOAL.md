# BOOK_QUALITY_GOAL.md — Canonical Quality Goal

> The single source of truth for **what "done" means** for *Large Language Models in
> Finance*. Anchors the multi-agent audit/iterate/regression workflow. Read this and
> [`RUBRIC.md`](RUBRIC.md) before running any `/audit-book-quality`,
> `/audit-chapter-quality`, `/iterate-book-quality`, or `/book-quality-regression`.

---

## The goal

Every chapter — and the book as a whole — scores **≥ 90/100 on every applicable
dimension** of the 14-dimension rubric in [`RUBRIC.md`](RUBRIC.md):

```
chapter_score[dimension] >= 90   for all chapters, all dimensions
book_level_score[dimension] >= 90   for all book-level dimensions
```

When a chapter is below 90 on any dimension, the workflow:
1. identifies the issue (constructive + skeptical reviewers + specialized auditors),
2. produces an **editor-approved** minimal implementation plan,
3. applies targeted changes via `chapter-surgeon`,
4. re-scores,
5. repeats until pass, `max_iterations` is reached, or external verification is needed.

This is **not** a one-agent critique. It is a contrarian-reviewer pair (constructive +
skeptical) → editor/orchestrator → implementer loop, fanned out per chapter in the
**`main.tex` reading order**, modelled on the `audit-hallucinations` parallel pattern.

---

## Non-negotiable facts (from `BOOK_AUDIT_PROJECT_CONTEXT.md`)

1. LaTeX book; entry point `book/main.tex`; build via `scripts/build-book.sh`.
2. Reading order = `\include` order in `main.tex`, **not** folder numbers.
3. Reading order: `01 → 16 → 02 → 03 → 08 → 04 → 09 → 14 → 05 → 06 → 10 → 11 → 12 → 13 → 07 → 15`.
4. Reuse existing agents/skills; do not duplicate functionality.
5. Reuse `chapter-surgeon` as implementer; reuse `audit-hallucinations` as the fan-out template.
6. Preserve good content. Targeted, minimal, auditable changes only.
7. Do not delete files unless explicitly identified as stale/duplicate and justified.
8. Project-level files only. No user-level Claude settings. No secrets.
9. Prefer lightweight checks; avoid expensive jobs unless necessary.

---

## Roles

| Role | Agent | Implements? |
|------|-------|-------------|
| Constructive reviewer | `constructive-reviewer` | No |
| Skeptical reviewer | `skeptical-reviewer` (sibling of `critic`) | No |
| Audit editor / orchestrator | `audit-editor` | Only trivial one-liners |
| Implementer | `chapter-surgeon` (reused) | Yes — targeted patches |
| Finance auditor | `finance-auditor` | No |
| Concept-ordering auditor | `concept-ordering-auditor` | No |
| Citation-description auditor | `citation-description-auditor` | No |
| Code/figure auditor | `code-figure-auditor` | No |
| Scoring engines (reused) | `math-checker`, `fact-checker`, `hallucination-detector`, `cross-ref-checker`, `consistency-checker`, `code-reviewer`, `structure-reviewer`, `pedagogy-reviewer`, `accessibility-reviewer` | No |

## Skills (slash commands)

| Command | Purpose |
|---------|---------|
| `/audit-chapter-quality [chNN or reading#]` | Full multi-agent audit of one chapter → reviews + plan + score |
| `/audit-book-quality` | Fan-out audit across all chapters in reading order → per-chapter + book-level reports |
| `/iterate-book-quality [chNN]` | Editor→surgeon→re-score loop until ≥90/dim or max iterations |
| `/book-quality-regression` | Build + bib + cross-ref + ordering + repetition + code/figure + score roll-up |

## Output locations

Per chapter, under `docs/quality/book-quality/chapters/<read#>-<slug>/`:
`constructive-review.md`, `skeptical-review.md`, `editor-plan.md`, `score.json`,
`change-log.md`.

Book-level, under `docs/quality/book-quality/`:
`BOOK_SCORE.json`, `BOOK_SCORE.md`, `CONCEPT_DEPENDENCY_MAP.md`, `REPETITION_MAP.md`,
`FINANCE_EXAMPLES_MAP.md`, `CITATION_DESCRIPTION_AUDIT.md`, `CODE_FIGURE_AUDIT.md`,
`IMPLEMENTATION_BACKLOG.md`, `SETUP_REPORT.md`.

## Iteration budget

Reuse `max_refine_iterations` from `TOPIC.md` (currently 5), adapted to 0–100: one
iteration = one editor-plan → surgeon-patch → re-score cycle. Stop at pass,
`max_iterations`, or a `NEEDS_EXTERNAL_VERIFICATION` / human-decision blocker.
