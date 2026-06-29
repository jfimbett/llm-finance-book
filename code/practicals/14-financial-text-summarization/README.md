# Practical 14 — Financial Text Summarization and Information Extraction (Claude Code / Cline)

**Large Language Models in Finance · Chapter 14**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a summarize-and-extract agent: it pulls structured
fields from a bundled filing, writes a grounded summary that cites each field, and runs a
faithfulness check — extraction, grounding, and scoring from the chapter, built with the
file-based agents/skills pattern.

The agent never reads a figure off the page or recalls one from memory: the deterministic
tools in `tools/` do all extraction and scoring, and the agent only chooses inputs and
interprets outputs.

## Setup

```bash
pip install -r requirements.txt   # only pytest; the tools are standard-library + numpy-free
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`extractor`, `summarizer`, `grader`) and one command,
`/summarize`.

## Run

```
/summarize
```

The agent extracts the named fields, writes a summary that cites each one, grades it for
faithfulness and figure coverage, revises if it stated a figure not in the filing, and
saves a report to `reports/`. Everything is offline — the source is a bundled fictional
earnings release for **Orion Dynamics Inc.** (`data/filings/`).

You can also run the steps by hand:

```bash
python -m tools.extract                                  # JSON fields + source spans
python -m tools.grade --summary "Revenue was \$1.46 billion; gross margin 58%; \
       diluted EPS \$1.27; FY guidance \$5.90 billion to \$6.10 billion."
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Extract named fields + source spans | `extractor` | `tools/extract.py` (regex → schema-validated dict) |
| Write a grounded summary citing fields | `summarizer` | — (reads `reports/_fields.json`) |
| Score faithfulness & figure coverage | `grader` | `tools/grade.py` (IDF-weighted + literal figure check) |

## Extracted fields

`tools/extract.py` finds four fields, each anchored to its label and validated against a
small JSON-schema-style contract (`revenue` and `guidance` are strings; `gross_margin` and
`eps` are numbers with range checks):

| Field | Example value | Source span |
|-------|---------------|-------------|
| `revenue` | `$1.46 billion` | "Total revenue was $1.46 billion" |
| `gross_margin` | `58.0` | "Gross margin was 58%" |
| `eps` | `1.27` | "Diluted earnings per share were $1.27" |
| `guidance` | `$5.90 billion to $6.10 billion` | "revenue guidance to a range of ..." |

## Things to try

- Make the `summarizer` state a figure that is **not** in `reports/_fields.json` (e.g.
  revenue of $2.30 billion) and re-grade — `figure_coverage` falls below 1.0 and the loop
  sends it back.
- Corrupt the extraction (drop a field, or set `gross_margin` to a string) and run
  `tools/extract.validate` — schema validation rejects it before any summary is written.
- Reword a figure's label in `data/filings/` and re-run the tests; watch the anchored
  regex stop matching, so the field goes missing rather than grabbing the wrong number.
- Add a second filing to `data/filings/` and summarise across both.

## Tests

```bash
python -m pytest -q        # fully offline
```
