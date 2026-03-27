from __future__ import annotations

from typing import Optional

import yfinance as yf

from packages.shared.contracts.market_data import MarketCandle

DEFAULT_LOOKBACK_BY_INTERVAL = {
    "1D": "6mo",
    "1W": "2y",
    "1M": "10y",
}

YFINANCE_INTERVALS = {
    "1D": "1d",
    "1W": "1wk",
    "1M": "1mo",
}

SYMBOL_ALIASES = {
    "NSE:NIFTY50": "^NSEI",
    "NSE:NIFTYBANK": "^NSEBANK",
}


class YFinanceMarketDataProvider:
    name = "yfinance"

    def fetch_candles(self, symbol: str, interval: str, lookback: Optional[str] = None) -> list[MarketCandle]:
        resolved_symbol = self._normalize_symbol(symbol)
        resolved_interval = YFINANCE_INTERVALS.get(interval.upper(), "1d")
        resolved_lookback = lookback or DEFAULT_LOOKBACK_BY_INTERVAL.get(interval.upper(), "6mo")

        history = yf.Ticker(resolved_symbol).history(
            period=resolved_lookback,
            interval=resolved_interval,
            auto_adjust=False,
            actions=False,
        )
        if history.empty:
            raise ValueError(f"No market data returned for symbol {symbol}")

        candles: list[MarketCandle] = []
        for index, row in history.iterrows():
            timestamp = int(index.to_pydatetime().timestamp())
            candles.append(
                MarketCandle(
                    time=timestamp,
                    open=round(float(row["Open"]), 2),
                    high=round(float(row["High"]), 2),
                    low=round(float(row["Low"]), 2),
                    close=round(float(row["Close"]), 2),
                    volume=round(float(row.get("Volume", 0.0)), 2),
                )
            )
        return candles

    def _normalize_symbol(self, symbol: str) -> str:
        if symbol in SYMBOL_ALIASES:
            return SYMBOL_ALIASES[symbol]

        if ":" in symbol:
            exchange, ticker = symbol.split(":", 1)
            if exchange.upper() == "NSE" and not ticker.startswith("^"):
                return f"{ticker}.NS"
            return ticker

        if self._looks_like_indian_equity(symbol):
            return f"{symbol}.NS"
        return symbol

    def _looks_like_indian_equity(self, symbol: str) -> bool:
        return symbol.isalnum() and symbol.upper() == symbol and len(symbol) <= 15
