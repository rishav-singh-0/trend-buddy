from dataclasses import dataclass, field


@dataclass
class ErrorDetail:
    message: str
    field: str = ""


@dataclass
class ErrorResponse:
    code: str
    message: str
    details: list[ErrorDetail] = field(default_factory=list)


@dataclass
class Pagination:
    page: int
    page_size: int
    total_items: int
    total_pages: int
