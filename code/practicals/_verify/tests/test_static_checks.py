from __future__ import annotations

from pathlib import Path

from _verify.static_checks import parse_frontmatter, lint_config, check_references


def _agentic(tmp_path: Path) -> Path:
    d = tmp_path / "04-x"
    (d / ".claude" / "skills" / "ask").mkdir(parents=True)
    (d / ".claude" / "agents").mkdir(parents=True)
    (d / "tools").mkdir()
    (d / "data" / "corpus").mkdir(parents=True)
    (d / ".claude" / "settings.json").write_text('{"permissions": {}}')
    (d / ".claude" / "skills" / "ask" / "SKILL.md").write_text(
        "---\nname: ask\ndescription: Ask a question\n---\nRun python -m tools.retrieve and read data/corpus/x.txt\n"
    )
    (d / ".claude" / "agents" / "retriever.md").write_text(
        "---\nname: retriever\ndescription: Retrieves chunks\n---\nbody\n"
    )
    (d / "tools" / "retrieve.py").write_text("x = 1\n")
    (d / "data" / "corpus" / "x.txt").write_text("hello")
    (d / "CLAUDE.md").write_text("Use tools.retrieve only.\n")
    return d


def test_parse_frontmatter_reads_mapping():
    fm = parse_frontmatter("---\nname: ask\ndescription: d\n---\nbody")
    assert fm == {"name": "ask", "description": "d"}
    assert parse_frontmatter("no frontmatter here") is None


def test_lint_config_passes_on_good_tree(tmp_path):
    assert lint_config(_agentic(tmp_path)).passed is True


def test_lint_config_fails_on_bad_json(tmp_path):
    d = _agentic(tmp_path)
    (d / ".claude" / "settings.json").write_text("{not json")
    res = lint_config(d)
    assert res.passed is False
    assert "settings.json" in res.detail


def test_lint_config_fails_on_missing_description(tmp_path):
    d = _agentic(tmp_path)
    (d / ".claude" / "skills" / "ask" / "SKILL.md").write_text("---\nname: ask\n---\nbody")
    res = lint_config(d)
    assert res.passed is False
    assert "description" in res.detail


def test_check_references_passes_when_targets_exist(tmp_path):
    assert check_references(_agentic(tmp_path)).passed is True


def test_check_references_fails_on_dangling_tool(tmp_path):
    d = _agentic(tmp_path)
    (d / "tools" / "retrieve.py").unlink()
    res = check_references(d)
    assert res.passed is False
    assert "retrieve" in res.detail


def test_lint_and_refs_tolerate_missing_agents_dir(tmp_path):
    import shutil
    d = _agentic(tmp_path)
    shutil.rmtree(d / ".claude" / "agents")
    assert lint_config(d).passed is True
    assert check_references(d).passed is True
