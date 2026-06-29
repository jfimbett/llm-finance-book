"""Deterministic tools for the iterate-to-target agent.

The agent (Claude Code / Cline) drafts and revises text; it never decides whether
the target is met. These modules compute the metric and the pass/fail gate so the
language model can only ever *react* to a number it did not produce.
"""
