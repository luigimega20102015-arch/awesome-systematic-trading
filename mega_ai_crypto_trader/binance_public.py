"""Read-only Binance Spot market data, using public unsigned endpoints."""
import json
from urllib.request import Request, urlopen

BASE_URL = "https://api.binance.com"
ALLOWED = frozenset({"BTCUSDT", "ETHUSDT"})

def get_public_ticker(symbol: str, opener=urlopen) -> dict:
    if symbol not in ALLOWED:
        raise ValueError("Unsupported symbol")
    request = Request(BASE_URL + "/api/v3/ticker/price?symbol=" + symbol,
                      headers={"User-Agent": "MegaCryptoPaper/0.1"})
    with opener(request, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("symbol") != symbol or float(payload.get("price", 0)) <= 0:
        raise ValueError("Invalid Binance public ticker")
    return {"symbol": symbol, "price": str(payload["price"])}

if __name__ == "__main__":
    for pair in ("BTCUSDT", "ETHUSDT"):
        print(get_public_ticker(pair))
