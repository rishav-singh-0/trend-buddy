from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter

from packages.shared.contracts.portfolio import EquityPoint, PortfolioHolding, PortfolioSummary

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def build_portfolio_summary() -> PortfolioSummary:
    start = date.today() - timedelta(days=6)
    equity_curve = [
        EquityPoint(session=(start + timedelta(days=offset)).isoformat(), close=value)
        for offset, value in enumerate([121_800.0, 122_640.0, 121_950.0, 123_380.0, 124_120.0, 125_540.0, 126_240.0])
    ]
    holdings = [
        PortfolioHolding(symbol="INFY", sector="IT", allocation_pct=22.4, pnl_pct=8.2),
        PortfolioHolding(symbol="HDFCBANK", sector="Financials", allocation_pct=18.6, pnl_pct=3.4),
        PortfolioHolding(symbol="RELIANCE", sector="Energy", allocation_pct=16.1, pnl_pct=5.1),
        PortfolioHolding(symbol="SUNPHARMA", sector="Pharma", allocation_pct=12.3, pnl_pct=7.9),
    ]
    return PortfolioSummary(
        total_value=126_240.0,
        daily_pnl=1_420.0,
        total_pnl=8_740.0,
        cash_balance=19_850.0,
        top_sector="IT",
        equity_curve=equity_curve,
        holdings=holdings,
    )


@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary() -> PortfolioSummary:
    return build_portfolio_summary()
