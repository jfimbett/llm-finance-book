"""Deterministic tools for the credit-decision explanation agent.

The agent (Claude Code / Cline) chooses *which* applicant to explain and
*interprets* the result; these modules do every bit of the actual feature
attribution and additivity checking, so the language model never computes an
attribution itself.
"""
