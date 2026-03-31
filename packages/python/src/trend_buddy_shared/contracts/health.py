from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class HealthResponse:
    service: str
    status: str
    checks: Dict[str, Any] = field(default_factory=dict)
