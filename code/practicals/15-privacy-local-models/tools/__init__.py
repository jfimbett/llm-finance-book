"""Deterministic tools for the PII de-identification agent.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the actual detection, redaction, and
metric computation so the language model never decides what counts as PII or how
much privacy was gained.
"""
