from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    symbol: str
    price: float
    change_pct: float
    signal: str
    generated_at: datetime


class MarketCandle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketCandlesResponse(BaseModel):
    symbol: str
    interval: str
    provider: Optional[str] = None
    source: str
    candles: list[MarketCandle]
