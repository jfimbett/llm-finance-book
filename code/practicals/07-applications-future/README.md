# Practical 7 — Finance Research-Brief Agent (Claude Code / Cline)

**Large Language Models in Finance · Chapter 7 — Other Applications and Future Trends**

This practical is an **agentic project**, not a notebook. You open this folder in **Claude
Code** or **Cline** and drive a research-brief agent: it routes a finance question to the
right evidence source, gathers grounded evidence, and writes a short cited brief — the
route → gather → write pattern that sits behind many of the "future" finance applications in
the chapter (research assistants, disclosure monitors, automated analyst notes).

The agent never does arithmetic or recalls figures from memory: the deterministic tools in
`tools/` do all routing, retrieval, and figure lookup, and the agent only chooses inputs and
interprets outputs.

## Setup

```bash
pip install -r requirements.txt   # pytest + numpy; the tools are otherwise standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`router`, `researcher`, `brief-writer`) and one command,
`/brief`.

## Run

```
/brief "What was Meridian's gross margin in fiscal 2025?"
```

The agent routes the question (here, to the metrics table), gathers evidence, writes a cited
brief, and saves it to `reports/`. Everything is offline — the evidence is bundled fictional
material for **Meridian Robotics Inc.** (`data/`).

You can also run the steps by hand:

```bash
python -m tools.route "What partnership did Meridian recently announce?"
python -m tools.retrieve "warehouse partnership" --source news -k 2 > reports/_evidence.json
python -m tools.metrics "gross margin"
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Route the question to metrics / filings / news | `router` | `tools/route.py` (keyword rules) |
| Gather evidence (figure lookup or snippet retrieval) | `researcher` | `tools/metrics.py`, `tools/retrieve.py` (TF-IDF cosine) |
| Write a grounded, cited brief | `brief-writer` | — (reads `reports/_evidence.json`) |

## Things to try

- Ask for a figure that isn't in the table (e.g. "What is Meridian's dividend yield?"). The
  metrics tool returns `found: false` and the agent must say "Not answerable from the
  available sources" instead of guessing.
- Ask a two-part question — "What was gross margin, and why did it improve?" — and watch the
  agent route to `metrics` for the number and `filings` for the explanation, citing both.
- Phrase a metric question as discussion ("Tell me about the company's risks") and inspect
  `tools.route` output: the `matched` terms show exactly why it routed to `filings`.
- Add a new row to `data/metrics.csv` and a matching alias in `tools/metrics.py`, then ask
  for it.
- Add a fourth snippet under `data/news/` and ask a question only it can answer.

## Tests

```bash
python -m pytest -q        # fully offline
```

Covers routing (figure questions → `metrics`, disclosure → `filings`, events → `news`),
retrieval (the on-topic snippet ranks first, source filtering holds), and metrics lookup
(exact keys, aliases, and unknown-metric handling).
