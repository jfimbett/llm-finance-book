# Task: Create a multi-agent book-quality goal system for the LLMs-in-Finance book

You are working inside my repository for the book **Large Language Models in Finance**.

The previous diagnostic report is in:

```text
.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md
```

Read that file first. Treat it as the factual starting point. Do not trust stale reports such as `docs/STATUS.md` or old bibliography audits without re-running or re-checking them.

Your task is to create a robust Claude Code workflow that reviews, scores, improves, and re-scores the book until each chapter scores at least **90/100** in each quality dimension.

This is not a one-agent critique. I want a multi-agent system with contrarian reviewers, an editor/orchestrator, and a separate implementer.

---

## 0. Non-negotiable project facts

Respect the following facts from `.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md`.

1. This is a LaTeX book, not Quarto or Jupyter Book.
2. The book entry point is:

```text
book/main.tex
```

3. The real reading order is the `\include{...}` order in `book/main.tex`, not the numeric order of chapter folders.
4. The current reading order is:

```text
01 → 16 → 02 → 03 → 08 → 04 → 09 → 14 → 05 → 06 → 10 → 11 → 12 → 13 → 07 → 15
```

5. Any concept-ordering, use-before-definition, repetition, or progressive-learning audit must use this reading order.
6. There are already many useful Claude Code agents and skills. Reuse existing agents/skills where appropriate instead of duplicating functionality.
7. The existing `scorer` currently scores only 5 dimensions on a 0–10 scale. I need a stricter 0–100 rubric with at least the dimensions below.
8. The existing `chapter-surgeon` should be reused as the implementation agent whenever possible.
9. The existing `audit-hallucinations` skill is the best template for book-wide parallel fan-out.
10. The orphaned valuation exercise in `exercises/valuation_example/` is a high-value asset and should be integrated into the business valuation chapter if appropriate.
11. Do not rewrite the whole book indiscriminately. Preserve good content. Make targeted, minimal, auditable changes.
12. Do not delete files unless the task explicitly identifies them as stale or duplicate and you can justify the deletion.
13. Do not modify user-level Claude settings. Only project-level files may be changed.
14. Do not expose secrets or credentials.
15. Do not run very expensive jobs unless necessary. Prefer lightweight checks and explicit summaries.

---

## 1. Overall goal

Create a project-level quality goal system so that the book can be iteratively improved until **every chapter** scores at least **90/100** on every dimension below:

1. Correctness of explanations.
2. Clear separation between big-picture concepts and under-the-hood technical details.
3. Correctness of code used to generate images, figures, diagrams, tables, examples, or exercises.
4. Proper introduction and ordering of concepts across the book.
5. Progressive learning path: chapters should build knowledge little by little.
6. Lack of unnecessary repetition.
7. Finance orientation.
8. Presence, quality, and integration of finance examples when available.
9. Correctness and cleanliness of BibTeX citations.
10. Accuracy of how cited papers are described.
11. Completeness: no missing bridge concepts, warnings, definitions, or key caveats.
12. Notation, labels, cross-references, and chapter references.
13. Reproducibility of examples, notebooks, code, and figures where relevant.
14. Pedagogical clarity for the intended audience.

The target is:

```text
chapter_score[dimension] >= 90
book_level_score[dimension] >= 90
```

If a chapter is below 90 on any dimension, the workflow should identify the issue, produce an editor-approved implementation plan, apply targeted changes, and re-score.

---

## 2. Architecture to implement

Implement a multi-agent workflow with the following roles.

### 2.1 Constructive reviewer

Create a new project-level agent if one does not already exist:

```text
.claude/agents/constructive-reviewer.md
```

Persona:

* Rewarded for identifying what is good, correct, coherent, well-explained, finance-relevant, and worth preserving.
* Should prevent unnecessary rewrites.
* Should identify strong explanations, examples, figures, citations, and pedagogical transitions.
* Should explicitly mark content as:

  * `KEEP`
  * `KEEP_BUT_MOVE`
  * `KEEP_BUT_CLARIFY`
  * `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`
  * `GOOD_FINANCE_EXAMPLE`
  * `GOOD_TECHNICAL_EXPLANATION`
  * `GOOD_BIG_PICTURE_EXPLANATION`

This agent should not implement changes.

