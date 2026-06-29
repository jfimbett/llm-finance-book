---
name: ask
description: Answer a question about the bundled NovaCorp filings, grounded and graded. Usage /ask "<question>"
---

# /ask "<question>"

Run the full Perceive → Reason → Act → Check loop and save a report.

1. **Retrieve** (retriever agent):
   `python -m tools.retrieve "<question>" -k 4 > reports/_context.json`
2. **Answer** (analyst agent): write a grounded answer from `reports/_context.json`,
   citing chunk ids for every figure.
3. **Grade** (grader agent):
   `python -m tools.grade --question "<question>" --answer "<answer>" --context reports/_context.json`
4. **Gate**: if `faithfulness < 0.7` revise the answer (or declare it unanswerable); if
   `relevance < 0.5` re-retrieve with a better query. Loop at most 3 times.
5. **Save** to `reports/<slug>.md`:
   - the question,
   - the final answer with citations,
   - the two scores,
   - the chunk ids used.

Try these to start:
- `/ask "What is NovaCorp's customer concentration risk?"`
- `/ask "How did gross margin change year over year, and why?"`
- `/ask "What was NovaCorp's net income?"`  ← not in the corpus; the agent must say so.
