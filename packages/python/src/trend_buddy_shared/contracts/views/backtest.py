from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from trend_buddy_shared.contracts.domain.execution import Fill
from trend_buddy_shared.contracts.views.analytics import PerformanceSummary


@dataclass
class IndicatorPoint:
    timestamp: datetime
    value: Decimal


@dataclass
class IndicatorSeries:
    indicator: str
    values: list[IndicatorPoint] = field(default_factory=list)


@dataclass
class EquityPoint:
    timestamp: datetime
    equity: Decimal


@dataclass
class BacktestResult:
    run_id: str
    strategy_id: str
    summary: PerformanceSummary
    fills: list[Fill] = field(default_factory=list)
    equity_curve: list[EquityPoint] = field(default_factory=list)
