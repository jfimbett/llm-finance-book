import pytest

from tools.attribute import attribute_applicant
from tools.check import check_additivity

APPLICANTS = ["alice", "bob", "carol"]


@pytest.mark.parametrize("name", APPLICANTS)
def test_additivity_gate_passes_on_real_attribution(name):
    r = attribute_applicant(name)
    chk = check_additivity(r)
    assert chk["ok"]
    assert chk["gap"] <= chk["tolerance"]


def test_gate_fails_when_an_attribution_is_tampered_with():
    """If a phi is corrupted, the additivity gate must catch it."""
    r = attribute_applicant("alice")
    r["sum_phi"] += 0.5  # pretend an explanation dropped or distorted a feature
    chk = check_additivity(r)
    assert not chk["ok"]
    assert chk["gap"] == pytest.approx(0.5, abs=1e-9)
