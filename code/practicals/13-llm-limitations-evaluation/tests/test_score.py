from tools.score import exact_match, token_f1, score_dataset
from tools._common import load_gold, load_predictions
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def test_token_f1_full_overlap_is_one():
    assert token_f1("gross margin was 64%", "gross margin was 64%") == 1.0


def test_token_f1_partial_overlap_is_between_zero_and_one():
    f1 = token_f1("gross margin 64%", "gross margin 61%")
    assert 0.0 < f1 < 1.0
    # two of three tokens shared on each side -> 2/3
    assert abs(f1 - 2 / 3) < 1e-9


def test_token_f1_zero_overlap_is_zero():
    assert token_f1("hardware revenue", "cloud services") == 0.0


def test_exact_match_is_normalised():
    assert exact_match("US Dollars", "us dollars") == 1
    assert exact_match("1.4 billion dollars", "1.14 billion dollars") == 0


def test_accuracy_counts_correct_items():
    gold = load_gold(DATA / "gold.json")
    preds = load_predictions(DATA / "candidates_overconfident.json")
    res = score_dataset(gold, preds)
    # q1, q2, q4, q7, q9 are right; the other five are wrong
    assert res["n"] == 10
    assert res["n_correct"] == 5
    assert res["accuracy"] == 0.5
    correct_ids = {i["id"] for i in res["items"] if i["correct"]}
    assert correct_ids == {"q1", "q2", "q4", "q7", "q9"}


def test_calibrated_model_is_more_accurate():
    gold = load_gold(DATA / "gold.json")
    over = score_dataset(gold, load_predictions(DATA / "candidates_overconfident.json"))
    cal = score_dataset(gold, load_predictions(DATA / "candidates_calibrated.json"))
    assert cal["accuracy"] > over["accuracy"]
