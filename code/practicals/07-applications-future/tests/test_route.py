from tools.route import classify


def test_metric_value_question_routes_to_metrics():
    assert classify("What was Meridian's revenue in fiscal 2025?")["route"] == "metrics"
    assert classify("What is the company's gross margin?")["route"] == "metrics"
    assert classify("How much free cash flow did they generate?")["route"] == "metrics"


def test_disclosure_question_routes_to_filings():
    assert classify("What are the main risk factors in the latest 10-K?")["route"] == "filings"
    assert classify("What supply chain risks does Meridian disclose?")["route"] == "filings"


def test_event_question_routes_to_news():
    assert classify("What partnership did Meridian recently announce?")["route"] == "news"
    assert classify("Was there a product recall in the news?")["route"] == "news"


def test_empty_or_unknown_question_defaults_to_filings():
    assert classify("Tell me everything.")["route"] == "filings"


def test_scores_are_reported_for_inspection():
    out = classify("What was net income?")
    assert out["scores"]["metrics"] >= out["scores"]["filings"]
    assert out["value_seeking"] is True