### 2.2 Skeptical reviewer

Create a new project-level agent if needed:

```text
.claude/agents/skeptical-reviewer.md
```

You may base it on the existing `critic` agent, but keep it separate if modifying `critic` would break existing workflows.

Persona:

* Rewarded for finding errors, missing definitions, repetitions, incorrect citations, weak finance integration, concept-ordering problems, stale figures, and unsubstantiated claims.
* Should be strict and adversarial but constructive.
* Must flag severity:

  * `BLOCKER`
  * `MAJOR`
  * `MINOR`
  * `NIT`
* Must classify issues by dimension.
* Must provide file path, section/title, and line numbers where possible.
* Must distinguish:

  * local chapter issue
  * cross-chapter ordering issue
  * book-level repetition issue
  * citation/BibTeX issue
  * code/figure issue
  * finance-example issue

This agent should not implement changes.

### 2.3 Audit editor / orchestrator

Create:

```text
.claude/agents/audit-editor.md
```

Role:

* Reads the constructive and skeptical reviews.
* Decides what really matters.
* Produces a prioritized implementation plan.
* Protects strong content from being overwritten.
* Separates:

  * must-fix before scoring
  * should-fix
  * optional improvement
  * do not change
* Converts reviewer comments into precise implementation instructions for `chapter-surgeon` or another implementer.
* Explicitly checks whether a problem is local or book-wide.
* Avoids contradictory edits.
* Avoids making the chapter longer unless necessary.
* Ensures the proposed edit improves the score dimensions that are below 90.

The editor should not directly rewrite chapters except for very small instructions; implementation should be delegated to the implementer.

### 2.4 Implementer

Reuse the existing:

```text
.claude/agents/chapter-surgeon.md
```

If needed, modify it minimally so it can apply the editor’s plan while preserving strong content.

The implementer must:

* Apply targeted patches only.
* Preserve LaTeX conventions.
* Preserve labels unless intentionally fixing collisions.
* Use `\ref`, `\label`, and existing environments correctly.
* Avoid introducing hard-coded chapter numbers.
* Avoid introducing citations that are not in the bibliography.
* Avoid inventing paper claims.
* If adding a citation, add a valid BibTeX entry only when the source is verified or already present.

### 2.5 Specialized auditors

Create these only if existing agents/skills cannot cleanly do the job.

#### Finance auditor

```text
.claude/agents/finance-auditor.md
```

Checks:

* Is the chapter genuinely finance-oriented?
* Are examples from finance central rather than decorative?
* Are there missing finance examples that already exist elsewhere in the repo?
* Does the chapter connect technical ideas to financial decision-making?
* Are valuation, credit risk, portfolio, disclosure, compliance, market microstructure, banking, risk management, or corporate finance examples used when appropriate?
* Is the orphaned `exercises/valuation_example/` integrated where appropriate?

#### Concept-ordering auditor

```text
.claude/agents/concept-ordering-auditor.md
```

Checks:

* Reads `book/main.tex` and derives actual reading order.
* Builds a concept dependency map.
* Flags concepts used before definition.
* Flags topics introduced too technically too early.
* Flags redundant re-derivations.
* Suggests where a concept should have its single source of truth.

Reuse `structure-reviewer`, `outline-curator`, and `accessibility-reviewer` ideas if helpful.

#### Citation-description auditor

```text
.claude/agents/citation-description-auditor.md
```

Checks:

* BibTeX hygiene.
* Whether cited papers are described accurately.
* Whether a claim cites the right paper.
* Whether a citation is being used for the wrong proposition.
* Whether there are placeholder/stub BibTeX entries.
* Whether specific numeric claims attributed to papers need verification.
* Must explicitly check seed issues from the diagnostic report:

  * `fama1970efficient` incorrectly used for Fama-French factors.
  * duplicate key `wei2022emergent`.
  * stub `xu2024stock`.
  * possible phantom or uncertain `kang2023hallucination`.
  * stale `.bib` files.

Do not invent paper details. If verification is not possible locally, mark as `NEEDS_EXTERNAL_VERIFICATION`.

#### Code and figure auditor

```text
.claude/agents/code-figure-auditor.md
```

Checks:

