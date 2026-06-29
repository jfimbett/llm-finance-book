from tools.lexicon import score


def test_clearly_positive_scores_above_zero():
    assert score("NovaCorp beats estimates as revenue hits record growth")["polarity"] > 0


def test_clearly_negative_scores_below_zero():
    assert score("NovaCorp posts a steep loss amid a fraud investigation")["polarity"] < 0


def test_neutral_text_scores_zero():
    s = score("NovaCorp schedules its annual shareholder meeting for May")
    assert s["polarity"] == 0.0
    assert s["n_sentiment"] == 0


def test_negation_flips_the_sign():
    plain = score("NovaCorp beat revenue estimates")["polarity"]
    negated = score("NovaCorp did not beat revenue estimates")["polarity"]
    assert plain > 0
    assert negated < 0


def test_intensifier_amplifies_magnitude():
    plain = score("NovaCorp reported gains")["polarity"]
    intensified = score("NovaCorp reported strong gains")["polarity"]
    assert intensified > plain > 0


def test_mixed_headline_nets_toward_zero():
    # one positive ('profit') and one negative ('misses') cancel
    assert score("NovaCorp profit misses forecasts")["polarity"] == 0.0
