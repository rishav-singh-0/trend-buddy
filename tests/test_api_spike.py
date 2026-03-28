from __future__ import annotations

import unittest

from apps.api.main import app
from apps.api.routers.market_data import build_market_candles, build_market_snapshot
from apps.api.routers.portfolio import build_portfolio_summary


class ApiSpikeTests(unittest.TestCase):
    def test_market_snapshot_contract(self) -> None:
        snapshot = build_market_snapshot()
        self.assertEqual(snapshot.symbol, "NSE:NIFTY50")
        self.assertIsInstance(snapshot.price, float)
        self.assertIn(snapshot.signal, {"watch", "hedge"})

    def test_market_snapshot_json_dump_serializes_datetime(self) -> None:
        snapshot = build_market_snapshot(symbol="INFY")
        payload = snapshot.model_dump(mode="json")

        self.assertIsInstance(payload["generated_at"], str)
        self.assertEqual(payload["symbol"], "INFY")

    def test_portfolio_summary_contract(self) -> None:
        summary = build_portfolio_summary()
        self.assertGreater(summary.total_value, 0)
        self.assertEqual(len(summary.equity_curve), 7)
        self.assertGreaterEqual(len(summary.holdings), 1)

    def test_market_candles_contract(self) -> None:
        candles = build_market_candles(symbol="INFY", bars=32)
        self.assertEqual(candles.symbol, "INFY")
        self.assertEqual(candles.interval, "1D")
        self.assertEqual(len(candles.candles), 32)
        self.assertGreater(candles.candles[0].high, candles.candles[0].low)

    def test_app_exposes_expected_routes(self) -> None:
        route_paths = {getattr(route, "path", "") for route in app.routes}
        self.assertIn("/portfolio/summary", route_paths)
        self.assertIn("/market-data/snapshot", route_paths)
        self.assertIn("/market-data/candles", route_paths)
        self.assertIn("/market-data/providers", route_paths)
        self.assertIn("/health", route_paths)
        self.assertIn("/ws/market-data", route_paths)


if __name__ == "__main__":
    unittest.main()
