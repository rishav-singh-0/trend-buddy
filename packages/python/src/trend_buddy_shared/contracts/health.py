from dataclasses import dataclass, field
from typing import Dict


@dataclass
class HealthResponse:
    service: str
    status: str
    details: Dict[str, str] = field(default_factory=dict)
