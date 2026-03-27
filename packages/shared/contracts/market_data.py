from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    symbol: str
    price: float
    change_pct: float
    signal: str
    generated_at: datetime
