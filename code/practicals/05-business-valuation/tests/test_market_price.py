import market_price


def fake_fetcher(ticker):
    return {"ticker": ticker.upper(), "price": 123.45,
            "market_cap": 2.0e12, "currency": "USD"}


def test_get_price_uses_injected_fetcher():
    out = market_price.get_price("aapl", fetcher=fake_fetcher)
    assert out["ticker"] == "AAPL"
    assert out["price"] == 123.45
    assert out["currency"] == "USD"
