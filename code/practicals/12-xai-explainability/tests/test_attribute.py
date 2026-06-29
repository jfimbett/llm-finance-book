import numpy as np
import pytest

from tools._common import applicant_vector, load_applicant, load_model
from tools.attribute import attribute, attribute_applicant, top_negative

APPLICANTS = ["alice", "bob", "carol"]


@pytest.mark.parametrize("name", APPLICANTS)
def test_additivity_holds(name):
    """sum(phi) must equal f(x) - f(baseline) for every applicant (exact linear SHAP)."""
    r = attribute_applicant(name)
    assert r["sum_phi"] == pytest.approx(r["logit"] - r["baseline_logit"], abs=1e-9)


@pytest.mark.parametrize("name", APPLICANTS)
def test_reconstructs_model_output(name):
    """sum(phi) + baseline_logit reproduces the model's own log-odds."""
    r = attribute_applicant(name)
    assert r["sum_phi"] + r["baseline_logit"] == pytest.approx(r["logit"], abs=1e-9)


def test_top_negative_feature_is_delinquencies_for_alice():
    """Alice is crafted so recent delinquencies dominate the denial."""
    r = attribute_applicant("alice")
    assert r["decision"] == "deny"
    top = top_negative(r, k=4)
    assert top[0]["key"] == "delinquencies_24m"
    # and it is genuinely the most negative contribution overall
    assert top[0]["phi"] == min(c["phi"] for c in r["contributions"])


def test_sign_correctness():
    """A feature above its baseline with a negative weight must lower the odds."""
    r = attribute_applicant("carol")
    by_key = {c["key"]: c for c in r["contributions"]}
    # utilization is above baseline (0.88 > 0.30) with weight < 0  -> phi < 0
    assert by_key["credit_utilization"]["phi"] < 0
    # months_employed above baseline (60 > 48) with weight > 0  -> phi > 0
    assert by_key["months_employed"]["phi"] > 0
    # a feature exactly at baseline contributes nothing
    assert by_key["delinquencies_24m"]["value"] == 0.0
    assert by_key["delinquencies_24m"]["phi"] == pytest.approx(0.0, abs=1e-12)


def test_clean_applicant_is_approved():
    r = attribute_applicant("bob")
    assert r["decision"] == "approve"
    assert r["prob"] > r["baseline_prob"]


def test_baseline_applicant_has_zero_attributions():
    """An applicant equal to the baseline gets all-zero phi and f(x) == f(baseline)."""
    from tools._common import feature_arrays
    model = load_model()
    _, _, baselines = feature_arrays(model)
    r = attribute(model, baselines.copy())
    assert all(c["phi"] == pytest.approx(0.0, abs=1e-12) for c in r["contributions"])
    assert r["logit"] == pytest.approx(r["baseline_logit"], abs=1e-12)


def test_protected_attributes_never_enter_the_vector():
    """The applicant file carries protected fields; the model vector must ignore them."""
    model = load_model()
    applicant = load_applicant("alice")
    assert "protected" in applicant  # the data file does carry them
    x = applicant_vector(model, applicant)
    assert len(x) == len(model["features"])  # exactly the model's own features, nothing else
