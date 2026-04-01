from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .instrument import Timeframe


@dataclass
class CandleKey:
    instrument_id: str
    timeframe: Timeframe


@dataclass
class Candle:
    instrument_id: str
    timeframe: Timeframe
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


@dataclass
class Quote:
    instrument_id: str
    timestamp: datetime
    bid_price: Decimal
    ask_price: Decimal
    bid_size: Decimal = Decimal("0")
    ask_size: Decimal = Decimal("0")
