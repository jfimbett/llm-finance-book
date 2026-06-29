<!-- Cline agent. Save as .clinerules (single file) OR .clinerules/<name>.md (directory form). -->
<!-- The same content also works as AGENTS.md, so it carries to Cursor and other AGENTS.md runners. -->

# <ROLE> — Cline rules

You are <ROLE>. <One sentence on the single job this agent does.>

## How to work
The deterministic tools in `tools/` do all arithmetic and retrieval; you choose the inputs and
interpret the outputs, and never compute or recall a number yourself.

For every task:
1. `python -m tools.<something> "<input>"`
2. Write the result using only facts the tools produced; cite the source of every figure.
3. <gate / check — e.g. if a quality score is too low, revise or re-run step 1>.
4. Save the result to `reports/<slug>.md`.

## Hard rules
- Never state a number a tool did not produce.
- If the inputs don't support an answer, say so — do not guess.
- Run tests with: `python -m pytest -q`
