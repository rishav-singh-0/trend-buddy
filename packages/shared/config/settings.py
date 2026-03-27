from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    api_host: str
    api_port: int
    cors_origins: list[str]
    market_data_db_path: str


def get_settings() -> Settings:
    origins = os.getenv("TREND_BUDDY_CORS_ORIGINS", "http://localhost:5173")
    cors_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    return Settings(
        api_host=os.getenv("TREND_BUDDY_API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("TREND_BUDDY_API_PORT", "3000")),
        cors_origins=cors_origins or ["http://localhost:5173"],
        market_data_db_path=os.getenv("TREND_BUDDY_MARKET_DATA_DB_PATH", ".data/market-data.sqlite3"),
    )
