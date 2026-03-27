from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from packages.shared.contracts.market_data import MarketCandle


@dataclass(frozen=True)
class StoredCandleBatch:
    symbol: str
    interval: str
    provider: str
    candles: list[MarketCandle]


class MarketDataStore:
    def __init__(self, db_path: str) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS market_candles (
                    symbol TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    interval TEXT NOT NULL,
                    time INTEGER NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    fetched_at TEXT NOT NULL,
                    PRIMARY KEY (symbol, provider, interval, time)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_market_candles_lookup
                ON market_candles(symbol, interval, provider, time)
                """
            )

    def save_candles(self, symbol: str, provider: str, interval: str, candles: list[MarketCandle]) -> None:
        if not candles:
            return

        fetched_at = datetime.now(timezone.utc).isoformat()
        rows = [
            (
                symbol,
                provider,
                interval,
                candle.time,
                candle.open,
                candle.high,
                candle.low,
                candle.close,
                candle.volume,
                fetched_at,
            )
            for candle in candles
        ]
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO market_candles (
                    symbol, provider, interval, time, open, high, low, close, volume, fetched_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(symbol, provider, interval, time) DO UPDATE SET
                    open = excluded.open,
                    high = excluded.high,
                    low = excluded.low,
                    close = excluded.close,
                    volume = excluded.volume,
                    fetched_at = excluded.fetched_at
                """,
                rows,
            )

    def get_candles(self, symbol: str, interval: str, provider: Optional[str] = None) -> Optional[StoredCandleBatch]:
        with self._connect() as connection:
            resolved_provider = provider or self._resolve_latest_provider(connection, symbol=symbol, interval=interval)
            if resolved_provider is None:
                return None

            rows = connection.execute(
                """
                SELECT time, open, high, low, close, volume
                FROM market_candles
                WHERE symbol = ? AND interval = ? AND provider = ?
                ORDER BY time ASC
                """,
                (symbol, interval, resolved_provider),
            ).fetchall()
            if not rows:
                return None

        candles = [
            MarketCandle(
                time=int(row["time"]),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["volume"]),
            )
            for row in rows
        ]
        return StoredCandleBatch(symbol=symbol, interval=interval, provider=resolved_provider, candles=candles)

    def _resolve_latest_provider(self, connection: sqlite3.Connection, symbol: str, interval: str) -> Optional[str]:
        row = connection.execute(
            """
            SELECT provider, MAX(fetched_at) AS latest_fetch
            FROM market_candles
            WHERE symbol = ? AND interval = ?
            GROUP BY provider
            ORDER BY latest_fetch DESC
            LIMIT 1
            """,
            (symbol, interval),
        ).fetchone()
        return str(row["provider"]) if row else None