* Does code run?
* Does code generate the figure claimed?
* Do figures match the prose?
* Are notebooks stale?
* Are generated images reproducible?
* Are live API calls, hard-coded user agents, or non-deterministic data sources used?
* Are there missing figures, dangling figure refs, or empty figure directories?
* Does `code/run_illustrations.sh` cover all relevant chapters?
* Are chapter code examples actually used or just orphaned?

Reuse `code-reviewer` and `figure-designer` ideas if helpful.

---

## 3. Files and skills to create

Create a canonical rubric:

```text
docs/quality/RUBRIC.md
```

Create a canonical goal file:

```text
docs/quality/BOOK_QUALITY_GOAL.md
```

Create a machine-readable score schema:

```text
docs/quality/score-schema.json
```

Create a book-level audit skill:

```text
.claude/skills/audit-book-quality/SKILL.md
```

Create a chapter-level audit skill:

```text
.claude/skills/audit-chapter-quality/SKILL.md
```

Create an iteration skill:

```text
.claude/skills/iterate-book-quality/SKILL.md
```

Create a regression/final-check skill:

```text
.claude/skills/book-quality-regression/SKILL.md
```

If Claude Code slash commands are represented by skills in this repo, the intended slash commands should be:

```text
/audit-book-quality
/audit-chapter-quality
/iterate-book-quality
/book-quality-regression
```

If the repo uses another command convention, follow the existing convention.

---

## 4. Required score outputs

For each chapter, the workflow should produce:

```text
docs/quality/book-quality/chapters/<reading_index>-<chapter_slug>/constructive-review.md
docs/quality/book-quality/chapters/<reading_index>-<chapter_slug>/skeptical-review.md
docs/quality/book-quality/chapters/<reading_index>-<chapter_slug>/editor-plan.md
docs/quality/book-quality/chapters/<reading_index>-<chapter_slug>/score.json
docs/quality/book-quality/chapters/<reading_index>-<chapter_slug>/change-log.md
```

For the book as a whole, produce:

```text
docs/quality/book-quality/BOOK_SCORE.json
docs/quality/book-quality/BOOK_SCORE.md
docs/quality/book-quality/CONCEPT_DEPENDENCY_MAP.md
docs/quality/book-quality/REPETITION_MAP.md
docs/quality/book-quality/FINANCE_EXAMPLES_MAP.md
docs/quality/book-quality/CITATION_DESCRIPTION_AUDIT.md
docs/quality/book-quality/CODE_FIGURE_AUDIT.md
docs/quality/book-quality/IMPLEMENTATION_BACKLOG.md
```

The `score.json` files must use 0–100 scores.

Each score entry must include:

```json
{
  "dimension": "...",
  "score": 0,
  "pass": false,
  "evidence": [],
  "blocking_issues": [],
  "recommended_action": ""
}
```

The chapter-level pass condition is:

```json
"pass": true
```

only if every dimension is at least 90.

The book-level pass condition is true only if:

1. every chapter passes;
2. every book-level dimension is at least 90;
3. the book compiles;
4. there are no broken references;
5. there are no unresolved citation keys;
6. there are no known duplicate labels;
7. there are no stale critical audit reports.

---

## 5. Required workflow behavior

### 5.1 Audit phase

For every chapter in the real reading order from `book/main.tex`:

1. Run constructive review.
2. Run skeptical review.
3. Run specialized checks as needed:

   * concept ordering,
   * finance examples,
   * code/figures,
   * citation descriptions,
   * notation/cross-refs.
4. Run audit editor to merge the reviews into a prioritized plan.
5. Produce a 0–100 scorecard.

Where possible, run independent chapter reviews in parallel, following the pattern of the existing `audit-hallucinations` skill.

### 5.2 Editing phase

For chapters below 90 in any dimension:

1. The audit editor selects the smallest set of changes likely to improve the failing dimensions.
2. The implementer applies the changes.
3. Re-run relevant checks.
4. Re-score.
5. Repeat until:

   * all dimensions are >= 90; or
   * max iterations is reached; or
   * the issue requires human/external verification.

Respect the project’s existing `max_refine_iterations` from `TOPIC.md`, but adapt it to the 0–100 system.

### 5.3 Regression phase

After edits:

