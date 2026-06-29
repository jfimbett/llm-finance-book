# Hooks in Cline — the portable fallback

Claude Code has a native hook engine (`.claude/settings.json` → scripts on `PostToolUse`,
`Stop`, `UserPromptSubmit`, …). **Cline has no equivalent event system.** To get the same two
guarantees from this practical under Cline, push the guardrail down to a layer that *does* run
on its own — git, the OS scheduler, or an MCP proxy.

## 1 · Timed safety commit → a watch loop or cron
`.claude/hooks/timed-commit.sh` is tool-agnostic (it reads no Claude-specific input). Run it
beside Cline:

```bash
# In a spare terminal while you work — commits the tree if >15 min since the last commit.
while true; do bash .claude/hooks/timed-commit.sh; sleep 300; done
```

Or schedule the same script with cron / launchd every few minutes against the repo. A git
`post-commit` hook is the *wrong* trigger here — it only fires when you already commit.

## 2 · Log every interaction → MCP wrapper or task history
Cline can't shell out on every model turn, so raw-prompt logging isn't native. Closest options:

- **Cline task history** — every task is already persisted; export it for the audit trail.
- **MCP logging server** — wrap your tools behind an MCP server (registered in
  `cline_mcp_settings.json`) that logs each call. This captures *tool* interactions, not prompts.

## The teaching point
A hook is a property of the **harness**, not the model. When the harness doesn't offer one,
you implement the same intent one layer down. Same guarantee, different plumbing.
