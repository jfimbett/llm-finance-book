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
