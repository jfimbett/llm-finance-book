# Practical 8 — Domain-Specific Financial LLMs (Claude Code / Cline)

**Large Language Models in Finance · Chapter 8**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a general-vs-domain comparison agent: it runs the
same finance sentiment task through a general-purpose classifier and a finance-domain
classifier, scores both against gold labels, and reports which wins and why — the
chapter's claim that domain adaptation helps on financial text.

The agent never classifies a sentence or computes an accuracy from memory: the
deterministic tools in `tools/` do all classification and scoring, and the agent only
chooses inputs and interprets outputs.

## Setup

```bash
pip install -r requirements.txt   # NumPy and pytest; the tools are standard-library + NumPy
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`generalist`, `specialist`, `adjudicator`) and one command,
`/compare`.

## Run

```
/compare
```

The agent runs both classifiers over the bundled labelled finance sentences, scores each
against the gold labels, names the winner and the margin, explains the gap with the
deciding finance terms, and saves a report to `reports/`. Everything is offline — the
dataset and both lexicons are bundled under `data/`.

You can also run the steps by hand:

```bash
python -m tools.general            # general-purpose accuracy + per-sentence results
python -m tools.domain             # finance-domain accuracy + per-sentence results
python -m tools.compare            # both accuracies, the winner, and the deciding terms
python -m tools.domain "Revenue beat guidance and margins expanded."   # one sentence
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Score the general-purpose baseline | `generalist` | `tools/general.py` (general lexicon) |
| Score the finance-domain model | `specialist` | `tools/domain.py` (finance lexicon) |
| Adjudicate: accuracies, winner, why | `adjudicator` | `tools/compare.py` |

## Why the domain model wins

The two lexicons disagree exactly on the words that carry finance meaning:

- `beat` — a beating (negative) in general English, *beat estimates* (positive) in finance.
- `headwinds`, `impairment`, `accretive` — unseen by the general lexicon, scored correctly
  by the domain one.
- `liability`, `covenant` — emotionally loaded in general English, neutral balance-sheet
  terms in finance.

`tools/compare.py` lists every sentence where these terms flip the verdict.

## Things to try

- Run `python -m tools.general "The company beat consensus estimates."` and the same on
  `tools.domain`. The labels disagree on one word — `beat`.
- Add the missing finance terms (`headwind`, `impairment`, `accretive`) to
  `data/lexicon_general.json` and watch the general accuracy climb — domain adaptation,
  done by hand.
- Add a new labelled sentence to `data/sentences.jsonl` whose verdict hinges on a finance
  term, then re-run `/compare`.
- Flip a domain score to the wrong sign and re-run the tests; see the comparison gate fail.

## Tests

```bash
python -m pytest -q        # fully offline
```
