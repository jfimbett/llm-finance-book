# Practical 4 — LLM Agents (Claude Code / Cline)

**Large Language Models in Finance · Chapter 4**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a filing question-answering agent that retrieves
text from SEC filings and answers questions grounded in what it found — the Perceive →
Reason → Act loop, tool use, and retrieval-augmented generation from the chapter, built
with the file-based agents/skills pattern.

The agent never does arithmetic or recalls figures from memory: the deterministic tools in
`tools/` do all retrieval and scoring, and the agent only chooses inputs and interprets
outputs.

## Setup

```bash
pip install -r requirements.txt   # only pytest; the tools are standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`retriever`, `analyst`, `grader`) and one command, `/ask`.

## Run

```
/ask "What is NovaCorp's customer concentration risk?"
```

The agent retrieves the most relevant chunks, writes a cited answer, grades it for
faithfulness and relevance, revises if it drifted off the source, and saves a report to
`reports/`. Everything is offline — the corpus is bundled fictional filings for
**NovaCorp Inc.** (`data/corpus/`).

You can also run the steps by hand:

```bash
python -m tools.retrieve "How did gross margin change?" -k 4 > reports/_context.json
python -m tools.grade --question "How did gross margin change?" \
       --answer "Gross margin expanded to 64%, up from 61% a year ago." --context reports/_context.json
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Retrieve relevant chunks | `retriever` | `tools/retrieve.py` (TF-IDF cosine) |
| Write a grounded, cited answer | `analyst` | — (reads `reports/_context.json`) |
| Score faithfulness & relevance | `grader` | `tools/grade.py` |

## Things to try

- Ask something the filings **don't** cover (e.g. "What was net income?"). The agent must
  answer "Not answerable from the available filings" instead of guessing.
- Drop `-k` to 1 and watch relevance fall — too little context starves the answer.
- Change the chunk `size`/`overlap` in `tools/chunk.py` and re-run the tests; see how
  retrieval quality shifts.
- Add a fourth document to `data/corpus/` and ask a question only it can answer.
- Make the `analyst` cite a number that isn't in the context, then run the grader — watch
  faithfulness drop and the loop send it back.

## Tests

```bash
python -m pytest -q        # fully offline
```
