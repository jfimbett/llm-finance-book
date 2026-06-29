from __future__ import annotations

from pathlib import Path

from _verify.model import Kind, Practical, CheckResult, PracticalResult


def test_practical_holds_slug_path_kind():
    p = Practical(slug="04-llm-agents", path=Path("/tmp/04"), kind=Kind.AGENTIC)
    assert p.slug == "04-llm-agents"
    assert p.kind is Kind.AGENTIC


def test_practical_result_ok_true_when_all_pass_or_skip():
    checks = [
        CheckResult(name="config-lint", passed=True),
        CheckResult(name="pytest", passed=False, skipped=True),
    ]
    result = PracticalResult(slug="04-llm-agents", kind="agentic", checks=checks)
    assert result.ok is True


def test_practical_result_ok_false_on_real_failure():
    checks = [CheckResult(name="config-lint", passed=False, detail="bad json")]
    result = PracticalResult(slug="04-llm-agents", kind="agentic", checks=checks)
    assert result.ok is False
