---
name: brief
description: Route a research question, gather grounded evidence, and write a cited brief. Usage /brief "<question>"
---

# /brief "<question>"

Run the route → gather → write loop and save a cited research brief.

1. **Route** (router agent):
   `python -m tools.route "<question>"` → note the `route`.
2. **Gather** (researcher agent), based on the route:
   - `metrics`: `python -m tools.metrics "<metric name>" > reports/_evidence.json`
   - `filings` / `news`: `python -m tools.retrieve "<question>" --source <route> -k 3 > reports/_evidence.json`
3. **Write** (brief-writer agent): read `reports/_evidence.json` and write a brief that cites
   a source for every claim. If the evidence does not answer the question (metrics
   `found: false`, or no on-topic snippet), write "Not answerable from the available sources."
4. **Two-part questions**: if the question asks for a figure *and* the reason behind it, gather
   twice — a `metrics` lookup for the figure and a `filings` retrieval for the explanation — and
   cite both.
5. **Save** to `reports/<slug>.md`:
   - the question,
   - the brief with citations,
   - the evidence used (metric row or snippet ids).

Try these to start:
- `/brief "What was Meridian's gross margin in fiscal 2025?"`  ← routes to metrics
- `/brief "What supply chain risks does Meridian disclose?"`   ← routes to filings
- `/brief "What partnership did Meridian recently announce?"`  ← routes to news
- `/brief "What is Meridian's dividend yield?"`  ← not in the table; must say so.
