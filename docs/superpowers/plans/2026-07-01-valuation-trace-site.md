# Valuation Run-Trace Static Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After `/valuation <ticker|cik>`, automatically produce a single self-contained HTML file that replays the real run — every agent, when it ran, every tool call with its actual command and captured output, and every hook firing — as a swimlane timeline with expandable detail.

**Architecture:** Claude Code hooks call `tools/trace_hook.py`, which (gated on an active-run sentinel created by the valuation skill) appends normalized JSON-line events to `reports/trace/run-<epoch>.jsonl`. As its final step the skill runs `tools/build_trace_site.py`, which parses the newest trace into an agents→tools→outputs model plus a hook rail and renders one inline-CSS/JS HTML file to `reports/<TICKER>-<date>.html`.

**Tech Stack:** Python 3.9 (stdlib only: `argparse`, `json`, `sys`, `time`, `pathlib`, `html`), pytest, Claude Code hooks + skills.

## Global Constraints

- Location for all code: `code/practicals/05-business-valuation/` (all paths below are relative to it unless noted).
- Tools import shared helpers from `_common` (tests put `tools/` on `sys.path` via `tests/conftest.py`); test files import tool modules directly by name (e.g. `import trace_hook`).
- Stdlib only — no new dependencies in `requirements.txt`.
- All tests must be fully offline and deterministic (no network, no wall-clock assertions — pass `ts` explicitly to pure functions).
- A hook MUST NEVER break a run: `trace_hook.py`'s `main()` swallows all exceptions and always exits 0.
- `reports/` is already git-ignored — do NOT add `.gitignore` entries and do NOT commit generated `.html`/trace/sentinel files.
- Follow the existing tool shape: module-level pure functions + a thin `main(argv=None)` CLI; mirror `tools/reconcile.py` style.
- Lane vocabulary is fixed: `edgar`, `dcf`, `comps`, `qualitative`, `reconciliation`, `orchestrator`.

---

## File Structure

New files:
- `tools/trace_hook.py` — hook handler + `--start`/`--stop` CLI; classifies and appends events.
- `tools/build_trace_site.py` — parses a trace file into a timeline model and renders the HTML.
- `tests/test_trace_hook.py` — unit tests for classification, normalization, gating, start/stop.
- `tests/test_build_trace_site.py` — unit tests for parsing, timeline pairing, rendering, CLI.
- `tests/test_trace_wiring.py` — asserts `.claude/settings.json` registers the hooks + allow-list entries.
- `tests/fixtures/trace_sample.jsonl` — a hand-authored trace covering edgar → 3 parallel lanes → reconciliation.

Modified files:
- `.claude/settings.json` — add `hooks` block + two Bash allow-list entries.
- `.claude/skills/valuation/SKILL.md` — add a `--start` step and a final site-build step.

---

## Task 1: Event classification + normalization (pure functions)

**Files:**
- Create: `tools/trace_hook.py`
- Test: `tests/test_trace_hook.py`

**Interfaces:**
- Consumes: nothing (leaf module).
- Produces:
  - `classify_lane(tool_name, command=None, subagent_type=None, file_path=None) -> str` — returns one of the fixed lane strings.
  - `normalize_event(payload: dict, ts: float) -> dict` — turns a raw Claude Code hook payload into a normalized event dict with at least keys `ts`, `event`, `tool_name`, `lane`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_trace_hook.py
import trace_hook


def test_classify_lane_maps_bash_tool_to_lane():
    assert trace_hook.classify_lane("Bash", "python tools/montecarlo_dcf.py --cik 1") == "dcf"
    assert trace_hook.classify_lane("Bash", "python tools/comps.py --cik 1") == "comps"
    assert trace_hook.classify_lane("Bash", "python tools/embeddings.py --cik 1") == "comps"
    assert trace_hook.classify_lane("Bash", "python tools/edgar_fetch.py --ticker AAPL") == "edgar"
    assert trace_hook.classify_lane("Bash", "python tools/reconcile.py --cik 1") == "reconciliation"


def test_classify_lane_maps_agent_and_narrative():
    assert trace_hook.classify_lane("Task", subagent_type="dcf-analyst") == "dcf"
    assert trace_hook.classify_lane("Task", subagent_type="qualitative-analyst") == "qualitative"
    assert trace_hook.classify_lane("Read", file_path="data/0000320193/narrative.txt") == "qualitative"


def test_classify_lane_defaults_to_orchestrator():
    assert trace_hook.classify_lane("Bash", "ls -la") == "orchestrator"
    assert trace_hook.classify_lane("Read", file_path="data/x/financials.json") == "orchestrator"


