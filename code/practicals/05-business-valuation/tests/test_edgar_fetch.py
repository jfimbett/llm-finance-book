import pytest
import edgar_fetch


def test_resolve_cik_found():
    m = {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
    assert edgar_fetch.resolve_cik("aapl", m) == "0000320193"


def test_resolve_cik_missing_dies():
    with pytest.raises(SystemExit):
        edgar_fetch.resolve_cik("ZZZZ", {"0": {"cik_str": 1, "ticker": "AAPL"}})


def test_strip_html_removes_tags_and_collapses_space():
    html = "<html><body><p>Risk&nbsp;Factors:   competition</p></body></html>"
    assert edgar_fetch.strip_html(html) == "Risk Factors: competition"
