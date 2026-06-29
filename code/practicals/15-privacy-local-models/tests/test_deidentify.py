from tools.deidentify import detect, deidentify
from tools._common import load_doc


def test_detects_all_seeded_pii_types():
    types = {e["type"] for e in detect(load_doc())}
    assert {"EMAIL", "SSN", "PHONE", "PERSON", "ACCOUNT"} <= types


def test_email_is_redacted():
    out = deidentify(load_doc())["redacted"]
    assert "james.whitfield@example.com" not in out
    assert "[EMAIL]" in out


def test_ssn_is_redacted():
    out = deidentify(load_doc())["redacted"]
    assert "123-45-6789" not in out
    assert "[SSN]" in out


def test_phone_is_redacted():
    out = deidentify(load_doc())["redacted"]
    assert "415-555-0199" not in out
    assert "[PHONE]" in out


def test_person_names_are_redacted():
    out = deidentify(load_doc())["redacted"]
    for name in ("James Whitfield", "Maria Delgado", "Alan Pierce"):
        assert name not in out
    assert "[PERSON]" in out


def test_account_number_is_redacted():
    out = deidentify(load_doc())["redacted"]
    assert "NVC-88421003" not in out
    assert "[ACCOUNT]" in out


def test_benign_sentence_is_not_overredacted():
    benign = "The quarterly compliance report was approved by the committee on schedule."
    result = deidentify(benign)
    assert result["entities"] == []
    assert result["redacted"] == benign
