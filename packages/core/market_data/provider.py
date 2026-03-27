from __future__ import annotations

from typing import Optional, Protocol

from packages.shared.contracts.market_data import MarketCandle


class MarketDataProvider(Protocol):
    name: str

    def fetch_candles(self, symbol: str, interval: str, lookback: Optional[str] = None) -> list[MarketCandle]:
        ...
