from __future__ import annotations

import math
from datetime import datetime, timezone

from fastapi import APIRouter

from packages.shared.contracts.market_data import MarketSnapshot

router = APIRouter(prefix="/market-data", tags=["market-data"])
DEFAULT_SYMBOL = "NSE:NIFTY50"


def build_market_snapshot(symbol: str = DEFAULT_SYMBOL, tick: int = 0) -> MarketSnapshot:
    now = datetime.now(timezone.utc)
    base_price = 24550.0
    intraday_wave = math.sin((now.timestamp() / 300.0) + (tick / 4.0)) * 42
    price = round(base_price + intraday_wave + (tick * 0.35), 2)
    change_pct = round(((price - base_price) / base_price) * 100, 2)
    return MarketSnapshot(
        symbol=symbol,
        price=price,
        change_pct=change_pct,
        signal="watch" if change_pct >= 0 else "hedge",
        generated_at=now,
    )


@router.get("/snapshot", response_model=MarketSnapshot)
async def get_market_snapshot() -> MarketSnapshot:
    return build_market_snapshot()
