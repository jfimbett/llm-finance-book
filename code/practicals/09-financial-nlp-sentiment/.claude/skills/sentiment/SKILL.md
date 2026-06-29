---
name: sentiment
description: Score the bundled headlines, aggregate them into a daily signal, and write a grounded summary. Usage /sentiment [YYYY-MM-DD]
---

# /sentiment [date]

Run the score -> aggregate -> summarize pipeline and save a report. With no date,
process every bundled day; with a date, process just that one.

1. **Aggregate** (aggregator agent): score and group all headlines.
   ```bash
   python -m tools.aggregate > reports/_signal.json
   # or for one day:
   python -m tools.aggregate --date 2024-02-13 > reports/_signal.json
   ```
2. **Read** `reports/_signal.json`: each date has a `mean`, a `label`, a `count`, and the
   `item_ids` that fed it; `headlines` holds each scored item.
3. **Spot-check** (scorer agent, optional): for any surprising item, run
   `python -m tools.lexicon "<headline>"` to see which words and modifiers moved it.
4. **Summarize** (summarizer agent): write a grounded summary that states each day's
   `mean` and `label` verbatim and cites the headlines that drove it by `id`. Never state
   a polarity or mean that is not in `reports/_signal.json`.
5. **Save** to `reports/<date>.md` (or `reports/signal.md` for all dates):
   - the daily mean and label,
   - the 2–3 headlines that drove it, each with its id and polarity,
   - a one-line caveat where a day rests on few headlines.

Try these to start:
- `/sentiment` — all three days; expect a bullish, a bearish and a neutral day.
- `/sentiment 2024-02-13` — the bearish day; see which headline weighed most.
- `/sentiment 2024-02-14` — a near-zero day where one negated headline ("does not beat")
  cancels a positive one; a good test of whether the summary respects the tool's signs.
