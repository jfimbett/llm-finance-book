from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Kind(Enum):
    NOTEBOOK = "notebook"
    AGENTIC = "agentic"


@dataclass
class Practical:
    slug: str
    path: Path
    kind: Kind


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    skipped: bool = False


@dataclass
class PracticalResult:
    slug: str
    kind: str
    checks: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.passed or c.skipped for c in self.checks)
