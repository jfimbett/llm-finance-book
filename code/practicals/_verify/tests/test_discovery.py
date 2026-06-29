from __future__ import annotations

from pathlib import Path

from _verify.discovery import discover, classify, select
from _verify.model import Kind


def _make_tree(tmp_path: Path) -> Path:
    root = tmp_path / "practicals"
    (root / "01-intro").mkdir(parents=True)
    (root / "01-intro" / "practical.ipynb").write_text("{}")
    (root / "04-llm-agents" / ".claude").mkdir(parents=True)
    (root / "_verify").mkdir()           # must be ignored (no NN- prefix)
    (root / "notes.md").write_text("x")  # files ignored
    return root


def test_discover_finds_and_classifies(tmp_path):
    found = discover(_make_tree(tmp_path))
    slugs = [p.slug for p in found]
    assert slugs == ["01-intro", "04-llm-agents"]
    kinds = {p.slug: p.kind for p in found}
    assert kinds["01-intro"] is Kind.NOTEBOOK
    assert kinds["04-llm-agents"] is Kind.AGENTIC


def test_classify_agentic_when_claude_dir_present(tmp_path):
    d = tmp_path / "04-x"
    (d / ".claude").mkdir(parents=True)
    assert classify(d) is Kind.AGENTIC


def test_select_filters_by_prefix(tmp_path):
    found = discover(_make_tree(tmp_path))
    picked = select(found, "04")
    assert [p.slug for p in picked] == ["04-llm-agents"]
    assert select(found, None) == found