1. Build the book.
2. Re-run bibliography checks.
3. Re-run cross-reference checks.
4. Re-run concept-ordering checks.
5. Re-run repetition checks.
6. Re-run code/figure checks where applicable.
7. Re-run score aggregation.
8. Write a final report.

---

## 6. Seed issues that must be included in the first backlog

The diagnostic report already found several concrete issues. Include these in the initial `IMPLEMENTATION_BACKLOG.md` and make sure the workflow can detect them in the future.

1. Reading order differs from filename order.
2. Chapter 16 is logically introductory but numbered and placed unusually.
3. Chapter 16 uses `\parencite/\textcite` while other chapters use `\citet/\citep`.
4. `exercises/valuation_example/` contains a complete AAPL Claude valuation exercise but is not linked from the valuation chapter.
5. Chapter 5 uses WACC but does not properly derive or introduce it.
6. Figures exist only for chapters 1–7; chapters 8–16 and appendices have empty figure folders.
7. Chapter 11 has a dangling reference to `fig:ch11-rag-pipeline`.
8. `def:calibration` label is defined more than once.
9. Chapter 10 has a broken hard-coded prose reference: “Chapter 7 on regulatory compliance”.
10. Chapter 13 cites `fama1970efficient` for Fama-French factors, where `fama1993common` is likely the correct citation.
11. `wei2022emergent` is duplicated in the bibliography.
12. `xu2024stock` is a stub BibTeX entry.
13. Some statistical primitives are never defined or are defined too late:

    * KL divergence,
    * n-gram,
    * CAPM,
    * cross-entropy,
    * softmax.
14. SHAP is referenced before being properly introduced.
15. AUROC is used before being properly introduced.
16. LoRA is re-derived in multiple places.
17. Attention is heavily duplicated between chapters 1 and 2.
18. RAG is duplicated between chapters 4 and 7.
19. Regulatory frameworks are reintroduced in chapters 11, 12, and 15.
20. Existing reports such as `docs/STATUS.md` and old bibliography audits are stale.

---

## 7. Rubric details

In `docs/quality/RUBRIC.md`, define each dimension strictly.

Use this scale:

```text
0–49: failing
50–69: weak
70–79: acceptable draft
80–89: good but not release-ready
90–94: release-quality
95–100: excellent
```

A chapter must not receive 90 merely because it is readable.

A 90 requires:

* correct explanations;
* no known major errors;
* appropriate definitions before use;
* finance-relevant examples where appropriate;
* no unnecessary repetition;
* accurate citations;
* working or clearly reproducible code/figures where relevant;
* clear separation between intuition and technical detail;
* smooth progression relative to previous chapters.

A 100 is rare and requires near-perfect content, structure, examples, citations, and reproducibility.

---

## 8. Specific integration requirement: valuation exercise

Inspect:

```text
exercises/valuation_example/
book/chapters/05-business-valuation/chapter.tex
```

Determine how to integrate the valuation exercise into the book.

Possible options:

1. Add a short boxed case study in chapter 5 pointing to the exercise.
2. Add a subsection explaining the AAPL Claude valuation workflow.
3. Add an appendix reference.
4. Add a reader exercise linking the chapter’s DCF/WACC discussion to the existing workflow.
5. Add a “companion exercise” note without overloading the chapter.

Do not blindly paste the whole exercise into the chapter.

The editor must decide the minimal integration that improves:

* finance example quality;
* finance orientation;
* code/example integration;
* progressive learning;
* completeness of WACC/DCF discussion.

---

## 9. Specific requirement: big-picture vs under-the-hood separation

Where a chapter mixes intuition and technical details too early, the workflow should suggest using existing LaTeX environments from `book/preamble.tex`, such as:

* context boxes,
* deepdive boxes,
* definitions,
* examples,
* warnings,
* takeaways.

Do not create new LaTeX environments unless necessary.

The goal is that readers can distinguish:

1. What they need to understand conceptually.
2. What is optional mathematical or implementation detail.
3. What is finance-specific application.

---

## 10. Specific requirement: concept single-source-of-truth

For repeated concepts, the workflow should designate one chapter as the main explanation and turn later repetitions into short reminders or cross-references.

Examples to check:

* attention,
* transformers,
* LoRA,
* RAG,
* calibration,
* regulatory frameworks,
* GDPR,
* MiFID II,
* SR 11-7,
* EU AI Act,
* SHAP,
* AUROC,
* WACC/CAPM.

