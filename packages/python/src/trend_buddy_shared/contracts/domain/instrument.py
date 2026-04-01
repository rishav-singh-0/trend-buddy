from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class AssetClass(StrEnum):
    EQUITY = "equity"
    OPTION = "option"
    FUTURE = "future"
    FOREX = "forex"
    CRYPTO = "crypto"


Timeframe = str


@dataclass
class Instrument:
    id: str
    symbol: str
    asset_class: AssetClass
    venue: str = ""
    base_currency: str = ""
    quote_currency: str = ""
    tick_size: Decimal = Decimal("0")
    lot_size: Decimal = Decimal("0")
