# Sentiment-Signal Agent — Chapter 9 Practical

You turn a set of dated financial headlines into a daily sentiment signal, grounded
**only** in what the deterministic tools score.

This repo is the file-based agent pattern from Chapter 9: capabilities live as markdown
artifacts under `.claude/`, and every polarity score and daily mean is computed by the
tools in `tools/`. You choose which headlines to look at and interpret the signal — you
never estimate, average, or recall a number yourself.

## The pipeline (score → aggregate → summarize)

1. **Aggregate** all headlines into a daily signal and save it:
   ```bash
   python -m tools.aggregate > reports/_signal.json          # all dates
   python -m tools.aggregate --date 2024-02-13 > reports/_signal.json
   ```
2. **Read** `reports/_signal.json`. Each date has a `mean`, a `label`
   (bullish / bearish / neutral), a `count`, and the `item_ids` behind it; `headlines`
   holds each scored item with its `polarity` and the words that drove it.
3. **Spot-check** any single headline:
   ```bash
   python -m tools.lexicon "NovaCorp warns of weak demand and announces layoffs"
   ```
4. **Summarize.** Write the day's `mean` and `label` verbatim and cite the 2–3 headlines
   that moved it by `id` (e.g. `h006`, polarity -1.0).
5. **Save** the summary to `reports/<date>.md`.

## Rules

- Never state a polarity or mean that is not in `reports/_signal.json` (or a fresh
  `tools.lexicon` run). No outside knowledge of the company.
- A day's label is whatever the tool assigned at the 0.15 threshold; do not relabel it.
- For multi-day or multi-headline work, delegate to the sub-agents in `.claude/agents/`
  (`scorer`, `aggregator`, `summarizer`) rather than doing everything in one turn.

## Data

Bundled in `data/`: `headlines.csv` — nine fictional headlines for **NovaCorp Inc.**
across three dates — and `lexicon.json`, a small Loughran-McDonald-style finance polarity
lexicon (positive/negative words, negators, intensifiers). Everything runs offline; no
network or API key is required. Tests: `python -m pytest -q`.
