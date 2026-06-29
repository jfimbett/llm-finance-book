from __future__ import annotations

import re
from pathlib import Path

from .model import Practical, Kind

_PRACTICAL_RE = re.compile(r"^\d{2}-")


def classify(path: Path) -> Kind:
    if (path / ".claude").is_dir():
        return Kind.AGENTIC
    return Kind.NOTEBOOK


def discover(root: Path) -> list:
    out = []
    for child in sorted(root.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or not _PRACTICAL_RE.match(child.name):
            continue
        out.append(Practical(slug=child.name, path=child.resolve(), kind=classify(child)))
    return out


def select(practicals: list, only: str | None) -> list:
    if not only:
        return practicals
    tokens = [t.strip() for t in only.split(",") if t.strip()]
    return [p for p in practicals if any(p.slug.startswith(t) for t in tokens)]
