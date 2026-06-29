---
name: my-skill
description: One sentence on what this command does and when to invoke it. Usage /my-skill "<arg>"
---

# /my-skill "<arg>"

One line on the workflow this skill runs end to end.

## Steps
1. **Retrieve / prepare** — what to do; which tool or sub-agent to use.
   `python -m tools.something "<arg>"`
2. **Act** — produce the draft result, citing sources for every figure.
3. **Gate / check** — the condition that decides success vs. retry (e.g. a score threshold);
   loop at most N times.
4. **Save** — where the result goes, e.g. `reports/<slug>.md`.

## Try these
- `/my-skill "a normal example"`
- `/my-skill "an example that should fail gracefully"`

<!-- Save this as .claude/skills/<name>/SKILL.md (the folder name becomes the command).
     Typing /<name> in Claude Code runs these steps in order. Skills may call other skills
     and delegate to the agents in .claude/agents/. -->
