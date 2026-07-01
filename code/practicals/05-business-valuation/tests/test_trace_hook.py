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
