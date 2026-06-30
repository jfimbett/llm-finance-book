# Task: Generate project context for LLMs-in-Finance book audit system

You are working inside my book project repository. The book is about **Large Language Models in Finance**. I want to build a rigorous multi-agent review/editing workflow later, but first I need you to inspect the current project and write a factual diagnostic report.

## Goal

Create a markdown file named:

```text
.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md
```

(The repo root keeps a `BOOK_AUDIT_PROJECT_CONTEXT.md` symlink to this path, so
references by the bare filename still resolve.)

This file should contain everything another AI assistant would need in order to design a robust Claude Code workflow that scores and improves the book across these dimensions:

1. Correctness of explanations.
2. Accurate separation between big-picture concepts and under-the-hood technical details.
3. Correctness of the code used to generate images, figures, diagrams, and examples.
4. Proper introduction and ordering of topics across chapters.
5. Progressive learning path: chapters should build knowledge little by little.
6. Lack of unnecessary repetition across chapters.
7. Finance orientation of the content.
8. Presence and quality of finance examples when available.
9. Correctness of BibTeX citations.
10. Accuracy of the way cited papers are described.
11. Missing important topics, concepts, examples, warnings, or bridge explanations.
12. Any other dimension you think is important for a high-quality technical book.

Do **not** redesign the project yet. Do **not** rewrite chapters yet. Do **not** create or modify agents/skills/workflows yet, except for writing this diagnostic markdown report.

## Important constraints

* Be factual and concrete.
* Do not guess.
* If something is missing, say it is missing.
* If something is unclear, say what file or folder made it unclear.
* Use exact file paths.
* Quote short snippets when useful.
* Redact secrets, tokens, API keys, or private credentials.
* Do not make destructive changes.
* Do not install new packages.
* Do not run expensive long jobs unless absolutely necessary.
* You may run safe inspection commands such as `ls`, `find`, `tree`, `rg`, `cat`, `sed`, `git status`, and lightweight build/test discovery commands.
* If parallel exploration is available, use it to inspect independent parts of the repo efficiently.

## Report structure

Write `.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md` with the following sections.

---

# 1. Repository overview

Describe the repository at a high level.

Include:

* Project root path.
* Git status summary.
* Main directories.
* Main book source directory or directories.
* Output/build directory if present.
* Whether this appears to be Quarto, Markdown, LaTeX, Jupyter Book, plain Markdown, custom scripts, or something else.
* Main commands used to build/render the book, if discoverable.
* Main configuration files.

Include a compact tree of the project, excluding heavy folders like `.git`, virtual environments, caches, build artifacts, and dependency folders.

---

# 2. `.claude` and Claude Code setup

Inspect all Claude Code-related files and folders.

Look especially for:

* `.claude/`
* `CLAUDE.md`
* Claude settings files
* custom slash commands
* agents/subagents
* skills
* hooks
* MCP configuration
* workflow files
* scripts used by Claude Code
* any existing goal/review/evaluation files

For each item found, report:

* File path.
* Type: setting, agent, skill, command, hook, workflow, prompt, other.
* Short description of what it does.
* Whether it is project-level or user-level if discoverable.
* Whether it seems relevant for the book audit workflow.
* Whether it should probably be reused, modified, or replaced later.

If there are agents or skills, create a table:

| Name | Path | Type | Purpose | Strengths | Limitations | Reuse recommendation |
| ---- | ---- | ---- | ------- | --------- | ----------- | -------------------- |

Do not create new agents yet.

---

# 3. Current book structure

Identify all chapters, appendices, front matter, exercises, notebooks, examples, and supporting files.

Create a table:

| Order | Chapter/file | Title | Approx. topic | Format | Depends on earlier concepts? | Possible issues noticed |
| ----- | ------------ | ----- | ------------- | ------ | ---------------------------- | ----------------------- |

For each chapter, identify:

* Title.
* File path.
* Its apparent role in the book.
* Major concepts introduced.
* Major finance examples used.
* Code examples used.
* Figures/images generated or referenced.
* Citations used.
* Any obvious missing prerequisites.
* Any obvious repetition with other chapters.
* Any obvious places where a technical concept appears before being introduced.

This is only a preliminary scan. Do not do the full review yet.

---

# 4. Concept dependency map

Build a preliminary dependency map of concepts.

Include concepts such as, if present:

* LLMs
* NLP
* tokens/tokenization
* embeddings
* attention
* transformers
* pretraining
* fine-tuning
* instruction tuning
* RLHF/RLAIF
* retrieval-augmented generation
* agents
* tool use
* evaluation
* hallucination
* prompting
* structured outputs
* classification
* sentiment analysis
* credit risk
* asset pricing
* valuation
* financial statements
* corporate finance
* risk management
* regulatory/ethical issues
* data privacy
* model interpretability
* backtesting
* any other important concepts present in the book

For each concept, provide:

| Concept | First appears in | First properly explained in | Used before explained? | Notes |
| ------- | ---------------- | --------------------------- | ---------------------- | ----- |

Flag cases where a concept seems to be used before being introduced.

---

# 5. Finance examples inventory

Identify all finance-oriented examples, exercises, case studies, notebooks, figures, and code.

Create a table:

| Example | Location | Finance area | Technical concept illustrated | Complete or partial? | Notes |
| ------- | -------- | ------------ | ----------------------------- | -------------------- | ----- |

