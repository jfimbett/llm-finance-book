# Practical 9 — Financial NLP and Sentiment Analysis (Claude Code / Cline)

**Large Language Models in Finance · Chapter 9**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a sentiment-signal agent that scores a set of dated
financial headlines with a deterministic finance lexicon, aggregates them into a daily
signal, and writes a grounded summary citing the scored items — the lexicon-based
sentiment pipeline from the chapter, built with the file-based agents/skills pattern.

The agent never assigns a polarity or averages a day from memory: the tools in `tools/`
do all scoring and aggregation, and the agent only chooses inputs and interprets outputs.

## Setup

```bash
pip install -r requirements.txt   # numpy + pytest; the tools are otherwise standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`scorer`, `aggregator`, `summarizer`) and one command,
`/sentiment`.

## Run

```
/sentiment            # all three bundled days
/sentiment 2024-02-13 # just the bearish day
```

The agent scores each headline, aggregates the day's mean polarity into a bullish /
bearish / neutral label, writes a cited summary, and saves a report to `reports/`.
Everything is offline — the headlines are bundled fictional news for **NovaCorp Inc.**
(`data/headlines.csv`) and the lexicon is bundled (`data/lexicon.json`).

You can also run the steps by hand:

```bash
python -m tools.lexicon "NovaCorp beats estimates on strong cloud growth"
python -m tools.aggregate > reports/_signal.json
python -m tools.aggregate --date 2024-02-13
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Score one headline's net polarity | `scorer` | `tools/lexicon.py` (lexicon + negation/intensity) |
| Aggregate headlines into a daily signal | `aggregator` | `tools/aggregate.py` (NumPy daily mean) |
| Write a grounded, cited summary | `summarizer` | — (reads `reports/_signal.json`) |

`tools/lexicon.py` scores text as the signed sum of polarity words divided by the number
of sentiment words: a negator in the prior three words flips a word's sign ("did not beat"
→ negative) and an intensifier in the prior two words amplifies it ("strong gains" >
"gains"). `tools/aggregate.py` means those polarities by date and labels each day against a
±0.15 threshold.

## Things to try

- Run `/sentiment 2024-02-14` — one negated headline ("does not beat") cancels a positive
  one, so the day nets to neutral. Check the summary respects the tool's signs.
- Add a headline to `data/headlines.csv` on an existing date and watch its daily mean and
  label move.
- Add a word to `data/lexicon.json` (e.g. put "guidance" in `positive`) and re-run; see how
  many headlines change sign.
- Drop the threshold in `tools/aggregate.py` toward 0 and watch neutral days flip to
  bullish/bearish — a lesson in how a labelling cutoff manufactures signal.
- Score a sarcastic or hedged headline by hand with `tools.lexicon` and see where a
  bag-of-words lexicon misreads it.

## Tests

```bash
python -m pytest -q        # fully offline
```
