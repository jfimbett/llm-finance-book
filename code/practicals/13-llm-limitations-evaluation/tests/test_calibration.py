from tools.calibration import (
    expected_calibration_error,
    confident_wrong,
    reliability_bins,
    analyze,
)
from tools.score import score_dataset
from tools._common import load_gold, load_predictions
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def _items(pred_file):
    gold = load_gold(DATA / "gold.json")
    return score_dataset(gold, load_predictions(DATA / pred_file))["items"]


def test_ece_is_higher_for_overconfident_than_calibrated():
    over = expected_calibration_error(_items("candidates_overconfident.json"))
    cal = expected_calibration_error(_items("candidates_calibrated.json"))
    assert over > cal
    # the overconfident model's confidence is badly out of line with reality
    assert over > 0.25
    # the calibrated model's confidence roughly tracks its accuracy
    assert cal < 0.2


def test_confident_wrong_flags_overconfident_failures():
    flagged = confident_wrong(_items("candidates_overconfident.json"), threshold=0.8)
    ids = {f["id"] for f in flagged}
    # q3, q5, q6, q8, q10 are wrong yet asserted at confidence >= 0.8
    assert ids == {"q3", "q5", "q6", "q8", "q10"}
    # every flagged item is genuinely wrong and genuinely confident
    for f in flagged:
        assert f["confidence"] >= 0.8
        assert f["candidate"] != f["gold"]


def test_calibrated_model_has_no_confident_wrong_cases():
    flagged = confident_wrong(_items("candidates_calibrated.json"), threshold=0.8)
    assert flagged == []


def test_reliability_bins_partition_all_predictions():
    bins = reliability_bins(_items("candidates_overconfident.json"), n_bins=10)
    assert sum(b["count"] for b in bins) == 10


def test_perfect_calibration_has_zero_ece():
    # accuracy equals confidence in every bin -> ECE 0
    items = [
        {"id": "a", "confidence": 1.0, "correct": True},
        {"id": "b", "confidence": 0.0, "correct": False},
    ]
    assert expected_calibration_error(items) == 0.0


def test_analyze_reports_the_headline_numbers():
    rep = analyze(_items("candidates_overconfident.json"))
    assert rep["n"] == 10
    assert rep["accuracy"] == 0.5
    assert rep["mean_confidence"] > 0.85
    assert rep["ece"] > 0.25
    assert len(rep["confident_wrong"]) == 5
