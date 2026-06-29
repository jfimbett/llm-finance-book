# Capability templates — Claude Code & Cline

Copy-ready skeletons for the four ways you extend an agentic coding assistant. Nothing here is
wired in by default; each file says where it goes. The live, working versions for this practical
are the filing-Q&A agents in `.claude/` — these templates are the blank forms behind them.

| Capability | Claude Code — copy to | Cline — copy to |
|------------|------------------------|------------------|
| **Agent** (a persona) | `.claude/agents/<name>.md` ← `claude/agent.md` | `.clinerules` or `.clinerules/<name>.md` ← `cline/agent.md` |
| **Skill** (a `/command`) | `.claude/skills/<name>/SKILL.md` ← `claude/skill/SKILL.md` | `.clinerules/workflows/<name>.md` ← `cline/workflow.md` |
| **Tool** (a new action) | MCP server in `.mcp.json`, or any CLI invoked via `Bash` | MCP server in `cline_mcp_settings.json` |
| **Hook** (an event callback) | `.claude/settings.json` + a script in `.claude/hooks/` | none native — see `cline/git-hooks-README.md` |

## Standard tools — already there
You rarely write a tool from scratch. Both assistants ship `Read`, `Edit`/`Write`, `Grep`,
`Glob`, and `Bash`. A **custom** tool (MCP) is only for what the environment can't already do:
a pricing API, an internal database, a deterministic valuation engine.

## The two hooks in this practical (Claude Code)
- `../.claude/hooks/log-interaction.sh` — appends one line per turn to `logs/llm-interactions.log`.
- `../.claude/hooks/timed-commit.sh` — commits the tree if >15 min since the last commit.

Both are wired in `../.claude/settings.json`. Try them: make an edit and end your turn, then watch
`logs/llm-interactions.log` grow; keep working past 15 minutes and watch a safety commit appear.
For the Cline equivalents, see `cline/git-hooks-README.md`.
