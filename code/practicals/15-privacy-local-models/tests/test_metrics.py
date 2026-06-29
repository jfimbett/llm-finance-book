from tools.deidentify import deidentify
from tools.metrics import privacy, utility, tradeoff
from tools._common import load_doc, seeded_pii_values


def test_privacy_is_one_when_all_seeded_pii_removed():
    redacted = deidentify(load_doc())["redacted"]
    assert privacy(redacted, seeded_pii_values()) == 1.0


def test_privacy_below_one_when_nothing_is_redacted():
    # The untouched document still contains every identifier.
    assert privacy(load_doc(), seeded_pii_values()) < 1.0


def test_utility_is_one_on_clean_text():
    clean = "The quarterly compliance report was approved by the committee on schedule."
    redacted = deidentify(clean)["redacted"]
    assert utility(clean, redacted, seeded_pii_values()) == 1.0


def test_utility_stays_high_after_redacting_the_document():
    text = load_doc()
    redacted = deidentify(text)["redacted"]
    assert utility(text, redacted, seeded_pii_values()) >= 0.9


def test_tradeoff_reports_both_numbers():
    text = load_doc()
    redacted = deidentify(text)["redacted"]
    scores = tradeoff(text, redacted, seeded_pii_values())
    assert scores["privacy"] == 1.0
    assert scores["utility"] >= 0.9
