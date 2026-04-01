from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LiveRunControlAction(StrEnum):
    START = "start"
    PAUSE = "pause"
    STOP = "stop"


@dataclass
class LiveRunControlRequest:
    strategy_id: str
    instrument_id: str
    action: LiveRunControlAction
    run_id: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
