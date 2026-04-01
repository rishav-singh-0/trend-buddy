from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class EventEnvelope:
    type: str
    source: str
    timestamp: datetime
    subject: str = ""
    data: Any = None


@dataclass
class StreamEnvelope:
    topic: str
    type: str
    timestamp: datetime
    data: Any = None
