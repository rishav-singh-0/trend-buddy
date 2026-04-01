from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class PerformanceSummary:
    period: str
    total_pnl: Decimal
    win_rate: Decimal
    max_drawdown: Decimal
    trade_count: int


@dataclass
class PortfolioSummary:
    equity: Decimal
    cash: Decimal
    open_positions: int
    timestamp: datetime
    account_id: str = ""
    realized_pnl: Decimal = Decimal("0")
    unrealized_pnl: Decimal = Decimal("0")
