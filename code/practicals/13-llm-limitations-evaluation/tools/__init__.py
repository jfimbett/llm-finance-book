"""Deterministic tools for the evaluation-harness agent.

The agent (Claude Code / Cline) chooses *which* eval set to run and *interprets*
the numbers; these modules compute every metric — exact-match accuracy, token-F1,
and Expected Calibration Error — so the language model never scores itself.
"""
