import argparse
import datetime
import html
import json
from pathlib import Path

from _common import PROJECT_ROOT, cik_pad, data_dir, emit

# ── Lane palette (kept in sync with trace_hook's lane names) ──────────────────
LANE_COLORS = {
    "edgar": "#2563eb",
    "dcf": "#7c3aed",
    "comps": "#0891b2",
    "qualitative": "#d97706",
    "reconciliation": "#16a34a",
    "orchestrator": "#64748b",
}
LANE_LABELS = {
    "edgar": "EDGAR / data",
    "dcf": "DCF lane",
    "comps": "Comparables lane",
    "qualitative": "Qualitative lane",
    "reconciliation": "Reconciliation",
    "orchestrator": "Orchestrator",
}

CSS = """
:root { --bg:#0f172a; --card:#1e293b; --ink:#e2e8f0; --muted:#94a3b8; --line:#334155; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; }
.wrap { max-width:1040px; margin:0 auto; padding:32px 24px 80px; }
h1 { font-size:26px; margin:0 0 4px; }
h2 { font-size:18px; margin:34px 0 12px; border-bottom:1px solid var(--line); padding-bottom:6px; }
.sub { color:var(--muted); margin:0 0 8px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px 20px; }
.headline { font-size:22px; font-weight:600; }
.headline .band { color:var(--muted); font-size:16px; font-weight:400; }
.badge { display:inline-block; padding:2px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.badge.ok { background:#14532d; color:#bbf7d0; }
.badge.warn { background:#7c2d12; color:#fed7aa; }
table { border-collapse:collapse; width:100%; font-size:14px; }
th,td { padding:7px 10px; text-align:right; border-bottom:1px solid var(--line); }
th:first-child, td:first-child { text-align:left; }
thead th { color:var(--muted); font-weight:600; }
.bar { position:relative; height:46px; margin:14px 0 6px; }
.bar .track { position:absolute; top:20px; left:0; right:0; height:8px; background:var(--line); border-radius:4px; }
.bar .range { position:absolute; top:18px; height:12px; background:#7c3aed55; border:1px solid #7c3aed; border-radius:6px; }
.bar .mark { position:absolute; top:8px; width:2px; height:32px; }
.bar .lbl { position:absolute; top:-2px; font-size:11px; transform:translateX(-50%); white-space:nowrap; }
.heat td { text-align:center; font-variant-numeric:tabular-nums; color:#0b1220; font-weight:600;
  border:1px solid var(--bg); min-width:70px; }
.heat th { text-align:center; color:var(--muted); font-weight:600; border:none; }
.heat td.null { background:repeating-linear-gradient(45deg,#334155,#334155 5px,#1e293b 5px,#1e293b 10px);
  color:var(--muted); font-weight:400; }
.heat td.base { outline:3px solid #f8fafc; outline-offset:-3px; }
.legend { display:flex; flex-wrap:wrap; gap:12px; margin:6px 0 4px; font-size:13px; color:var(--muted); }
.legend span::before { content:""; display:inline-block; width:11px; height:11px; border-radius:3px;
  margin-right:5px; vertical-align:middle; background:var(--c); }
.tl { position:relative; margin-top:8px; }
.tl .row { display:grid; grid-template-columns:78px 1fr; gap:12px; padding:8px 0;
  border-bottom:1px solid var(--line); }
.tl .t { color:var(--muted); font-size:12px; font-variant-numeric:tabular-nums; padding-top:2px; }
.tl .body { border-left:3px solid var(--c); padding-left:12px; }
.tl .op { font-weight:600; }
.tl .lane { font-size:11px; color:var(--c); text-transform:uppercase; letter-spacing:.04em; }
.tl .dur { color:var(--muted); font-size:12px; margin-left:8px; }
.tl code { background:#0b1220; padding:1px 6px; border-radius:5px; font-size:12.5px;
  color:#cbd5e1; word-break:break-all; }
details { margin-top:6px; } summary { cursor:pointer; color:var(--muted); font-size:12px; }
details pre { background:#0b1220; padding:10px; border-radius:8px; overflow:auto; font-size:12px;
  max-height:240px; color:#cbd5e1; }
ul.risks { margin:6px 0; padding-left:20px; } ul.risks li { margin:3px 0; }
.foot { color:var(--muted); font-size:12px; margin-top:40px; }
"""


