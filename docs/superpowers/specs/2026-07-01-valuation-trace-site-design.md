# Valuation run-trace static site — design

**Date:** 2026-07-01
**Location:** `code/practicals/05-business-valuation/`
**Status:** Approved (design), pending implementation plan

## Goal

Teach students how the `/valuation` agent pipeline actually works by producing,
after every run, a **single self-contained HTML file** that replays the real
trace of that run: the prompt, every agent, when it ran, every tool call with its
real command and captured output, and every hook firing.

Audience: students learning multi-agent orchestration in Claude Code. The site is
a faithful record of one run (not an idealized diagram), enriched with light
static annotations that explain what an agent / tool / hook *is*.

## Non-goals (YAGNI)

- No live/streaming view, no local server.
- No per-run history browser, no diffing between runs.
- No multi-file site — one static `.html` per run.
- No hand-authored, run-invariant architecture diagram — the trace is the teacher.

## Key decisions (from brainstorming)

1. **Data source:** the REAL captured trace of an actual run.
2. **Capture method:** Claude Code **hooks** log events. Hooks both capture the
   trace AND serve as the featured teaching example — the lesson's subject
   captures the lesson's data.
3. **Generation:** automatic, as a final step of the `/valuation` skill.
4. **Output form:** one self-contained HTML file (inline CSS/JS, no build step,
   double-click to open), matching the repo's existing html-slides ethos.
5. **Centerpiece:** a **swimlane timeline** (one lane per agent; sequential
   edgar-analyst, then the 3 parallel lanes, then reconciliation).
6. **Detail depth:** compact by default; every tool block and agent expands to
   full command / args / captured stdout / dispatch prompt.

## Architecture

Three units, each independently testable:

### Unit A — `tools/trace_hook.py` (capture)

A hook handler registered in `.claude/settings.json`. Reads a Claude Code hook
payload as JSON on stdin, normalizes it to one event, and appends it as a single
JSON line to `reports/trace/<session_id>.jsonl`.

Registered on these events:

| Hook event        | Records |
|-------------------|---------|
| `UserPromptSubmit`| Run start. If the prompt begins with `/valuation`, truncate/open a fresh trace for this `session_id` and create an "active" sentinel file. |
| `PreToolUse`      | A tool call begins: `tool_name`, timestamp, and args — for `Bash` the command, for `Task` the `subagent_type` + dispatch prompt. |
| `PostToolUse`     | A tool finished: captured `tool_response` (Bash stdout/stderr/JSON), end timestamp. |
| `SubagentStop`    | An agent lane finished. |
| `Stop`            | Run complete: clear the sentinel. |

**Gating:** every hook invocation first checks for the active sentinel; if absent
(i.e. not inside a `/valuation` run) it exits immediately writing nothing. This
keeps traces clean and avoids noise on unrelated Claude Code activity.

**Sentinel + trace paths:** keyed by `session_id` (present in every hook payload)
so concurrent/interleaved sessions don't clobber each other. The active sentinel
also stores the `session_id` of the current valuation run so the builder can find
the right trace.

**Normalized event shape** (one per line):

```json
{
  "ts": 1719830400.123,
  "event": "PreToolUse|PostToolUse|UserPromptSubmit|SubagentStop|Stop",
  "session_id": "…",
  "transcript_path": "…",
  "tool_name": "Bash|Task|Read|…",
  "lane": "edgar|dcf|comps|qualitative|reconciliation|orchestrator",
  "command": "python tools/montecarlo_dcf.py --cik …",
  "subagent_type": "dcf-analyst",
  "prompt": "…dispatch prompt (Task only)…",
  "output": "…captured stdout/JSON (PostToolUse only)…"
}
```

`trace_hook.py` records the raw fields; **lane attribution can happen either here
or in the builder** (see Attribution). Timestamps come from the hook process's
real clock at invocation.

### Unit B — `tools/build_trace_site.py` (render)

