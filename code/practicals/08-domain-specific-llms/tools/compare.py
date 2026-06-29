"""Compare the general-purpose and finance-domain classifiers on the labelled finance set.

Reports each classifier's accuracy against the gold labels, names the winner and the
margin, and lists the finance sentences where the domain classifier wins — with the
deciding terms (the tokens the general lexicon scores wrongly or has never seen).

CLI:
    python -m tools.compare           # human-readable summary
    python -m tools.compare --json    # machine-readable, for the /compare skill
"""
from __future__ import annotations

import argparse
import json

from tools import domain, general
from tools._common import accuracy, load_sentences, tokenize


def _deciding_terms(text: str) -> list[dict]:
    """Tokens whose general vs domain polarity differs — the reason a verdict flips.

    A term counts as deciding when the two lexicons disagree on its score, including the
    case where the general lexicon has never seen it (treated as 0)."""
    gen_lex = general.LEXICON
    dom_lex = domain.LEXICON
    out: list[dict] = []
    for tok in dict.fromkeys(tokenize(text)):  # de-duplicate, keep order
        g = gen_lex.get(tok)
        d = dom_lex.get(tok)
        if (g or 0) != (d or 0):
            out.append({
                "term": tok,
                "general": "absent" if g is None else g,
                "domain": "absent" if d is None else d,
            })
    return out


def compare() -> dict:
    rows = load_sentences()
    gold = [r["label"] for r in rows]
    gen_pred = general.predict_all(rows)
    dom_pred = domain.predict_all(rows)

    gen_acc = accuracy(gen_pred, gold)
    dom_acc = accuracy(dom_pred, gold)

    domain_wins = []
    for r, g, d in zip(rows, gen_pred, dom_pred):
        if d == r["label"] and g != r["label"]:
            domain_wins.append({
                "id": r["id"],
                "text": r["text"],
                "gold": r["label"],
                "general_pred": g,
                "domain_pred": d,
                "deciding_terms": _deciding_terms(r["text"]),
            })

    if dom_acc > gen_acc:
        winner = "domain"
    elif gen_acc > dom_acc:
        winner = "general"
    else:
        winner = "tie"

    return {
        "n_sentences": len(rows),
        "general_accuracy": round(gen_acc, 4),
        "domain_accuracy": round(dom_acc, 4),
        "winner": winner,
        "margin": round(abs(dom_acc - gen_acc), 4),
        "domain_wins": domain_wins,
    }


def _format(result: dict) -> str:
    lines = [
        f"Compared {result['n_sentences']} labelled finance sentences.",
        f"  general-purpose accuracy : {result['general_accuracy']:.3f}",
        f"  finance-domain  accuracy : {result['domain_accuracy']:.3f}",
        f"  winner: {result['winner'].upper()}  (margin {result['margin']:.3f})",
    ]
    if result["domain_wins"]:
        lines.append("")
        lines.append("Sentences the domain classifier got right and the general one missed:")
        for w in result["domain_wins"]:
            terms = ", ".join(
                f"{t['term']} (general={t['general']}, domain={t['domain']})"
                for t in w["deciding_terms"]
            ) or "—"
            lines.append(f"  [{w['id']}] gold={w['gold']}  general={w['general_pred']}  domain={w['domain_pred']}")
            lines.append(f"        \"{w['text']}\"")
            lines.append(f"        deciding terms: {terms}")
    return "\n".join(lines)


def _main() -> None:
    ap = argparse.ArgumentParser(description="Compare general vs finance-domain classifiers.")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a text summary")
    args = ap.parse_args()
    result = compare()
    print(json.dumps(result, indent=2) if args.json else _format(result))


if __name__ == "__main__":
    _main()
