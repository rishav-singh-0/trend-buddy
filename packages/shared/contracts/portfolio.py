from __future__ import annotations

from pydantic import BaseModel


class EquityPoint(BaseModel):
    session: str
    close: float


class PortfolioHolding(BaseModel):
    symbol: str
    sector: str
    allocation_pct: float
    pnl_pct: float


class PortfolioSummary(BaseModel):
    total_value: float
    daily_pnl: float
    total_pnl: float
    cash_balance: float
    top_sector: str
    equity_curve: list[EquityPoint]
    holdings: list[PortfolioHolding]
