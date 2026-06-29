"""Deterministic tools for the portfolio-construction agent.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the actual optimization and
backtesting so the language model never has to compute anything itself.
"""
