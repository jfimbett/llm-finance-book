import pytest

from tools._common import load_filing_text
from tools.extract import SchemaError, extract, validate, validate_or_raise


def test_clean_extraction_passes_validation():
    rec = extract(load_filing_text())
    assert validate(rec) == []
    assert validate_or_raise(rec) is rec


def test_missing_required_field_is_rejected():
    rec = extract(load_filing_text())
    rec.pop("eps")
    errors = validate(rec)
    assert any("eps" in e for e in errors)
    with pytest.raises(SchemaError):
        validate_or_raise(rec)


def test_wrong_type_is_rejected():
    rec = extract(load_filing_text())
    rec["gross_margin"]["value"] = "fifty-eight percent"  # string where a number is required
    errors = validate(rec)
    assert any("gross_margin" in e and "number" in e for e in errors)


def test_out_of_range_value_is_rejected():
    rec = extract(load_filing_text())
    rec["gross_margin"]["value"] = 580.0  # a margin of 580% is impossible
    errors = validate(rec)
    assert any("gross_margin" in e for e in errors)
