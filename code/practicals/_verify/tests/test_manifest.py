from __future__ import annotations

import pytest

from _verify.manifest import load_manifest, Manifest, LiveCheck


def test_missing_manifest_returns_empty(tmp_path):
    m = load_manifest(tmp_path)
    assert m == Manifest(smoke=[], live=[])


def test_loads_smoke_and_live(tmp_path):
    (tmp_path / "verify.yaml").write_text(
        "smoke:\n"
        "  - python -m tools.retrieve \"q\" -k 4 > reports/_context.json\n"
        "live:\n"
        "  - prompt: '/ask \"risk?\"'\n"
        "    expect_file: 'reports/*.md'\n"
        "    expect_contains: ['concentration']\n"
        "  - prompt: '/ask \"net income?\"'\n"
        "    expect_not_contains: ['$']\n"
    )
    m = load_manifest(tmp_path)
    assert m.smoke == ['python -m tools.retrieve "q" -k 4 > reports/_context.json']
    assert m.live[0] == LiveCheck(prompt='/ask "risk?"', expect_file='reports/*.md',
                                  expect_contains=['concentration'])
    assert m.live[1].expect_not_contains == ['$']


def test_live_item_without_prompt_raises(tmp_path):
    (tmp_path / "verify.yaml").write_text("live:\n  - expect_contains: ['x']\n")
    with pytest.raises(ValueError, match="prompt"):
        load_manifest(tmp_path)
