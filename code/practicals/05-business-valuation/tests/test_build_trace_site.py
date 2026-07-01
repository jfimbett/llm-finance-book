import build_trace_site as b


def test_build_spans_pairs_pre_and_post():
    events = [
        {"event": "PreToolUse", "tool_name": "Bash", "lane": "dcf",
         "command": "python tools/montecarlo_dcf.py --cik 1", "ts": 100.0},
        {"event": "PostToolUse", "tool_name": "Bash", "lane": "dcf",
         "command": "python tools/montecarlo_dcf.py --cik 1", "ts": 102.5,
         "output": '{"median": 178}'},
    ]
    spans = b.build_spans(events)
    assert len(spans) == 1
    s = spans[0]
    assert s["lane"] == "dcf" and s["label"] == "Bash"
    assert abs(s["dur"] - 2.5) < 1e-9
    assert "178" in s["output"]


def test_build_spans_keeps_unclosed_pre():
    events = [{"event": "PreToolUse", "tool_name": "Task", "lane": "comps",
               "subagent_type": "comps-analyst", "ts": 5.0}]
    spans = b.build_spans(events)
    assert len(spans) == 1 and spans[0]["dur"] is None
    assert spans[0]["label"] == "comps-analyst"


def test_render_html_includes_headline_and_gap():
    ctx = {
        "ticker": "AAPL", "date": "2026-07-01",
        "final": {"median": 210.0, "p10": 180.0, "p90": 240.0,
                  "p90_p10_ratio": 1.33, "review_required": False,
                  "review_reason": "P90/P10 spread 1.3x within 2x",
                  "weights": {"dcf": 0.5, "llm": 0.3, "embedding": 0.2}},
        "market": {"price": 190.0},
        "lanes": [{"label": "DCF (Monte Carlo)", "lane": "dcf",
                   "median": 205.0, "p10": 170.0, "p90": 250.0, "weight": 0.5}],
        "sensitivity": {
            "wacc_axis": [0.08, 0.10], "tg_axis": [0.02, 0.03],
            "grid": [[210.0, 260.0], [180.0, 205.0]],
            "base": {"wacc": 0.10, "terminal_growth": 0.03, "per_share": 205.0}},
        "meta": {"risk_summary": ["Concentration in iPhone revenue"],
                 "normalization_notes": ["Stripped $2B one-time litigation charge"]},
        "spans": b.build_spans([
            {"event": "PreToolUse", "tool_name": "Bash", "lane": "dcf",
             "command": "python tools/montecarlo_dcf.py", "ts": 1.0},
            {"event": "PostToolUse", "tool_name": "Bash", "lane": "dcf",
             "command": "python tools/montecarlo_dcf.py", "ts": 3.0, "output": "ok"},
        ]),
    }
    htm = b.render_html(ctx)
    assert "AAPL" in htm and "$210.00" in htm
    assert "under-valued" in htm  # median 210 > price 190
    assert "within governance band" in htm
    assert "Concentration in iPhone revenue" in htm
    assert "one-time litigation" in htm
    assert "g≥WACC" not in htm  # this grid has no blocked cells
    assert "montecarlo_dcf" in htm  # timeline rendered
    assert htm.strip().startswith("<!doctype html>")


def test_render_html_flags_review():
    ctx = {"ticker": "XYZ", "date": "2026-07-01",
           "final": {"median": 10.0, "p10": 2.0, "p90": 40.0,
                     "review_required": True,
                     "review_reason": "P90/P10 spread 20.0x exceeds 2x"},
           "market": {}, "lanes": [], "sensitivity": None, "meta": {}, "spans": []}
    htm = b.render_html(ctx)
    assert "human review required" in htm
    assert "No agent trace" in htm
