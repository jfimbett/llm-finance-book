"""Deterministic tools for the sentiment-signal agent.

The agent (Claude Code / Cline) chooses *which* headlines to score and
*interprets* the daily signal; these modules do every bit of the actual
polarity scoring and aggregation so the language model never computes or
recalls a number itself.
"""
