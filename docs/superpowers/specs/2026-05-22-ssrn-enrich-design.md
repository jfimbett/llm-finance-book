# Design Spec — `/ssrn-enrich` Skill

**Date:** 2026-05-22
**Status:** Approved

---

## Overview

A new skill that searches SSRN for recent working papers relevant to a given book chapter, then integrates the best finds directly into the chapter's LaTeX text with properly woven prose. Targets the fast-moving LLM-in-finance literature that has not yet appeared in journals.

---

## New Files

| Path | Purpose |
|------|---------|
| `.claude/skills/ssrn-enrich/SKILL.md` | The skill workflow |
| `.claude/agents/ssrn-researcher.md` | New agent: SSRN discovery and ranking |

---

## Architecture

Two-agent pipeline matching the project's single-purpose agent rule:

1. **`ssrn-researcher` agent** — discovery only. Takes chapter text + topic, formulates search queries, fetches SSRN metadata, ranks papers by relevance, outputs structured BibTeX + placement notes.
2. **`editor` agent** (existing) — integration only. Takes chapter text + researcher output, inserts `\cite{}` markers, and extends surrounding prose to explain each paper's contribution.

---

## Skill Workflow — `/ssrn-enrich [chNN-name]`

### Inputs
- Chapter identifier (e.g. `06-credit-risk`) — required; prompt if not provided
- `TOPIC.md` — for subject area and `quality_threshold`
- `book/chapters/NN-name/chapter.tex` — the chapter to enrich

### Steps

1. Read `TOPIC.md` for subject area and `quality_threshold`.
2. Read `book/chapters/NN-name/chapter.tex` to understand current content, section headers, and existing citations.
3. **Invoke `ssrn-researcher` agent** with:
   - Full chapter text
   - Book topic from `TOPIC.md`
   - Target: 5–10 papers, posted within the last 3 years
4. Receive from agent: a structured list of papers (BibTeX entries + placement notes).
5. Append new `@unpublished` BibTeX entries to `book/bibliography.bib`. Skip any whose key already exists.
6. **Invoke `editor` agent** with:
   - Full chapter text
   - Researcher output (BibTeX keys + placement notes)
   - Instruction: insert `\cite{}` markers at indicated locations and extend surrounding sentences to explain each paper's contribution — no bare parenthetical cites
7. Write updated chapter to `book/chapters/NN-name/chapter.tex`.
8. Run `/audit-bibliography` to verify no broken cite keys.
9. Run `/score-content book/chapters/NN-name/chapter.tex`. If any dimension is below `quality_threshold`, run `/refine-until-threshold`.
10. Commit: `feat(chNN): enrich with SSRN working papers`

### Error handling
- If fewer than 3 papers are found on SSRN: warn the user and proceed with what was found rather than failing.
- If a BibTeX key collision is detected: append `_ssrn` suffix to the new key and note it.
- If `/score-content` is unavailable: skip and remind user to run manually.

---

## `ssrn-researcher` Agent Design

### Inputs
- Chapter text (full `.tex` content)
- Topic string from `TOPIC.md`

### Process

1. **Query generation**: extract section titles and 3–5 domain keywords from the chapter. Combine with book topic to produce 3–5 targeted search strings, e.g.:
   - `"LLM credit risk working paper site:ssrn.com"`
   - `"large language model loan default prediction site:ssrn.com after:2022"`
2. **Discovery**: `WebSearch` each query; collect SSRN abstract URLs from results.
3. **Metadata fetch**: `WebFetch` each abstract page (`https://papers.ssrn.com/sol3/papers.cfm?abstract_id=XXXXXX`) to extract: title, authors, date posted, abstract, SSRN ID.
4. **Recency filter**: discard papers posted before `(current_year - 3)`.
5. **Relevance ranking**: score each paper against the chapter's specific sections. Identify which section it supports and what claim or gap it fills.
6. **Selection**: return top 5–10 papers by relevance score.

### Output format (one block per paper)

```
PAPER: [ShortKey2024]
Section: 3.2 — Credit Scoring Models
Supports: claim that LLMs outperform gradient boosting on unstructured text inputs
BibTeX:
@unpublished{ShortKey2024,
  author = {Last, First and Last2, First2},
  title  = {Title Here},
  note   = {Working Paper, SSRN \#1234567},
  year   = {2024},
  url    = {https://ssrn.com/abstract=1234567}
}
```

### Scope limits
- Does not verify that the paper's abstract matches its actual content.
- Does not fetch full PDF text — abstract only.
- Does not rewrite prose — placement notes are for the editor agent.

---

## BibTeX Convention for Working Papers

Use `@unpublished` with:
- `note = {Working Paper, SSRN \#ID}`
- `url` field pointing to the abstract page
- Key format: `AuthorYYYY` or `AuthorKeywordYYYY` if disambiguation needed

---

## Quality Assurance

- `/audit-bibliography` runs after bib append to catch key collisions or missing fields.
- `/score-content` + `/refine-until-threshold` ensure the prose integration doesn't degrade chapter quality below `quality_threshold = 8`.
