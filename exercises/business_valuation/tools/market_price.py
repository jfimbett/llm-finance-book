import argparse

from _common import data_dir, die, emit, write_json


def _yfinance_fetch(ticker):
    import yfinance as yf
    t = yf.Ticker(ticker)
    fast = {}
    try:
        fast = dict(t.fast_info)
    except Exception:
        fast = {}
    price = fast.get("last_price") or fast.get("lastPrice")
    if price is None:
        hist = t.history(period="1d")
        if hist.empty:
            die(f"no market price available for {ticker}")
        price = float(hist["Close"].iloc[-1])
    return {
        "ticker": ticker.upper(),
        "price": float(price),
        "market_cap": float(fast["market_cap"]) if fast.get("market_cap") else None,
        "currency": fast.get("currency", "USD"),
    }


def get_price(ticker, fetcher=None):
    fetcher = fetcher or _yfinance_fetch
    return fetcher(ticker)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--cik")
    a = ap.parse_args()
    out = get_price(a.ticker)
    if a.cik:
        write_json(data_dir(a.cik) / "market.json", out)
    emit(out)


if __name__ == "__main__":
    main()
