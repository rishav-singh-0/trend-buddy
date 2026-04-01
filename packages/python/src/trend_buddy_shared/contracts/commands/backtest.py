from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from trend_buddy_shared.contracts.domain.instrument import Timeframe


@dataclass
class BacktestRequest:
    strategy_id: str
    instrument_id: str
    timeframe: Timeframe
    start_time: datetime
    end_time: datetime
    initial_capital: Decimal
    fees: Decimal = Decimal("0")
    slippage: Decimal = Decimal("0")
    parameters: dict[str, Any] = field(default_factory=dict)
