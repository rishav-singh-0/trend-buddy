from __future__ import annotations

import hashlib
import math
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException

from packages.core.market_data import create_market_data_service
from packages.shared.contracts.market_data import MarketCandle, MarketCandlesResponse, MarketSnapshot

router = APIRouter(prefix="/market-data", tags=["market-data"])
DEFAULT_SYMBOL = "NSE:NIFTY50"
market_data_service = create_market_data_service()


def _symbol_seed(symbol: str) -> int:
    return int(hashlib.sha256(symbol.encode("utf-8")).hexdigest()[:8], 16)


def _symbol_base_price(symbol: str) -> float:
    if symbol == DEFAULT_SYMBOL:
        return 24_550.0
    return 450.0 + (_symbol_seed(symbol) % 2_200)


def build_market_snapshot(symbol: str = DEFAULT_SYMBOL, tick: int = 0) -> MarketSnapshot:
    now = datetime.now(timezone.utc)
    base_price = _symbol_base_price(symbol)
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


def build_market_candles(
    symbol: str = DEFAULT_SYMBOL, interval: str = "1D", bars: int = 160
) -> MarketCandlesResponse:
    now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    base_price = _symbol_base_price(symbol)
    seed = _symbol_seed(symbol)
    drift = ((seed % 17) - 8) * 0.18
    candles: list[MarketCandle] = []
    previous_close = base_price

    for offset in range(max(bars, 10)):
        current_time = now - timedelta(days=(bars - offset))
        wave = math.sin((offset / 7.0) + (seed % 11)) * (base_price * 0.012)
        trend = offset * drift
        open_price = previous_close + (wave * 0.16)
        close_price = base_price + wave + trend
        high_price = max(open_price, close_price) + abs(math.cos(offset / 3.0) * (base_price * 0.006))
        low_price = min(open_price, close_price) - abs(math.sin(offset / 2.7) * (base_price * 0.005))
        volume = 1_000_000 + ((seed % 90_000) * 3) + (offset * 4_800)

        candle = MarketCandle(
            time=int(current_time.timestamp()),
            open=round(open_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2),
            close=round(close_price, 2),
            volume=round(volume, 2),
        )
        candles.append(candle)
        previous_close = candle.close

    return MarketCandlesResponse(symbol=symbol, interval=interval, provider=None, source="synthetic", candles=candles)


@router.get("/snapshot", response_model=MarketSnapshot)
async def get_market_snapshot(symbol: str = DEFAULT_SYMBOL) -> MarketSnapshot:
    return build_market_snapshot(symbol=symbol)


@router.get("/providers")
async def get_market_data_providers() -> dict[str, list[str]]:
    return {"providers": [provider.name for provider in market_data_service.list_providers()]}


@router.get("/candles", response_model=MarketCandlesResponse)
async def get_market_candles(
    symbol: str = DEFAULT_SYMBOL,
    interval: str = "1D",
    provider: Optional[str] = None,
    lookback: Optional[str] = None,
    refresh: bool = False,
) -> MarketCandlesResponse:
    try:
        response = market_data_service.get_candles(
            symbol=symbol,
            interval=interval,
            provider=provider,
            lookback=lookback,
            refresh=refresh,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if response is None:
        raise HTTPException(
            status_code=404,
            detail="No stored candles were found. Supply a provider query parameter to fetch and persist data.",
        )

    return response
