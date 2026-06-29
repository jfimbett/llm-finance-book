"""Deterministic AML screening tools for the transaction-screening agent.

The agent (Claude Code / Cline) chooses *which* rule to run and *interprets*
the flags; these modules do every bit of the actual detection so the language
model never has to judge an amount, a date window, or a country itself.
"""