Use `\ref{...}` references, not hard-coded chapter numbers.

---

## 11. Specific requirement: citation accuracy

The citation-description auditor should distinguish:

1. BibTeX hygiene:

   * duplicate keys,
   * missing fields,
   * malformed entries,
   * unused entries,
   * stale bibliography files.

2. Citation resolution:

   * undefined citation keys,
   * cited but missing entries.

3. Citation-content accuracy:

   * whether the cited paper actually supports the sentence;
   * whether a different paper is more appropriate;
   * whether a numerical result is accurately described;
   * whether a citation is a placeholder or uncertain.

If external verification is needed and unavailable, mark the issue as:

```text
NEEDS_EXTERNAL_VERIFICATION
```

Do not invent details.

---

## 12. Specific requirement: code and figure correctness

The code/figure auditor should check:

1. Whether the code exists.
2. Whether it is actually used in the book.
3. Whether it runs or is plausibly runnable.
4. Whether it depends on live APIs or large downloads.
5. Whether generated figures are stale.
6. Whether figures match the surrounding prose.
7. Whether every referenced figure exists.
8. Whether every figure has a useful caption.
9. Whether figure-generation scripts are covered by a reproducibility plan.
10. Whether notebooks are real or placeholders.

Do not attempt to fully solve reproducibility in this task unless it is simple. Create a backlog where needed.

---

## 13. Implementation style

When creating or modifying Claude Code agents and skills:

1. Follow the style of existing `.claude/agents/*.md`.
2. Follow the style of existing `.claude/skills/*/SKILL.md`.
3. Reuse existing agents where possible.
4. Avoid breaking existing skills.
5. Prefer additive changes over destructive rewrites.
6. Include exact output paths in each skill.
7. Include clear pass/fail criteria.
8. Include JSON schemas where useful.
9. Include instructions to run independent chapter analyses in parallel when possible.
10. Include instructions to write concise summaries for the user after each major phase.

---

## 14. What to do now

Perform the following steps.

### Step A — Inspect current setup

Read these files first:

```text
.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md
book/main.tex
TOPIC.md
.claude/CLAUDE.md
.claude/settings.json
.claude/agents/scorer.md
.claude/agents/critic.md
.claude/agents/hallucination-detector.md
.claude/agents/structure-reviewer.md
.claude/agents/code-reviewer.md
.claude/agents/fact-checker.md
.claude/agents/chapter-surgeon.md
.claude/skills/audit-hallucinations/SKILL.md
.claude/skills/full-review/SKILL.md
.claude/skills/refine-until-threshold/SKILL.md
book/preamble.tex
```

### Step B — Create or update the quality system

Create or update the files listed in sections 2 and 3.

Do not start mass-rewriting chapters yet.

### Step C — Run a dry-run audit on two chapters

After creating the system, run a dry-run audit on:

```text
book/chapters/01-intro/chapter.tex
book/chapters/05-business-valuation/chapter.tex
```

The dry run should produce reviews, editor plans, and score JSON files, but should not make chapter edits unless the skill explicitly supports a dry-run mode and you are certain edits are safe.

Use these two chapters because:

* chapter 1 tests introduction, concept ordering, and repetition with chapter 2;
* chapter 5 tests finance orientation, WACC/DCF completeness, and integration of the orphaned valuation exercise.

### Step D — Produce a final implementation report

Create:

```text
docs/quality/book-quality/SETUP_REPORT.md
```

This report must include:

1. Files created.
2. Files modified.
3. Agents created or modified.
4. Skills created or modified.
5. How to run the new workflow.
6. What the dry run found for chapter 1.
7. What the dry run found for chapter 5.
8. Whether the system is ready to run on the full book.
9. Any blockers or human decisions required.
10. The exact next command I should run in Claude Code.

---

## 15. Expected final message to me

When done, print a concise message with:

1. Whether the quality goal system was created.
2. The list of new slash commands or skills.
3. The main dry-run findings.
4. Whether any files were edited beyond agents/skills/docs.
5. The exact next command I should run to launch the full iterative audit.

Do not claim the book is fully improved yet unless you actually ran the full iterative workflow and all dimensions passed.
