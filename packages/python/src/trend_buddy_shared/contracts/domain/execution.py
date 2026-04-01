from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class OrderSide(StrEnum):
    BUY = "buy"
    SELL = "sell"


class OrderType(StrEnum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


class PositionDirection(StrEnum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"


@dataclass
class Fee:
    amount: Decimal
    currency: str
    kind: str = ""


@dataclass
class Order:
    id: str
    instrument_id: str
    side: OrderSide
    type: OrderType
    status: OrderStatus
    quantity: Decimal
    submitted_at: datetime
    updated_at: datetime
    account_id: str = ""
    strategy_id: str = ""
    venue: str = ""
    limit_price: Decimal = Decimal("0")
    stop_price: Decimal = Decimal("0")
    filled_quantity: Decimal = Decimal("0")
    average_fill: Decimal = Decimal("0")


@dataclass
class Fill:
    id: str
    order_id: str
    instrument_id: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    executed_at: datetime
    position_id: str = ""
    account_id: str = ""
    strategy_id: str = ""
    fees: list[Fee] = field(default_factory=list)


@dataclass
class Position:
    id: str
    instrument_id: str
    direction: PositionDirection
    quantity: Decimal
    opened_at: datetime
    account_id: str = ""
    strategy_id: str = ""
    average_open: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")
    unrealized_pnl: Decimal = Decimal("0")
    closed_at: datetime | None = None


@dataclass
class Holding:
    instrument_id: str
    quantity: Decimal
    average_price: Decimal = Decimal("0")
    market_price: Decimal = Decimal("0")
    market_value: Decimal = Decimal("0")
    cost_basis: Decimal = Decimal("0")
    unrealized_pnl: Decimal = Decimal("0")


@dataclass
class PortfolioSnapshot:
    equity: Decimal
    cash: Decimal
    timestamp: datetime
    account_id: str = ""
    buying_power: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")
    unrealized_pnl: Decimal = Decimal("0")
    holdings: list[Holding] = field(default_factory=list)
