from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class LiveCheck:
    prompt: str
    expect_file: str | None = None
    expect_contains: list = field(default_factory=list)
    expect_not_contains: list = field(default_factory=list)


@dataclass
class Manifest:
    smoke: list = field(default_factory=list)
    live: list = field(default_factory=list)


def _parse_live(item: dict) -> LiveCheck:
    if not isinstance(item, dict) or "prompt" not in item:
        raise ValueError(f"live check is missing required 'prompt': {item!r}")
    return LiveCheck(
        prompt=item["prompt"],
        expect_file=item.get("expect_file"),
        expect_contains=list(item.get("expect_contains", []) or []),
        expect_not_contains=list(item.get("expect_not_contains", []) or []),
    )


def load_manifest(practical_path: Path) -> Manifest:
    f = practical_path / "verify.yaml"
    if not f.exists():
        return Manifest(smoke=[], live=[])
    data = yaml.safe_load(f.read_text()) or {}
    smoke = [str(c) for c in (data.get("smoke", []) or [])]
    live = [_parse_live(item) for item in (data.get("live", []) or [])]
    return Manifest(smoke=smoke, live=live)