def esc(x):
    return html.escape("" if x is None else str(x))


def _money(x):
    return "—" if x is None else f"${x:,.2f}"


def _pct(x):
    return "—" if x is None else f"{x * 100:.1f}%"


# ── trace → spans ─────────────────────────────────────────────────────────────
def _span(pre, post):
    tool = pre.get("tool_name")
    if pre.get("subagent_type"):
        label, detail = pre["subagent_type"], pre.get("description") or pre.get("prompt") or ""
    elif pre.get("command"):
        label, detail = "Bash", pre["command"]
    elif pre.get("file"):
        label, detail = tool, pre["file"]
    else:
        label, detail = (tool or "?"), pre.get("prompt") or ""
    start = float(pre.get("ts", 0) or 0)
    end = float(post["ts"]) if post and post.get("ts") is not None else None
    return {
        "lane": pre.get("lane", "orchestrator"),
        "tool": tool, "label": label, "detail": detail,
        "start": start, "end": end,
        "dur": (end - start) if end is not None else None,
        "output": (post or {}).get("output", ""),
    }


def build_spans(events):
    events = sorted(events, key=lambda e: e.get("ts", 0) or 0)

    def keyof(e):
        return (e.get("tool_name"),
                e.get("command") or e.get("subagent_type") or e.get("file") or "")

    open_by_key, spans = {}, []
    for e in events:
        if e.get("event") == "PreToolUse":
            open_by_key.setdefault(keyof(e), []).append(e)
        elif e.get("event") == "PostToolUse":
            stack = open_by_key.get(keyof(e))
            spans.append(_span(stack.pop(0), e) if stack else _span(e, e))
    for stack in open_by_key.values():
        for pre in stack:
            spans.append(_span(pre, None))
    spans.sort(key=lambda s: s["start"])
    return spans


# ── HTML sections ─────────────────────────────────────────────────────────────
def _band_html(final, market):
    p10, med, p90 = final.get("p10"), final.get("median"), final.get("p90")
    if None in (p10, med, p90):
        return ""
    price = (market or {}).get("price")
    lo = min([v for v in (p10, price) if v is not None]) * 0.92
    hi = max([v for v in (p90, price) if v is not None]) * 1.08
    span = (hi - lo) or 1.0

    def pos(v):
        return max(0.0, min(100.0, (v - lo) / span * 100.0))

    parts = ['<div class="bar"><div class="track"></div>']
    parts.append(f'<div class="range" style="left:{pos(p10):.1f}%;'
                 f'width:{pos(p90) - pos(p10):.1f}%"></div>')
    parts.append(f'<div class="mark" style="left:{pos(med):.1f}%;background:#a78bfa"></div>'
                 f'<div class="lbl" style="left:{pos(med):.1f}%;color:#a78bfa">'
                 f'fair {_money(med)}</div>')
    if price is not None:
        parts.append(f'<div class="mark" style="left:{pos(price):.1f}%;background:#f8fafc"></div>'
                     f'<div class="lbl" style="left:{pos(price):.1f}%;top:34px">'
                     f'market {_money(price)}</div>')
    parts.append(f'<div class="lbl" style="left:{pos(p10):.1f}%;top:34px">P10 {_money(p10)}</div>')
    parts.append(f'<div class="lbl" style="left:{pos(p90):.1f}%;top:34px">P90 {_money(p90)}</div>')
    parts.append('</div>')
    return "".join(parts)


def _lanes_table(lanes):
    if not lanes:
        return ""
    rows = ["<table><thead><tr><th>Lane</th><th>Median</th><th>P10</th>"
            "<th>P90</th><th>Weight</th><th>Peers</th></tr></thead><tbody>"]
    for lane in lanes:
        peers = ", ".join(lane.get("peers", []) or [])
        w = lane.get("weight")
        rows.append(
            f"<tr><td>{esc(lane['label'])}</td><td>{_money(lane.get('median'))}</td>"
            f"<td>{_money(lane.get('p10'))}</td><td>{_money(lane.get('p90'))}</td>"
            f"<td>{'—' if w is None else f'{w * 100:.0f}%'}</td>"
            f"<td style='text-align:left;color:#94a3b8;font-size:12.5px'>{esc(peers)}</td></tr>")
    rows.append("</tbody></table>")
    return "".join(rows)


