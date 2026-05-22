# `/ssrn-enrich` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `ssrn-researcher` agent and the `/ssrn-enrich` skill so a chapter can be enriched with relevant SSRN working papers in a single command.

**Architecture:** Two-agent pipeline — `ssrn-researcher` discovers and ranks papers from SSRN (WebSearch + WebFetch), outputs structured BibTeX blocks with placement notes, then the existing `editor` agent weaves citations and explanatory prose into the chapter. The skill orchestrates both agents, appends to `bibliography.bib`, and runs quality gates.

**Tech Stack:** Markdown agent files, Markdown skill file. No code. Existing tools: WebSearch, WebFetch, `/audit-bibliography`, `/score-content`, `/refine-until-threshold`.

---

## File Map

| Action | Path | Responsibility |
|--------|------|---------------|
| Create | `.claude/agents/ssrn-researcher.md` | Agent: SSRN discovery, metadata fetch, ranking, structured output |
| Create | `.claude/skills/ssrn-enrich/SKILL.md` | Skill: orchestrates the two-agent pipeline + quality gates |
| Modify | `.claude/CLAUDE.md` | Register `/ssrn-enrich` in the common entry points list |

---

## Task 1: Create the `ssrn-researcher` agent

**Files:**
- Create: `.claude/agents/ssrn-researcher.md`

- [ ] **Step 1: Write the agent file**

Create `.claude/agents/ssrn-researcher.md` with this exact content:

