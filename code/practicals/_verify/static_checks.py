from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .model import CheckResult

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_TOOLS_RE = re.compile(r"tools\.([a-zA-Z_][a-zA-Z0-9_]*)")
_DATA_RE = re.compile(r"(data/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)")


def parse_frontmatter(text: str) -> dict | None:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    loaded = yaml.safe_load(m.group(1))
    return loaded if isinstance(loaded, dict) else None


def _doc_files(practical_dir: Path) -> list:
    docs = []
    claude_md = practical_dir / "CLAUDE.md"
    if claude_md.exists():
        docs.append(claude_md)
    docs.extend(sorted((practical_dir / ".claude" / "skills").rglob("SKILL.md")))
    return docs


def lint_config(practical_dir: Path) -> CheckResult:
    problems = []

    settings = practical_dir / ".claude" / "settings.json"
    if settings.exists():
        try:
            json.loads(settings.read_text())
        except json.JSONDecodeError as exc:
            problems.append(f".claude/settings.json: invalid JSON ({exc})")

    md_files = sorted((practical_dir / ".claude" / "skills").rglob("SKILL.md"))
    md_files += sorted((practical_dir / ".claude" / "agents").glob("*.md"))
    for md in md_files:
        fm = parse_frontmatter(md.read_text())
        rel = md.relative_to(practical_dir)
        if fm is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        for key in ("name", "description"):
            if not str(fm.get(key, "")).strip():
                problems.append(f"{rel}: missing '{key}'")

    return CheckResult(name="config-lint", passed=not problems, detail="; ".join(problems))


def check_references(practical_dir: Path) -> CheckResult:
    missing = []
    for doc in _doc_files(practical_dir):
        text = doc.read_text()
        for mod in sorted(set(_TOOLS_RE.findall(text))):
            if not (practical_dir / "tools" / f"{mod}.py").exists():
                missing.append(f"tools.{mod} (in {doc.name})")
        for data_ref in sorted(set(_DATA_RE.findall(text))):
            if not (practical_dir / data_ref).exists():
                missing.append(f"{data_ref} (in {doc.name})")
    return CheckResult(name="references", passed=not missing, detail="; ".join(sorted(set(missing))))