def _heatmap_html(sens):
    if not sens or not sens.get("grid"):
        return ""
    waxis, taxis, grid = sens["wacc_axis"], sens["tg_axis"], sens["grid"]
    base = sens.get("base") or {}
    vals = [v for row in grid for v in row if v is not None]
    if not vals:
        return ""
    vmin, vmax = min(vals), max(vals)
    rng = (vmax - vmin) or 1.0

    def color(v):
        t = (v - vmin) / rng
        hue = 210 * (1 - t)  # blue (low) → red (high)
        return f"hsl({hue:.0f},72%,62%)"

    out = ['<table class="heat"><thead><tr><th>WACC ＼ g</th>']
    out += [f"<th>{_pct(tg)}</th>" for tg in taxis]
    out.append("</tr></thead><tbody>")
    for i, w in enumerate(waxis):
        out.append(f"<tr><th>{_pct(w)}</th>")
        for j, tg in enumerate(taxis):
            v = grid[i][j]
            is_base = (abs(w - base.get("wacc", -9)) < 1e-9
                       and abs(tg - base.get("terminal_growth", -9)) < 1e-9)
            cls = "base" if is_base else ""
            if v is None:
                out.append(f'<td class="null {cls}">g≥WACC</td>')
            else:
                out.append(f'<td class="{cls}" style="background:{color(v)}">${v:,.0f}</td>')
        out.append("</tr>")
    out.append("</tbody></table>")
    out.append('<p class="sub">Each cell is DCF fair value per share holding the other drivers '
               'at their central case; the outlined cell is the base case. Note how the value '
               'explodes as terminal growth <em>g</em> approaches WACC — the terminal-value '
               'dominance the lecture warned about.</p>')
    return "".join(out)


def _timeline_html(spans):
    if not spans:
        return '<p class="sub">No agent trace was recorded. Enable the PreToolUse/PostToolUse ' \
               'hooks in <code>.claude/settings.json</code> and re-run.</p>'
    t0 = spans[0]["start"]
    lanes_seen = []
    for s in spans:
        if s["lane"] not in lanes_seen:
            lanes_seen.append(s["lane"])
    legend = '<div class="legend">' + "".join(
        f'<span style="--c:{LANE_COLORS.get(l, "#64748b")}">{esc(LANE_LABELS.get(l, l))}</span>'
        for l in lanes_seen) + "</div>"

    rows = ['<div class="tl">']
    for s in spans:
        c = LANE_COLORS.get(s["lane"], "#64748b")
        rel = s["start"] - t0
        dur = "" if s["dur"] is None else f'<span class="dur">{s["dur"]:.1f}s</span>'
        detail = esc(s["detail"])[:400]
        detail_html = f"<code>{detail}</code>" if s["tool"] == "Bash" else esc(s["detail"])[:400]
        out_html = ""
        if s["output"]:
            out_html = (f"<details><summary>output</summary><pre>"
                        f"{esc(s['output'])[:4000]}</pre></details>")
        rows.append(
            f'<div class="row"><div class="t">+{rel:5.1f}s</div>'
            f'<div class="body" style="--c:{c}">'
            f'<div><span class="lane">{esc(LANE_LABELS.get(s["lane"], s["lane"]))}</span> '
            f'<span class="op">{esc(s["label"])}</span>{dur}</div>'
            f'<div>{detail_html}</div>{out_html}</div></div>')
    rows.append("</div>")
    return legend + "".join(rows)


