from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Optional

from packages.core.market_data.service import MarketDataService
from packages.core.market_data.storage import MarketDataStore
from packages.shared.contracts.market_data import MarketCandle


class FakeMarketDataProvider:
    name = "fake"

    def fetch_candles(self, symbol: str, interval: str, lookback: Optional[str] = None) -> list[MarketCandle]:
        return [
            MarketCandle(time=1_710_000_000, open=100.0, high=104.0, low=99.0, close=103.5, volume=10_000.0),
            MarketCandle(time=1_710_086_400, open=103.5, high=107.0, low=102.0, close=106.0, volume=12_500.0),
        ]


class MarketDataDomainTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        db_path = str(Path(self._temp_dir.name) / "market-data.sqlite3")
        self.store = MarketDataStore(db_path)
        self.service = MarketDataService(
            store=self.store,
            providers={"fake": FakeMarketDataProvider()},
            default_provider="fake",
        )

    def tearDown(self) -> None:
        self._temp_dir.cleanup()

    def test_fetch_and_store_candles_persists_batch(self) -> None:
        fetched = self.service.get_candles(symbol="INFY", interval="1D", provider="fake")
        self.assertIsNotNone(fetched)
        assert fetched is not None
        self.assertEqual(fetched.provider, "fake")
        self.assertEqual(fetched.source, "provider")
        self.assertEqual(len(fetched.candles), 2)

        stored = self.service.get_candles(symbol="INFY", interval="1D")
        self.assertIsNotNone(stored)
        assert stored is not None
        self.assertEqual(stored.provider, "fake")
        self.assertEqual(stored.source, "stored")
        self.assertEqual(stored.candles[1].close, 106.0)

    def test_list_providers_exposes_registered_provider_names(self) -> None:
        providers = self.service.list_providers()
        self.assertEqual([provider.name for provider in providers], ["fake"])

    def test_missing_stored_batch_returns_none(self) -> None:
        self.assertIsNone(self.service.get_candles(symbol="UNKNOWN", interval="1D"))


if __name__ == "__main__":
    unittest.main()