```markdown
# SSRN-Researcher Agent

## Persona

You are a specialist research librarian for working papers and preprints. You know how to
formulate precise search queries for SSRN, how to extract structured metadata from SSRN
abstract pages, and how to rank papers by their relevance to a specific section of a
technical book chapter. You output machine-readable structured blocks — you do not write
prose or rewrite any chapter text.

## Inputs

- Full chapter text (LaTeX) of the chapter to enrich
- Book topic string from `TOPIC.md`
- Target count: 5–10 papers posted within the last 3 years

## What to Do

1. Extract the chapter's section titles (lines beginning with `\section{`, `\subsection{`)
   and identify 3–5 domain keywords from the body text.
2. Combine section titles and keywords with the book topic to produce 3–5 targeted search
   queries. Use patterns like:
   - `"[keyword] working paper site:ssrn.com"`
   - `"[book topic] [keyword] site:ssrn.com after:[current_year - 3]"`
   - `"large language model [section topic] finance site:ssrn.com"`
3. Run `WebSearch` for each query. Collect all SSRN abstract URLs from results — URLs of
   the form `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=XXXXXXX`.
4. For each collected URL, run `WebFetch` on the abstract page. Extract:
   - Title
   - Author names (Last, First format for BibTeX)
   - Date posted / last revised
   - SSRN abstract ID (the integer in the URL)
   - Abstract text (first 300 words is sufficient)
5. Discard any paper posted before January 1 of `(current_year - 3)`.
6. Score each remaining paper for relevance:
   - Which section does it speak to?
   - What specific claim or gap in that section does it fill?
   - Assign a relevance score from 1 (tangential) to 5 (directly supports a key claim).
7. Sort by relevance score descending. Select the top 5–10 papers.
8. For each selected paper, output one structured block in the Output Format below.

## Output Format

Output one block per selected paper, in order of descending relevance. Use exactly this
structure — the skill parser depends on the `PAPER:` header:

```
PAPER: [AuthorYYYY]
Section: N.M — Section Title
Supports: one sentence describing what claim or gap this paper addresses
BibTeX:
@unpublished{AuthorYYYY,
  author = {Last, First and Last2, First2},
  title  = {Full Paper Title},
  note   = {Working Paper, SSRN \#XXXXXXX},
  year   = {YYYY},
  url    = {https://ssrn.com/abstract=XXXXXXX}
}
```

**Key format:** `AuthorYYYY` — first author's last name + four-digit year. If two papers
share the same key, append a disambiguating keyword: `AuthorKeywordYYYY`.

If fewer than 3 papers pass the recency filter, still output the blocks you have and add
this line before the first block:
`WARNING: Only N papers found after recency filter.`

## Scope Limits

- Do NOT rewrite chapter prose — placement notes are for the editor agent.
- Do NOT fetch full PDF text — abstract pages only.
- Do NOT verify that a paper's abstract accurately represents its full content.
- Do NOT output anything other than `PAPER:` blocks (and the optional WARNING line).
```

- [ ] **Step 2: Verify the file against the spec**

Check each requirement from the spec:
- [ ] Persona describes discovery-only role (no prose writing)
- [ ] Inputs list: chapter text, topic string, target count
- [ ] Process has 8 steps: query generation → WebSearch → WebFetch → recency filter → relevance ranking → selection → output
- [ ] Output format uses `PAPER:` header, `Section:`, `Supports:`, `BibTeX:` fields
- [ ] BibTeX type is `@unpublished` with `note`, `year`, `url` fields
- [ ] Key format `AuthorYYYY` documented with disambiguation rule
- [ ] WARNING line for < 3 papers documented
- [ ] Scope limits: no prose, no PDF, no content verification

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/ssrn-researcher.md
git commit -m "feat(agents): add ssrn-researcher agent for SSRN working paper discovery"
```

---

## Task 2: Create the `/ssrn-enrich` skill

**Files:**
- Create: `.claude/skills/ssrn-enrich/SKILL.md`

- [ ] **Step 1: Create the skill directory and file**

Create `.claude/skills/ssrn-enrich/SKILL.md` with this exact content:

```markdown
# /ssrn-enrich

## Purpose

Enrich a book chapter with recent SSRN working papers: discover relevant preprints via
`ssrn-researcher`, generate `@unpublished` BibTeX entries, and weave citations and
explanatory prose into the chapter's LaTeX using the `editor` agent.

## When to Invoke

When a chapter has real draft content and you want to incorporate recent working papers
not yet published in journals — especially useful for fast-moving LLM-in-finance topics.
Run after `/draft-chapter` and before `/release-chapter`.

## Inputs Required

- Chapter identifier, e.g. `06-credit-risk` — required; ask if not provided
- `TOPIC.md` — for subject area and `quality_threshold`
- `book/chapters/NN-name/chapter.tex` — must contain real content (not placeholder text)

## Steps

1. Read `TOPIC.md` to extract the book's subject area and `quality_threshold`.

2. Read `book/chapters/NN-name/chapter.tex`. If the file still contains placeholder text
   (e.g. "invoke /draft-chapter"), stop immediately and tell the user:
   > "This chapter has not been drafted yet. Run `/draft-chapter NN-name` first."

3. **Invoke the `ssrn-researcher` agent** — provide:
   - The full chapter text
   - The topic string from `TOPIC.md`
   - Instruction: find 5–10 papers posted in the last 3 years

4. Receive the agent's structured output: one `PAPER:` block per paper.
   If the output contains a `WARNING: Only N papers found` line, relay that warning to
   the user but continue.

5. Append BibTeX entries to `book/bibliography.bib`:
   - Read the existing `bibliography.bib` and collect all current entry keys.
   - For each new `@unpublished` entry from the researcher, check if its key already
     exists. If it does, append `_ssrn` to the incoming key (e.g. `Smith2024_ssrn`) and
     log: `NOTE: key Smith2024 already exists — renamed to Smith2024_ssrn.`
   - Append all new entries to the end of `bibliography.bib`.

6. **Invoke the `editor` agent** — provide:
   - The full chapter text (as last read in step 2)
   - The researcher's complete output (all `PAPER:` blocks, with any key renames applied)
   - This exact instruction:
     > "For each PAPER block, insert a `\cite{KEY}` marker at the location indicated by
     > its Section and Supports fields. Then extend the surrounding sentence, or add a
     > new sentence immediately after, to explain in one clause what this working paper
     > contributes. Do not produce bare parenthetical citations — the paper's contribution
     > must appear in the prose, not just in the cite marker."

7. Write the editor's revised chapter text to `book/chapters/NN-name/chapter.tex`.

8. Run `/audit-bibliography` to catch broken cite keys or missing required fields.
   If the audit reports any broken keys, resolve them before proceeding.

9. Run `/score-content book/chapters/NN-name/chapter.tex`.
   If any dimension is below `quality_threshold` from `TOPIC.md`, run
   `/refine-until-threshold book/chapters/NN-name/chapter.tex`.

10. Commit:
    ```
    git add book/chapters/NN-name/chapter.tex book/bibliography.bib
    git commit -m "feat(chNN): enrich with SSRN working papers"
    ```
    Replace `NN` with the chapter number.

## Expected Output

- `book/chapters/NN-name/chapter.tex` — updated with `\cite{}` markers and explanatory
  prose for each new working paper
- `book/bibliography.bib` — new `@unpublished` entries appended at the end
- Quality scores at or above `quality_threshold` in all dimensions

## Error Handling

- **Fewer than 3 papers found**: relay the researcher's WARNING, proceed with what was
  found, do not abort.
- **BibTeX key collision**: rename with `_ssrn` suffix and log the rename; do not skip
  the paper.
- **Chapter is placeholder text**: stop immediately, direct user to `/draft-chapter`.
- **`/score-content` unavailable**: skip scoring and print:
  `Run /score-content book/chapters/NN-name/chapter.tex manually when available.`
- **`/audit-bibliography` reports broken keys**: do not commit until broken keys are
  resolved. Fix or remove the offending entry, then re-run the audit.
```

- [ ] **Step 2: Verify the file against the spec**

Check each requirement from the spec:
- [ ] Purpose describes both discovery and prose integration
- [ ] Inputs: chapter identifier, TOPIC.md, chapter.tex
- [ ] Step 1: reads TOPIC.md for quality_threshold ✓
- [ ] Step 2: guards against placeholder chapter ✓
- [ ] Step 3: invokes ssrn-researcher with correct inputs (chapter text, topic, 5–10 papers, last 3 years) ✓
- [ ] Step 5: key collision detection with `_ssrn` suffix rename ✓
- [ ] Step 6: invokes editor with prose-weaving instruction (no bare cites) ✓
- [ ] Step 7: writes updated chapter back ✓
- [ ] Step 8: runs /audit-bibliography ✓
- [ ] Step 9: runs /score-content + /refine-until-threshold ✓
- [ ] Step 10: correct commit format ✓
- [ ] All 3 error handling cases from spec present ✓

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ssrn-enrich/SKILL.md
git commit -m "feat(skills): add /ssrn-enrich skill for SSRN working paper enrichment"
```

---

## Task 3: Register the skill in CLAUDE.md

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: Add `/ssrn-enrich` to the common entry points list**

In `.claude/CLAUDE.md`, find the "Common entry points" block (currently ends with
`/topic-status`). Add one line at the end of the list:

```
- `/ssrn-enrich [chNN]` — search SSRN for recent working papers and weave them into the chapter
```

The block should look like this after the edit:

```markdown
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
```

- [ ] **Step 2: Verify the edit**

Open `.claude/CLAUDE.md` and confirm:
- [ ] The new line appears at the end of the entry points list
- [ ] No other lines were accidentally changed
- [ ] The format matches the other entry points (backtick command, em-dash, description)

- [ ] **Step 3: Commit**

```bash
git add .claude/CLAUDE.md
git commit -m "chore(config): register /ssrn-enrich in CLAUDE.md entry points"
```

---

## Spec Coverage Self-Review

| Spec requirement | Covered by |
|-----------------|-----------|
| New agent `ssrn-researcher.md` | Task 1 |
| New skill `ssrn-enrich/SKILL.md` | Task 2 |
| Agent: query generation from section headers + keywords | Task 1, step 1 (What to Do §1–2) |
| Agent: WebSearch per query | Task 1, step 1 (§3) |
| Agent: WebFetch each abstract page | Task 1, step 1 (§4) |
| Agent: recency filter (last 3 years) | Task 1, step 1 (§5) |
| Agent: relevance ranking 1–5 | Task 1, step 1 (§6) |
| Agent: select top 5–10 | Task 1, step 1 (§7) |
| Agent: `PAPER:` output format with Section + Supports + BibTeX | Task 1, step 1 (Output Format) |
| Agent: `@unpublished` with note + url | Task 1, step 1 (Output Format) |
| Agent: WARNING for < 3 papers | Task 1, step 1 (Output Format) |
| Agent: scope limits (no prose, no PDF) | Task 1, step 1 (Scope Limits) |
| Skill: reads TOPIC.md | Task 2, step 1 (Skill step 1) |
| Skill: guards placeholder chapter | Task 2, step 1 (Skill step 2) |
| Skill: invokes ssrn-researcher | Task 2, step 1 (Skill step 3) |
| Skill: appends to bibliography.bib, skips duplicates | Task 2, step 1 (Skill step 5) |
| Skill: key collision → `_ssrn` suffix | Task 2, step 1 (Skill step 5) |
| Skill: invokes editor with no-bare-cite instruction | Task 2, step 1 (Skill step 6) |
| Skill: runs /audit-bibliography | Task 2, step 1 (Skill step 8) |
| Skill: runs /score-content + /refine-until-threshold | Task 2, step 1 (Skill step 9) |
| Skill: commit message format | Task 2, step 1 (Skill step 10) |
| All 3 error handling cases | Task 2, step 1 (Skill Error Handling) |
| Register in CLAUDE.md | Task 3 |