def render_html(ctx):
    final = ctx.get("final") or {}
    market = ctx.get("market") or {}
    meta = ctx.get("meta") or {}
    ticker = ctx.get("ticker") or "?"
    med, price = final.get("median"), market.get("price")
    gap = None if not (med and price) else (med - price) / price * 100.0
    review = final.get("review_required")
    badge = ('<span class="badge warn">⚠ human review required</span>'
             if review else '<span class="badge ok">✓ within governance band</span>')
    reason = esc(final.get("review_reason", ""))

    gap_txt = ""
    if gap is not None:
        verb = "under-valued" if gap > 0 else "over-valued"
        gap_txt = f' &nbsp;·&nbsp; market {_money(price)} → <b>{abs(gap):.1f}% {verb}</b>'

    risks = meta.get("risk_summary") or []
    risks_html = ""
    if risks:
        risks_html = ("<h2>Qualitative &amp; risk</h2><ul class='risks'>"
                      + "".join(f"<li>{esc(r)}</li>" for r in risks) + "</ul>")
        if meta.get("weights_rationale"):
            risks_html += f"<p class='sub'>Weighting: {esc(meta['weights_rationale'])}</p>"

    norm = meta.get("normalization_notes") or []
    norm_html = ""
    if norm:
        norm_html = ("<h2>Normalization notes</h2><ul class='risks'>"
                     + "".join(f"<li>{esc(n)}</li>" for n in norm)
                     + "</ul><p class='sub'>Non-recurring items the analysts stripped or "
                       "flagged before forecasting recurring earning power.</p>")

    sections = [
        f'<div class="card"><div class="headline">{esc(ticker)} fair value ≈ '
        f'<b>{_money(med)}</b>/share <span class="band">'
        f'(P10–P90: {_money(final.get("p10"))}–{_money(final.get("p90"))})</span>{gap_txt}</div>'
        f'{_band_html(final, market)}'
        f'<div style="margin-top:8px">{badge} <span class="sub" '
        f'style="display:inline">{reason}</span></div></div>',
    ]
    lanes_tbl = _lanes_table(ctx.get("lanes") or [])
    if lanes_tbl:
        sections.append("<h2>Valuation lanes</h2>" + lanes_tbl)
    heat = _heatmap_html(ctx.get("sensitivity"))
    if heat:
        sections.append("<h2>DCF sensitivity — WACC × terminal growth</h2>" + heat)
    if risks_html:
        sections.append(risks_html)
    if norm_html:
        sections.append(norm_html)
    sections.append("<h2>Agent timeline</h2>" + _timeline_html(ctx.get("spans") or []))

    date = ctx.get("date", "")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(ticker)} valuation — {esc(date)}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<h1>{esc(ticker)} — business valuation</h1>
<p class="sub">Generated {esc(date)} · reconciled from DCF, comparables, and qualitative lanes.
All figures produced by Python tools; the LLM agents chose inputs and interpreted outputs.</p>
{''.join(sections)}
<p class="foot">Numbers are educational, not investment advice. Fair value is benchmarked
against a live market quote that was never fed back into any valuation lane.</p>
</div></body></html>"""


# ── I/O glue ──────────────────────────────────────────────────────────────────
def _load(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _load_trace(path):
    p = Path(path)
    if not p.exists():
        return []
    events = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def load_context(cik, ticker=None, trace_path=None, meta_path=None, date=None):
    d = data_dir(cik)
    final = _load(d / "final.json") or {}
    market = _load(d / "market.json") or {}
    meta = _load(meta_path or (d / "report_meta.json")) or {}

    lanes = []
    dcf = _load(d / "dcf_result.json")
    if dcf:
        lanes.append({"label": "DCF (Monte Carlo)", **dcf})
    for src, label in (("comps_llm.json", "Comps · LLM peers"),
                       ("comps_embedding.json", "Comps · embedding peers")):
        c = _load(d / src)
        if c:
            lanes.append({"label": label, **c})
    for lane in lanes:
        key = "dcf" if lane.get("lane") == "dcf" else lane.get("source")
        lane["weight"] = (final.get("weights") or {}).get(key)

    ticker = ticker or final.get("ticker") or market.get("ticker") or meta.get("ticker")
    return {
        "cik": cik_pad(cik), "ticker": ticker,
        "date": date or datetime.date.today().isoformat(),
        "final": final, "market": market, "meta": meta, "lanes": lanes,
        "sensitivity": _load(d / "sensitivity.json"),
        "spans": build_spans(_load_trace(trace_path or PROJECT_ROOT / "data" / "trace.jsonl")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--ticker")
    ap.add_argument("--out", help="output .html path (default reports/<TICKER>-<date>.html)")
    ap.add_argument("--trace", help="path to trace.jsonl")
    ap.add_argument("--meta", help="path to report_meta.json")
    a = ap.parse_args()
    ctx = load_context(a.cik, a.ticker, a.trace, a.meta)
    htm = render_html(ctx)
    out = Path(a.out) if a.out else (PROJECT_ROOT / "reports" /
                                     f"{ctx['ticker'] or ctx['cik']}-{ctx['date']}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(htm)
    emit({"report_html": str(out), "events": len(ctx["spans"]),
          "review_required": ctx["final"].get("review_required")})


if __name__ == "__main__":
    main()
