from tools.metrics import lookup, resolve_key


def test_exact_and_alias_lookup_return_the_right_figure():
    gm = lookup("gross margin")
    assert gm["found"] is True
    assert gm["value"] == "58"
    assert gm["unit"] == "percent"
    assert gm["source"] == "meridian_mdna.txt"


def test_revenue_aliases_resolve_to_same_key():
    assert resolve_key("revenue") == "revenue"
    assert resolve_key("total sales for the year") == "revenue"
    assert lookup("what were total sales")["value"] == "2.40"


def test_longer_phrase_wins_over_substring():
    # "gross margin" must not be captured by the bare "margin" alias
    assert resolve_key("gross margin") == "gross_margin"
    assert resolve_key("operating margin") == "operating_margin"


def test_unknown_metric_is_not_found():
    out = lookup("dividend yield")
    assert out["found"] is False
    assert out["query"] == "dividend yield"