Reads the newest (or session-specified) `reports/trace/<session_id>.jsonl`,
groups events into agents → tool calls → outputs plus a hook-event rail, computes
per-lane start/end for the timeline, and renders a single HTML file via a Python
string template (inline CSS/JS). Writes `reports/<TICKER>-<date>.html`.

Pure Python, offline, deterministic. No JS build step, no external assets.

### Unit C — `.claude/settings.json` + `SKILL.md` (wiring)

- `settings.json`: add the `hooks` block registering `trace_hook.py` on the five
  events, and add `python tools/build_trace_site.py` to the Bash allow-list.
- `SKILL.md`: add a final step (after the report) that runs
  `python tools/build_trace_site.py --ticker <TICKER> --date <date>` and prints
  the resulting `.html` path to the user.

## Attribution (tool call → swimlane)

Primary signal: **tool → lane mapping** (robust because each Python tool belongs
to exactly one lane):

- `edgar_fetch.py`, `financials.py` → `edgar`
- `montecarlo_dcf.py` → `dcf`
- `comps.py`, `embeddings.py` → `comps`
- `reconcile.py`, `market_price.py` → `reconciliation`
- qualitative-analyst reads `narrative.txt` (a `Read` tool call, no Bash) → `qualitative`
- `build_trace_site.py`, and top-level `Task` dispatches → `orchestrator`

Secondary signal: **`transcript_path` grouping** disambiguates the 3 concurrent
lanes (each subagent has its own transcript path in the hook payload) and orders
events within a lane. Agent dispatch identity + dispatch prompt come from the
`Task` `PreToolUse` payloads (`subagent_type`, `prompt`).

## The page

- **Header:** the exact `/valuation <ARG>` prompt; the final headline
  (`<TICKER> fair value ≈ $<median>/share (P10–P90 …); market $<price> (Δ …)`);
  a link to the `.md` report.
- **Swimlane timeline (hero):** horizontal time axis; one lane per agent —
  `edgar-analyst` (sequential) → `dcf` / `comps` / `qualitative` (overlapping
  bars showing real parallelism) → `reconciliation-analyst`. Tool calls render as
  blocks positioned by their real start/end. Hook firings render as tick marks on
  a dedicated "hooks" rail so students see hooks firing between tool calls.
- **Expandable detail:** clicking a tool block expands the exact command, args,
  and captured stdout/JSON; clicking an agent expands its dispatch prompt. All
  content is inlined so the file is a complete, shareable record of the run.
- **Legend:** a short static key explaining what an agent / tool / hook is —
  light touch, so the real trace remains the teacher.

## Testing (all offline, matching repo ethos)

- `tests/test_trace_hook.py`: feed sample hook-payload JSON on stdin, assert the
  appended normalized line shape; assert gating (no sentinel → no write).
- `tests/test_build_trace_site.py`: feed a fixture `trace.jsonl`, assert the
  rendered HTML contains the expected lanes, tool blocks, hook markers, and
  headline.
- `tests/fixtures/trace_sample.jsonl`: a small hand-authored trace covering the
  edgar → 3 parallel lanes → reconciliation shape.

## File manifest

New:
- `tools/trace_hook.py`
- `tools/build_trace_site.py`
- `tests/test_trace_hook.py`
- `tests/test_build_trace_site.py`
- `tests/fixtures/trace_sample.jsonl`

Edit:
- `.claude/settings.json` (hooks block + allow-list entry)
- `.claude/skills/valuation/SKILL.md` (final site-build step)
- `.gitignore` (ignore `reports/trace/*.jsonl` and the active sentinel)

## Open risks

- Hook payload field names/availability for `Task`/`SubagentStop` must be
  verified against the running Claude Code version during implementation; the
  builder should degrade gracefully if a field is missing (e.g. fall back to
  tool→lane mapping when `subagent_type` is absent).
- Concurrent lanes may interleave `PreToolUse`/`PostToolUse` in the trace file;
  pairing is by `(transcript_path, tool_name, command)` and nearest-in-time.
