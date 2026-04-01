from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class LiveRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class LiveRun:
    id: str
    strategy_id: str
    instrument_id: str
    status: LiveRunStatus
    started_at: datetime
    updated_at: datetime
