from tools._common import load_filing_text
from tools.extract import extract


def test_each_field_extracted_with_correct_value():
    rec = extract(load_filing_text())
    assert rec["revenue"]["value"] == "$1.46 billion"
    assert rec["gross_margin"]["value"] == 58.0
    assert rec["eps"]["value"] == 1.27
    assert rec["guidance"]["value"] == "$5.90 billion to $6.10 billion"


def test_each_field_records_its_source_span():
    rec = extract(load_filing_text())
    norm = " ".join(load_filing_text().split())
    for field, entry in rec.items():
        start, end = entry["span"]
        sliced = norm[start:end]
        # the recorded span must slice the captured figure back out of the source,
        # and that slice must sit inside the human-readable source snippet
        assert sliced and sliced in entry["source"], field


def test_distractor_percentages_do_not_capture_the_wrong_field():
    # '54%' (prior-year margin) and '22%' (revenue growth) must not be picked up as
    # gross_margin / guidance — the patterns are anchored to their labels.
    rec = extract(load_filing_text())
    assert rec["gross_margin"]["value"] == 58.0
    assert "5.90 billion to $6.10 billion" in rec["guidance"]["source"]
