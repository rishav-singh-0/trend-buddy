from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any


class StrategyState(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class SignalAction(StrEnum):
    ENTER_LONG = "enter_long"
    EXIT_LONG = "exit_long"
    ENTER_SHORT = "enter_short"
    EXIT_SHORT = "exit_short"
    HOLD = "hold"


@dataclass
class StrategyDefinition:
    id: str
    name: str
    version: str
    state: StrategyState
    instrument_ids: list[str] = field(default_factory=list)
    indicator_refs: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategySignal:
    strategy_id: str
    instrument_id: str
    action: SignalAction
    timestamp: datetime
    strength: Decimal = Decimal("0")
    metadata: dict[str, Any] = field(default_factory=dict)
