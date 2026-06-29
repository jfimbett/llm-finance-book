from tools.aggregate import score_records, daily_signal, label, build_signal


def test_known_inputs_give_known_daily_mean():
    records = [
        # 2024-01-02: +1.0 and -1.0  -> mean 0.0
        {"date": "2024-01-02", "id": "a", "text": "beats record growth"},
        {"date": "2024-01-02", "id": "b", "text": "loss decline lawsuit"},
        # 2024-01-03: +1.0 only       -> mean 1.0
        {"date": "2024-01-03", "id": "c", "text": "profit growth"},
    ]
    sig = daily_signal(score_records(records))
    assert sig["2024-01-02"]["mean"] == 0.0
    assert sig["2024-01-02"]["count"] == 2
    assert sig["2024-01-03"]["mean"] == 1.0


def test_labels_follow_the_threshold():
    assert label(0.5) == "bullish"
    assert label(-0.5) == "bearish"
    assert label(0.0) == "neutral"
    assert label(0.1) == "neutral"   # below the 0.15 band


def test_item_ids_are_preserved_per_date():
    records = [
        {"date": "D", "id": "x", "text": "growth"},
        {"date": "D", "id": "y", "text": "loss"},
    ]
    sig = daily_signal(score_records(records))
    assert sig["D"]["item_ids"] == ["x", "y"]


def test_bundled_signal_has_three_dated_groups():
    out = build_signal()
    assert set(out["by_date"]) == {"2024-02-12", "2024-02-13", "2024-02-14"}
    # the bundled headlines are engineered as a bullish, a bearish and a neutral day
    assert out["by_date"]["2024-02-12"]["label"] == "bullish"
    assert out["by_date"]["2024-02-13"]["label"] == "bearish"
    assert out["by_date"]["2024-02-14"]["label"] == "neutral"
    assert len(out["headlines"]) == 9
