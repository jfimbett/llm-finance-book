<!-- Cline workflow — save as .clinerules/workflows/<name>.md. -->
<!-- This is Cline's analogue of a Claude skill. Invoke it from the Cline chat by typing /<name>. -->

# /<name> "<arg>"

One line on what this workflow does.

## Steps
1. Run: `python -m tools.<something> "<arg>"`
2. Read the output and draft the result, citing sources for every figure.
3. Check the gate condition; if it fails, revise or re-run step 1 with a better input.
4. Save the result to `reports/<slug>.md`.

You can reference files with `@`, run shell commands, and chain tools — a workflow is just an
ordered, repeatable recipe that Cline follows step by step, the same idea as a Claude skill.