Pay special attention to whether there is a **business valuation exercise using Claude** or similar material. I remember doing such an exercise, but I am not seeing it clearly in the book. Search for terms such as:

* valuation
* DCF
* discounted cash flow
* business valuation
* company valuation
* multiples
* comparables
* Claude
* financial statements
* cash flows
* terminal value
* WACC

Report whether you find it, where it is, and whether it appears integrated into the book.

---

# 6. Code and figure-generation inventory

Identify all code used in the book, especially code that generates:

* figures
* diagrams
* plots
* tables
* screenshots
* examples
* synthetic data
* finance exercises
* notebooks

Create a table:

| File | Language | Purpose | Generates figures? | Used in chapter(s) | Has tests? | Obvious risks |
| ---- | -------- | ------- | ------------------ | ------------------ | ---------- | ------------- |

Also report:

* How images are generated.
* Where generated images are stored.
* Whether images are checked into the repo.
* Whether figure-generation code appears reproducible.
* Whether there are stale generated files.
* Whether there are tests or validation scripts.
* Whether code is embedded directly in chapters or imported from scripts/notebooks.

Do not fix code yet.

---

# 7. Bibliography and citation inventory

Find all bibliography-related files:

* `.bib`
* CSL files
* citation keys in chapters
* references sections
* manually written citations
* paper summaries

Create a table:

| Citation key | Bibliography file | Cited in chapters | Title/authors/year from BibTeX | Obvious issue |
| ------------ | ----------------- | ----------------- | ------------------------------ | ------------- |

Also report:

* Missing citation keys.
* Unused bibliography entries.
* Duplicate entries.
* Suspicious or incomplete BibTeX entries.
* Citation keys that appear malformed.
* Places where the text claims a result from a paper and should later be fact-checked.
* Whether there is enough information to verify the content of cited papers later.

Do not fact-check every paper yet, but identify which cited papers will need content verification.

---

# 8. Existing quality-control mechanisms

Identify current mechanisms for quality control, such as:

* tests
* linters
* spell checkers
* build checks
* notebooks execution
* citation checks
* link checks
* figure-generation checks
* custom review scripts
* Claude agents or skills for reviewing
* workflows or goals

Create a table:

| Mechanism | Path/command | What it checks | Is it currently usable? | Gaps |
| --------- | ------------ | -------------- | ----------------------- | ---- |

Also identify any missing mechanisms that would be useful for the future workflow.

---

# 9. Proposed audit architecture, based only on current setup

Based on the current repo and Claude setup, propose what should probably be created or modified later.

Do not implement it yet.

Discuss whether the future workflow should include:

* `/goal` command or equivalent.
* Chapter-level scoring.
* Book-level scoring.
* Two contrarian reviewer agents per chapter:

  * one constructive reviewer rewarded for identifying what is good, coherent, and worth preserving;
  * one skeptical reviewer rewarded for identifying flaws, missing explanations, errors, weak citations, repetition, and finance gaps.
* An editor/orchestrator agent that compares the two reviews and creates an implementation plan.
* A separate implementer agent that modifies chapters.
* A citation auditor.
* A code/figure auditor.
* A finance examples auditor.
* A concept-ordering auditor.
* A final regression/checking workflow.
* A scorecard format.
* A loop that iterates until each chapter scores at least 90% on each dimension.

For each proposed component, include:

| Proposed component | Create new or modify existing? | Reason | Files likely affected |
| ------------------ | ------------------------------ | ------ | --------------------- |

---

# 10. Recommended scoring rubric draft

Create a preliminary scoring rubric for the future workflow.

Use this table:

| Dimension | Score 0 means | Score 50 means | Score 90 means | Score 100 means | Evidence required |
| --------- | ------------- | -------------- | -------------- | --------------- | ----------------- |

Include at least the dimensions listed in the goal, plus any additional dimensions you think are important.

The rubric should be strict. A chapter should not get 90 merely because it is readable. It should get 90 only if it is correct, progressive, non-repetitive, finance-oriented where appropriate, properly cited, and supported by working code where relevant.

---

# 11. Risks and unknowns

List the main risks for building the future workflow.

Examples:

* The book has no explicit chapter order.
* Concepts are scattered across files.
* Code is embedded in notebooks and hard to test.
* Bibliography is incomplete.
* Claude agents already exist but overlap.
* There is no build command.
* Figures are generated manually.
* Some chapters mix conceptual and technical explanations too early.
* Finance examples are not systematically integrated.

For each risk, include:

| Risk | Evidence | Why it matters | Suggested next step |
| ---- | -------- | -------------- | ------------------- |

---

# 12. Exact files that another assistant should read next

Provide a prioritized list of files that another assistant should read before designing the final workflow.

Create a table:

| Priority | File/folder | Why it matters |
| -------- | ----------- | -------------- |

---

# 13. Executive summary for ChatGPT

End with a concise section titled:

```text
Executive summary for ChatGPT
```

This should be written specifically for another AI assistant that will receive this report and then design the exact Claude Code prompt/workflow.

Include:

* What the project is.
* What the book structure looks like.
* What Claude Code setup already exists.
* Which agents/skills/workflows already exist and are reusable.
* What is missing.
* What the highest-priority design decisions are.
* What you recommend doing next.

## Final instruction

After writing `.claude/context/BOOK_AUDIT_PROJECT_CONTEXT.md`, print a short message telling me:

1. The file was created.
2. The most important 5 findings.
3. Any places where you were unable to inspect something.