def test_normalize_event_bash_pretool():
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": "s1",
        "transcript_path": "/t/dcf",
        "tool_name": "Bash",
        "tool_input": {"command": "python tools/montecarlo_dcf.py --cik 320193"},
    }
    ev = trace_hook.normalize_event(payload, ts=1007.0)
    assert ev["ts"] == 1007.0
    assert ev["event"] == "PreToolUse"
    assert ev["tool_name"] == "Bash"
    assert ev["lane"] == "dcf"
    assert ev["command"] == "python tools/montecarlo_dcf.py --cik 320193"


def test_normalize_event_task_and_posttool_output():
    task = trace_hook.normalize_event(
        {"hook_event_name": "PreToolUse", "tool_name": "Task",
         "tool_input": {"subagent_type": "comps-analyst", "prompt": "do comps"}},
        ts=1.0,
    )
    assert task["lane"] == "comps"
    assert task["subagent_type"] == "comps-analyst"
    assert task["prompt"] == "do comps"

    post = trace_hook.normalize_event(
        {"hook_event_name": "PostToolUse", "tool_name": "Bash",
         "tool_input": {"command": "python tools/reconcile.py --cik 1"},
         "tool_response": {"median": 178}},
        ts=2.0,
    )
    assert post["event"] == "PostToolUse"
    assert "178" in post["output"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_hook.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'trace_hook'`

- [ ] **Step 3: Write minimal implementation**

```python
# tools/trace_hook.py
import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LANE_BY_TOOL = {
    "edgar_fetch.py": "edgar",
    "financials.py": "edgar",
    "montecarlo_dcf.py": "dcf",
    "comps.py": "comps",
    "embeddings.py": "comps",
    "reconcile.py": "reconciliation",
    "market_price.py": "reconciliation",
    "build_trace_site.py": "orchestrator",
}

LANE_BY_AGENT = {
    "edgar-analyst": "edgar",
    "dcf-analyst": "dcf",
    "comps-analyst": "comps",
    "qualitative-analyst": "qualitative",
    "reconciliation-analyst": "reconciliation",
}

MAX_OUTPUT_CHARS = 20000


def classify_lane(tool_name, command=None, subagent_type=None, file_path=None):
    if subagent_type and subagent_type in LANE_BY_AGENT:
        return LANE_BY_AGENT[subagent_type]
    if command:
        for fname, lane in LANE_BY_TOOL.items():
            if fname in command:
                return lane
    if file_path and "narrative.txt" in file_path:
        return "qualitative"
    return "orchestrator"


def normalize_event(payload, ts):
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command")
    subagent_type = tool_input.get("subagent_type")
    prompt = tool_input.get("prompt")
    description = tool_input.get("description")
    file_path = tool_input.get("file_path")
    ev = {
        "ts": ts,
        "event": payload.get("hook_event_name"),
        "session_id": payload.get("session_id"),
        "transcript_path": payload.get("transcript_path"),
        "tool_name": payload.get("tool_name"),
        "lane": classify_lane(payload.get("tool_name"), command, subagent_type, file_path),
    }
    if command:
        ev["command"] = command
    if subagent_type:
        ev["subagent_type"] = subagent_type
    if prompt:
        ev["prompt"] = prompt
    if description:
        ev["description"] = description
    if file_path:
        ev["file"] = file_path
    resp = payload.get("tool_response")
    if resp is not None:
        text = resp if isinstance(resp, str) else json.dumps(resp)
        ev["output"] = text[:MAX_OUTPUT_CHARS]
    return ev
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_hook.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/05-business-valuation/tools/trace_hook.py code/practicals/05-business-valuation/tests/test_trace_hook.py
git commit -m "feat(code05): add trace event classification + normalization"
```

---

## Task 2: Trace gating, start/stop, and hook CLI

**Files:**
- Modify: `tools/trace_hook.py` (append the IO/CLI layer)
- Test: `tests/test_trace_hook.py` (add cases)

**Interfaces:**
- Consumes: `normalize_event` from Task 1.
- Produces:
  - `active_path(root=PROJECT_ROOT) -> Path` — the sentinel file `reports/trace/active.json`.
  - `start(prompt: str, ts: float, root=PROJECT_ROOT) -> Path` — creates the sentinel + a fresh `run-<int(ts)>.jsonl`, writes a `{"event":"start"}` line, returns the trace path.
  - `stop(ts: float, root=PROJECT_ROOT) -> Path|None` — appends `{"event":"stop"}`, removes the sentinel; `None` if no active run.
  - `handle(payload: dict, ts: float, root=PROJECT_ROOT) -> dict|None` — appends a normalized event only when a sentinel exists; clears the sentinel after a `Stop` event; returns the event or `None` when gated out.
  - `main(argv=None) -> int` — `--start [--prompt STR]`, `--stop`, or (no flags) read one hook payload from stdin.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_trace_hook.py
import json


def _read_lines(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def test_handle_is_silent_without_active_sentinel(tmp_path):
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": "python tools/comps.py --cik 1"}}
    assert trace_hook.handle(payload, ts=5.0, root=tmp_path) is None
    assert not trace_hook.active_path(tmp_path).exists()
    assert not (tmp_path / "reports" / "trace").exists() or \
        list((tmp_path / "reports" / "trace").glob("run-*.jsonl")) == []


def test_start_then_handle_writes_events(tmp_path):
    trace_file = trace_hook.start("/valuation AAPL", ts=1000.0, root=tmp_path)
    assert trace_hook.active_path(tmp_path).exists()
    trace_hook.handle(
        {"hook_event_name": "PreToolUse", "tool_name": "Bash",
         "tool_input": {"command": "python tools/montecarlo_dcf.py --cik 1"}},
        ts=1002.0, root=tmp_path,
    )
    rows = _read_lines(trace_file)
    assert rows[0]["event"] == "start" and rows[0]["prompt"] == "/valuation AAPL"
    assert rows[1]["event"] == "PreToolUse" and rows[1]["lane"] == "dcf"


def test_stop_event_via_handle_clears_sentinel(tmp_path):
    trace_hook.start("/valuation AAPL", ts=1.0, root=tmp_path)
    trace_hook.handle({"hook_event_name": "Stop"}, ts=9.0, root=tmp_path)
    assert not trace_hook.active_path(tmp_path).exists()


def test_main_start_and_stdin_hook(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(trace_hook, "PROJECT_ROOT", tmp_path)
    trace_hook.main(["--start", "--prompt", "/valuation MSFT"])
    payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                          "tool_input": {"command": "python tools/reconcile.py --cik 1"}})
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(payload))
    rc = trace_hook.main([])
    assert rc == 0
    runs = list((tmp_path / "reports" / "trace").glob("run-*.jsonl"))
    assert len(runs) == 1
    rows = _read_lines(runs[0])
    assert any(r.get("lane") == "reconciliation" for r in rows)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_hook.py -v`
Expected: FAIL with `AttributeError: module 'trace_hook' has no attribute 'active_path'`

- [ ] **Step 3: Write minimal implementation**

Append to `tools/trace_hook.py`:

```python
def _trace_dir(root):
    d = Path(root) / "reports" / "trace"
    d.mkdir(parents=True, exist_ok=True)
    return d


def active_path(root=PROJECT_ROOT):
    return Path(root) / "reports" / "trace" / "active.json"


def _append(trace_file, ev):
    with open(trace_file, "a") as f:
        f.write(json.dumps(ev) + "\n")


def start(prompt, ts, root=PROJECT_ROOT):
    trace_file = _trace_dir(root) / f"run-{int(ts)}.jsonl"
    trace_file.write_text("")
    active_path(root).write_text(json.dumps(
        {"trace": str(trace_file), "prompt": prompt, "started": ts}))
    _append(trace_file, {"ts": ts, "event": "start", "lane": "orchestrator", "prompt": prompt})
    return trace_file


def stop(ts, root=PROJECT_ROOT):
    ap = active_path(root)
    if not ap.exists():
        return None
    trace_file = Path(json.loads(ap.read_text())["trace"])
    _append(trace_file, {"ts": ts, "event": "stop", "lane": "orchestrator"})
    ap.unlink()
    return trace_file


def handle(payload, ts, root=PROJECT_ROOT):
    ap = active_path(root)
    if not ap.exists():
        return None
    trace_file = Path(json.loads(ap.read_text())["trace"])
    ev = normalize_event(payload, ts)
    _append(trace_file, ev)
    if ev.get("event") == "Stop":
        ap.unlink()
    return ev


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", action="store_true")
    ap.add_argument("--stop", action="store_true")
    ap.add_argument("--prompt", default="")
    a = ap.parse_args(argv)
    ts = time.time()
    try:
        if a.start:
            start(a.prompt, ts)
        elif a.stop:
            stop(ts)
        else:
            raw = sys.stdin.read()
            if raw.strip():
                handle(json.loads(raw), ts)
    except Exception:
        pass  # a hook must never break the run
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_hook.py -v`
Expected: PASS (9 tests total)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/05-business-valuation/tools/trace_hook.py code/practicals/05-business-valuation/tests/test_trace_hook.py
git commit -m "feat(code05): add trace gating, start/stop, and hook CLI"
```

---

## Task 3: Trace fixture + timeline model builder

**Files:**
- Create: `tools/build_trace_site.py`
- Create: `tests/fixtures/trace_sample.jsonl`
- Test: `tests/test_build_trace_site.py`

**Interfaces:**
- Consumes: nothing (reads a trace file written by Task 2's schema).
- Produces:
  - `load_events(trace_file) -> list[dict]` — one dict per non-blank JSON line.
  - `newest_trace(trace_dir=TRACE_DIR) -> Path|None` — newest `run-*.jsonl` by name.
  - `build_timeline(events: list[dict]) -> dict` — returns `{"prompt": str, "t0": float, "t1": float, "lanes": [ {"lane": str, "label": str, "blocks": [ {"lane","tool_name","command","subagent_type","prompt","file","start","end","output"} ]} ], "hooks": [ {"ts","event","lane"} ]}`. Lanes appear in fixed `LANE_ORDER`, only if non-empty. `PreToolUse`/`PostToolUse` with matching `(transcript_path, tool_name, command)` are paired into one block (`start` from Pre, `end`+`output` from Post).

- [ ] **Step 1: Create the fixture**

```
# tests/fixtures/trace_sample.jsonl
{"ts": 1000.0, "event": "start", "lane": "orchestrator", "prompt": "/valuation AAPL"}
{"ts": 1001.0, "event": "PreToolUse", "tool_name": "Task", "lane": "edgar", "subagent_type": "edgar-analyst", "prompt": "fetch AAPL"}
{"ts": 1002.0, "event": "PreToolUse", "tool_name": "Bash", "lane": "edgar", "command": "python tools/edgar_fetch.py --ticker AAPL", "transcript_path": "/t/edgar"}
{"ts": 1004.0, "event": "PostToolUse", "tool_name": "Bash", "lane": "edgar", "command": "python tools/edgar_fetch.py --ticker AAPL", "transcript_path": "/t/edgar", "output": "{\"cik\": \"0000320193\"}"}
{"ts": 1005.0, "event": "SubagentStop", "lane": "orchestrator"}
{"ts": 1006.0, "event": "PreToolUse", "tool_name": "Task", "lane": "dcf", "subagent_type": "dcf-analyst", "prompt": "run dcf"}
{"ts": 1006.1, "event": "PreToolUse", "tool_name": "Task", "lane": "comps", "subagent_type": "comps-analyst", "prompt": "run comps"}
{"ts": 1007.0, "event": "PreToolUse", "tool_name": "Bash", "lane": "dcf", "command": "python tools/montecarlo_dcf.py --cik 320193", "transcript_path": "/t/dcf"}
{"ts": 1007.5, "event": "PreToolUse", "tool_name": "Bash", "lane": "comps", "command": "python tools/comps.py --cik 320193", "transcript_path": "/t/comps"}
{"ts": 1009.0, "event": "PostToolUse", "tool_name": "Bash", "lane": "dcf", "command": "python tools/montecarlo_dcf.py --cik 320193", "transcript_path": "/t/dcf", "output": "{\"median\": 180}"}
{"ts": 1010.0, "event": "PostToolUse", "tool_name": "Bash", "lane": "comps", "command": "python tools/comps.py --cik 320193", "transcript_path": "/t/comps", "output": "{}"}
{"ts": 1012.0, "event": "PreToolUse", "tool_name": "Bash", "lane": "reconciliation", "command": "python tools/reconcile.py --cik 320193", "transcript_path": "/t/main"}
{"ts": 1013.0, "event": "PostToolUse", "tool_name": "Bash", "lane": "reconciliation", "command": "python tools/reconcile.py --cik 320193", "transcript_path": "/t/main", "output": "{\"median\": 178}"}
{"ts": 1014.0, "event": "stop", "lane": "orchestrator"}
```

- [ ] **Step 2: Write the failing test**

```python
# tests/test_build_trace_site.py
from pathlib import Path

import build_trace_site

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "trace_sample.jsonl"


def test_load_events_reads_all_lines():
    events = build_trace_site.load_events(FIXTURE)
    assert len(events) == 14
    assert events[0]["event"] == "start"


def test_build_timeline_groups_and_orders_lanes():
    model = build_trace_site.build_timeline(build_trace_site.load_events(FIXTURE))
    lane_names = [l["lane"] for l in model["lanes"]]
    assert lane_names == ["edgar", "dcf", "comps", "reconciliation"]
    assert model["prompt"] == "/valuation AAPL"
    assert model["t0"] == 1000.0 and model["t1"] == 1014.0


def test_build_timeline_pairs_pre_and_post():
    model = build_trace_site.build_timeline(build_trace_site.load_events(FIXTURE))
    dcf = next(l for l in model["lanes"] if l["lane"] == "dcf")
    bash_block = next(b for b in dcf["blocks"] if b["tool_name"] == "Bash")
    assert bash_block["start"] == 1007.0
    assert bash_block["end"] == 1009.0
    assert "180" in bash_block["output"]


def test_build_timeline_collects_hook_rail():
    model = build_trace_site.build_timeline(build_trace_site.load_events(FIXTURE))
    events = {h["event"] for h in model["hooks"]}
    assert "PreToolUse" in events and "PostToolUse" in events and "SubagentStop" in events
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_build_trace_site.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'build_trace_site'`

- [ ] **Step 4: Write minimal implementation**

```python
# tools/build_trace_site.py
import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = PROJECT_ROOT / "reports" / "trace"
REPORTS_DIR = PROJECT_ROOT / "reports"

LANE_ORDER = ["edgar", "dcf", "comps", "qualitative", "reconciliation", "orchestrator"]
LANE_LABEL = {
    "edgar": "edgar-analyst",
    "dcf": "dcf-analyst",
    "comps": "comps-analyst",
    "qualitative": "qualitative-analyst",
    "reconciliation": "reconciliation-analyst",
    "orchestrator": "orchestrator (skill)",
}


def load_events(trace_file):
    events = []
    for line in Path(trace_file).read_text().splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def newest_trace(trace_dir=TRACE_DIR):
    runs = sorted(Path(trace_dir).glob("run-*.jsonl"))
    return runs[-1] if runs else None


def build_timeline(events):
    prompt = ""
    blocks = []
    hooks = []
    pending = {}
    ts_all = [e["ts"] for e in events if "ts" in e]
    t0 = min(ts_all) if ts_all else 0.0
    t1 = max(ts_all) if ts_all else 1.0
    for e in events:
        ev = e.get("event")
        if ev == "start":
            prompt = e.get("prompt", "")
            continue
        if ev == "stop":
            continue
        hooks.append({"ts": e.get("ts", t0), "event": ev, "lane": e.get("lane", "orchestrator")})
        key = (e.get("transcript_path"), e.get("tool_name"), e.get("command"))
        if ev == "PreToolUse":
            blk = {
                "lane": e.get("lane", "orchestrator"),
                "tool_name": e.get("tool_name"),
                "command": e.get("command"),
                "subagent_type": e.get("subagent_type"),
                "prompt": e.get("prompt"),
                "file": e.get("file"),
                "start": e.get("ts", t0),
                "end": e.get("ts", t0),
                "output": "",
            }
            blocks.append(blk)
            pending[key] = blk
        elif ev == "PostToolUse":
            blk = pending.pop(key, None)
            if blk is not None:
                blk["end"] = e.get("ts", blk["start"])
                blk["output"] = e.get("output", "")
            else:
                blocks.append({
                    "lane": e.get("lane", "orchestrator"),
                    "tool_name": e.get("tool_name"),
                    "command": e.get("command"),
                    "subagent_type": None, "prompt": None, "file": None,
                    "start": e.get("ts", t0), "end": e.get("ts", t0),
                    "output": e.get("output", ""),
                })
    lanes = []
    for lane in LANE_ORDER:
        lane_blocks = [b for b in blocks if b["lane"] == lane]
        if lane_blocks:
            lanes.append({"lane": lane, "label": LANE_LABEL[lane], "blocks": lane_blocks})
    return {"prompt": prompt, "t0": t0, "t1": t1, "lanes": lanes, "hooks": hooks}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_build_trace_site.py -v`
Expected: PASS (4 tests)

- [ ] **Step 6: Commit**

```bash
git add code/practicals/05-business-valuation/tools/build_trace_site.py code/practicals/05-business-valuation/tests/test_build_trace_site.py code/practicals/05-business-valuation/tests/fixtures/trace_sample.jsonl
git commit -m "feat(code05): parse valuation trace into a timeline model"
```

---

## Task 4: HTML render + CLI

**Files:**
- Modify: `tools/build_trace_site.py` (add `render_html`, `main`)
- Test: `tests/test_build_trace_site.py` (add cases)

**Interfaces:**
- Consumes: `build_timeline`, `load_events`, `newest_trace` from Task 3.
- Produces:
  - `render_html(model: dict, ticker: str, date: str, headline: str = "") -> str` — a complete self-contained HTML document (inline `<style>`; expandable detail via native `<details>`; blocks positioned by timestamp percentage).
  - `main(argv=None) -> int` — `--ticker` (req), `--date` (req), `--headline`, `--trace` (default `newest_trace()`), `--out` (default `reports/<TICKER>-<date>.html`); writes the file and prints its path; returns 1 with a JSON error if no trace exists.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_build_trace_site.py
def test_render_html_contains_lanes_headline_and_prompt():
    model = build_trace_site.build_timeline(build_trace_site.load_events(FIXTURE))
    doc = build_trace_site.render_html(model, "AAPL", "2026-07-01",
                                       headline="AAPL fair value ~ $178/share")
    assert doc.lstrip().startswith("<!doctype html>")
    assert "swimlane" in doc
    assert "dcf-analyst" in doc and "reconciliation-analyst" in doc
    assert "montecarlo_dcf.py" in doc
    assert "/valuation AAPL" in doc
    assert "$178" in doc
    assert "<details" in doc  # expandable tool/agent detail


def test_render_html_escapes_output():
    model = {"prompt": "<x>", "t0": 0.0, "t1": 1.0,
             "lanes": [{"lane": "dcf", "label": "dcf-analyst",
                        "blocks": [{"lane": "dcf", "tool_name": "Bash",
                                    "command": "echo <b>", "subagent_type": None,
                                    "prompt": None, "file": None,
                                    "start": 0.0, "end": 1.0, "output": "<script>"}]}],
             "hooks": []}
    doc = build_trace_site.render_html(model, "T", "2026-07-01")
    assert "<script>" not in doc
    assert "&lt;script&gt;" in doc


def test_main_writes_html_from_explicit_trace(tmp_path, capsys):
    out = tmp_path / "AAPL-2026-07-01.html"
    rc = build_trace_site.main(["--ticker", "AAPL", "--date", "2026-07-01",
                                "--trace", str(FIXTURE), "--out", str(out)])
    assert rc == 0
    assert out.exists()
    assert "dcf-analyst" in out.read_text()
    assert str(out) in capsys.readouterr().out


def test_main_errors_when_no_trace(tmp_path, capsys):
    missing = tmp_path / "none.jsonl"
    rc = build_trace_site.main(["--ticker", "AAPL", "--date", "2026-07-01",
                                "--trace", str(missing), "--out", str(tmp_path / "o.html")])
    assert rc == 1
    assert "error" in capsys.readouterr().out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_build_trace_site.py -v`
Expected: FAIL with `AttributeError: module 'build_trace_site' has no attribute 'render_html'`

- [ ] **Step 3: Write minimal implementation**

Add `import html` to the top imports, then append to `tools/build_trace_site.py`:

```python
CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#0f1420;color:#e6ebf5}
header{padding:20px 28px;background:#161c2b;border-bottom:1px solid #2a3346}
header h1{margin:0 0 6px;font-size:18px}
.prompt{font-family:ui-monospace,Menlo,monospace;color:#8fb7ff}
.headline{margin-top:8px;color:#9be7b4;font-weight:600}
.hooks-rail{position:relative;height:22px;margin:14px 28px 0;border-bottom:1px dashed #33405c}
.hooks-rail .hook{position:absolute;top:4px;width:2px;height:14px;background:#f0a33c}
.swimlane{padding:12px 28px 40px}
.lane{display:flex;align-items:stretch;margin:8px 0}
.lane-name{width:170px;flex:0 0 170px;font-size:13px;color:#b9c3d6;padding-top:6px}
.track{position:relative;flex:1;height:34px;background:#131a29;border-radius:6px}
.blk{position:absolute;top:3px;height:28px;background:#2d4a8a;border:1px solid #4d6fc0;border-radius:5px;
     color:#eaf1ff;font-size:11px;overflow:hidden}
.blk[open]{z-index:5;height:auto;min-width:280px;background:#1b2740;overflow:visible}
.blk summary{padding:6px 8px;cursor:pointer;white-space:nowrap;list-style:none}
.blk pre{margin:0;padding:6px 8px;white-space:pre-wrap;word-break:break-word;font-size:11px;background:#0c111c}
.blk pre.out{color:#9be7b4;border-top:1px solid #2a3346;max-height:280px;overflow:auto}
.legend{padding:16px 28px;color:#8a97ad;font-size:12px;border-top:1px solid #2a3346}
.legend b{color:#e6ebf5}
"""


def _pct(ts, t0, t1):
    span = (t1 - t0) or 1.0
    return max(0.0, min(100.0, (ts - t0) / span * 100.0))


def render_html(model, ticker, date, headline=""):
    t0, t1 = model["t0"], model["t1"]
    lane_html = []
    for lane in model["lanes"]:
        segs = []
        for b in lane["blocks"]:
            left = _pct(b["start"], t0, t1)
            width = max(2.0, _pct(b["end"], t0, t1) - left)
            label = b.get("subagent_type") or b.get("tool_name") or "?"
            detail = b.get("command") or b.get("prompt") or b.get("file") or ""
            out = b.get("output") or ""
            segs.append(
                f'<details class="blk" style="left:{left:.2f}%;width:{width:.2f}%">'
                f'<summary>{html.escape(str(label))}</summary>'
                f'<pre>{html.escape(str(detail))}</pre>'
                f'<pre class="out">{html.escape(str(out)[:8000])}</pre>'
                f'</details>'
            )
        lane_html.append(
            f'<div class="lane"><div class="lane-name">{html.escape(lane["label"])}</div>'
            f'<div class="track">{"".join(segs)}</div></div>'
        )
    hook_marks = "".join(
        f'<span class="hook" style="left:{_pct(h["ts"], t0, t1):.2f}%" '
        f'title="{html.escape(str(h["event"]))}"></span>'
        for h in model["hooks"]
    )
    headline_html = f'<div class="headline">{html.escape(headline)}</div>' if headline else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(ticker)} valuation trace — {html.escape(date)}</title>
<style>{CSS}</style></head>
<body>
<header>
  <h1>{html.escape(ticker)} — valuation run trace</h1>
  <div class="prompt">{html.escape(model["prompt"])}</div>
  {headline_html}
</header>
<div class="hooks-rail" title="hook firings">{hook_marks}</div>
<section class="swimlane">{"".join(lane_html)}</section>
<footer class="legend">
  <b>How to read this:</b> each row is an <b>agent</b> the skill dispatched; boxes are
  <b>tool calls</b> (click to expand the exact command and captured output). The orange
  ticks above are <b>hook firings</b> — the same hooks that captured this trace. Overlapping
  boxes across rows show lanes running in <b>parallel</b>.
</footer>
</body></html>"""


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--headline", default="")
    ap.add_argument("--trace", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    trace_file = Path(a.trace) if a.trace else newest_trace()
    if not trace_file or not Path(trace_file).exists():
        print(json.dumps({"error": "no trace file found"}))
        return 1
    model = build_timeline(load_events(trace_file))
    doc = render_html(model, a.ticker, a.date, a.headline)
    out = Path(a.out) if a.out else REPORTS_DIR / f"{a.ticker}-{a.date}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print(str(out))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_build_trace_site.py -v`
Expected: PASS (8 tests total)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/05-business-valuation/tools/build_trace_site.py code/practicals/05-business-valuation/tests/test_build_trace_site.py
git commit -m "feat(code05): render valuation trace as a self-contained HTML site"
```

---

## Task 5: Register hooks + allow-list in settings.json

**Files:**
- Modify: `.claude/settings.json`
- Test: `tests/test_trace_wiring.py`

**Interfaces:**
- Consumes: `trace_hook.py`, `build_trace_site.py` command names.
- Produces: a `settings.json` that runs `python tools/trace_hook.py` on `PreToolUse`, `PostToolUse`, `SubagentStop`, `Stop`, and allows the two new Bash commands.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_trace_wiring.py
import json
from pathlib import Path

SETTINGS = Path(__file__).resolve().parent.parent / ".claude" / "settings.json"


def _hook_commands(cfg, event):
    cmds = []
    for group in cfg.get("hooks", {}).get(event, []):
        for h in group.get("hooks", []):
            cmds.append(h.get("command"))
    return cmds


def test_settings_registers_trace_hook_on_all_events():
    cfg = json.loads(SETTINGS.read_text())
    for event in ("PreToolUse", "PostToolUse", "SubagentStop", "Stop"):
        assert any("trace_hook.py" in c for c in _hook_commands(cfg, event)), event


def test_settings_allows_new_tools():
    cfg = json.loads(SETTINGS.read_text())
    allow = cfg["permissions"]["allow"]
    assert any("build_trace_site.py" in a for a in allow)
    assert any("trace_hook.py" in a for a in allow)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_wiring.py -v`
Expected: FAIL (`KeyError`/assertion — no `hooks` block, no new allow entries)

- [ ] **Step 3: Write the new settings.json**

Replace the entire contents of `.claude/settings.json` with:

```json
{
  "permissions": {
    "allow": [
      "Bash(python tools/edgar_fetch.py:*)",
      "Bash(python tools/financials.py:*)",
      "Bash(python tools/montecarlo_dcf.py:*)",
      "Bash(python tools/market_price.py:*)",
      "Bash(python tools/comps.py:*)",
      "Bash(python tools/embeddings.py:*)",
      "Bash(python tools/reconcile.py:*)",
      "Bash(python tools/trace_hook.py:*)",
      "Bash(python tools/build_trace_site.py:*)",
      "Bash(pip install:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python tools/trace_hook.py"}]}
    ],
    "PostToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python tools/trace_hook.py"}]}
    ],
    "SubagentStop": [
      {"hooks": [{"type": "command", "command": "python tools/trace_hook.py"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python tools/trace_hook.py"}]}
    ]
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest tests/test_trace_wiring.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/05-business-valuation/.claude/settings.json code/practicals/05-business-valuation/tests/test_trace_wiring.py
git commit -m "feat(code05): register trace hooks and allow-list trace tools"
```

---

## Task 6: Wire the skill + full offline verification

**Files:**
- Modify: `.claude/skills/valuation/SKILL.md`

**Interfaces:**
- Consumes: `trace_hook.py --start`, `build_trace_site.py` CLI.
- Produces: a skill that starts a trace before Step 1 and builds the site after the report.

- [ ] **Step 1: Add the trace-start instruction**

In `.claude/skills/valuation/SKILL.md`, immediately after the `Announce:` line (before `## Step 1`), insert:

```markdown
## Step 0 — Start the run trace
Run `python tools/trace_hook.py --start --prompt "/valuation <ARG>"` once. This
opens a fresh trace and lets the registered hooks capture every subsequent agent
and tool call. (Hooks stay silent outside an active run.)
```

- [ ] **Step 2: Add the site-build step**

In the same file, rename the current `## Step 4 — Headline` section to `## Step 5 — Headline`, and insert before it:

```markdown
## Step 4 — Build the trace site
Run `python tools/build_trace_site.py --ticker <TICKER> --date <date> --headline
"<headline>"` where `<headline>` is the same one-line fair-value summary from
Step 5. It reads the newest trace and writes `reports/<TICKER>-<date>.html`.
Print that path to the user alongside the report path.
```

- [ ] **Step 3: Verify the full offline test suite passes**

Run: `cd code/practicals/05-business-valuation && python -m pytest -q`
Expected: PASS — all pre-existing tests plus the new `test_trace_hook.py`, `test_build_trace_site.py`, `test_trace_wiring.py`.

- [ ] **Step 4: Manual end-to-end smoke of the generator**

Run: `cd code/practicals/05-business-valuation && python tools/build_trace_site.py --ticker AAPL --date 2026-07-01 --trace tests/fixtures/trace_sample.jsonl --out /tmp/trace_smoke.html && open /tmp/trace_smoke.html`
Expected: the browser shows the header prompt `/valuation AAPL`, an orange hook rail, and swimlanes for edgar/dcf/comps/reconciliation with the dcf and comps boxes overlapping in time; clicking a box expands its command + output.

- [ ] **Step 5: Commit**

```bash
git add code/practicals/05-business-valuation/.claude/skills/valuation/SKILL.md
git commit -m "feat(code05): build run-trace site as final step of /valuation"
```

---

## Self-Review

**Spec coverage:**
- Real captured trace → Tasks 1–2 (hooks capture normalized events). ✓
- Hooks as capture + teaching example → Task 5 registration; legend in Task 4. ✓
- Auto-generation as final skill step → Task 6. ✓
- Single self-contained HTML → Task 4 `render_html` (inline CSS, native `<details>`, no assets). ✓
- Swimlane centerpiece with parallel lanes → Task 4 layout + Task 3 lane grouping. ✓
- Expandable full detail (command/args/output/dispatch prompt) → Task 4 `<details>` blocks. ✓
- Tool→lane attribution + transcript pairing → Task 1 `classify_lane`, Task 3 `(transcript_path, tool_name, command)` pairing. ✓
- Offline deterministic tests + fixture → Tasks 1–5. ✓
- Graceful degradation on missing fields → `.get(...)` defaults throughout; `main` swallows hook errors. ✓

**Deviations from spec (intentional, documented):** gating is created by the skill's explicit `--start` rather than a `UserPromptSubmit` hook (slash-command prompt text is not reliably visible to a hook and subagents may carry different session ids); the sentinel is a single `reports/trace/active.json` so gating is robust to session-id differences. No `.gitignore` change (all of `reports/` is already ignored).

**Placeholder scan:** none — every code step contains complete code.

**Type consistency:** `classify_lane`/`normalize_event` signatures match between Tasks 1–2 and their use in Task 3's fixture schema; `build_timeline`'s returned dict keys (`prompt`,`t0`,`t1`,`lanes`,`hooks`, and block keys) match `render_html`'s reads in Task 4; CLI flag names consistent across Tasks 4 and 6.
