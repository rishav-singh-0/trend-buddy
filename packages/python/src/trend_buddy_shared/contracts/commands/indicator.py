from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from trend_buddy_shared.contracts.domain.instrument import Timeframe


@dataclass
class IndicatorRequest:
    indicator: str
    instrument_id: str
    timeframe: Timeframe
    start_time: datetime
    end_time: datetime
    parameters: dict[str, Any] = field(default_factory=dict)
