import unittest
from datetime import datetime
from decimal import Decimal

from trend_buddy_shared.contracts import (
    AssetClass,
    BacktestRequest,
    Candle,
    ErrorResponse,
    EventEnvelope,
    IndicatorRequest,
    Instrument,
    LiveRun,
    LiveRunStatus,
    SignalAction,
    StrategyDefinition,
    StrategyState,
    StrategySignal,
    StreamEnvelope,
)


class SharedContractsTest(unittest.TestCase):
    def test_domain_contracts_are_instantiable(self) -> None:
        instrument = Instrument(id="NSE:SBIN", symbol="SBIN", asset_class=AssetClass.EQUITY, venue="NSE")
        candle = Candle(
            instrument_id=instrument.id,
            timeframe="1m",
            timestamp=datetime(2024, 1, 1, 9, 15),
            open=Decimal("1.0"),
            high=Decimal("2.0"),
            low=Decimal("0.5"),
            close=Decimal("1.5"),
            volume=Decimal("100.0"),
        )
        strategy = StrategyDefinition(
            id="strat-1",
            name="Mean Reversion",
            version="v1",
            state=StrategyState.DRAFT,
            instrument_ids=[instrument.id],
        )
        signal = StrategySignal(
            strategy_id="strat-1",
            instrument_id=instrument.id,
            action=SignalAction.HOLD,
            timestamp=datetime(2024, 1, 1, 9, 16),
        )
        event = EventEnvelope(type="strategy.signal", source="strategy-engine", timestamp=datetime(2024, 1, 1, 9, 16))
        stream = StreamEnvelope(topic="candles.1m", type="candle", timestamp=datetime(2024, 1, 1, 9, 16))
        error = ErrorResponse(code="invalid_request", message="bad input")
        indicator = IndicatorRequest(
            indicator="ema",
            instrument_id=instrument.id,
            timeframe="1m",
            start_time=datetime(2024, 1, 1, 9, 15),
            end_time=datetime(2024, 1, 1, 15, 30),
        )
        backtest = BacktestRequest(
            strategy_id="strat-1",
            instrument_id=instrument.id,
            timeframe="1m",
            start_time=datetime(2024, 1, 1, 9, 15),
            end_time=datetime(2024, 1, 1, 15, 30),
            initial_capital=Decimal("10000.0"),
        )
        live_run = LiveRun(
            id="run-1",
            strategy_id="strat-1",
            instrument_id=instrument.id,
            status=LiveRunStatus.RUNNING,
            started_at=datetime(2024, 1, 1, 9, 15),
            updated_at=datetime(2024, 1, 1, 9, 16),
        )

        self.assertEqual(candle.instrument_id, "NSE:SBIN")
        self.assertEqual(strategy.version, "v1")
        self.assertEqual(signal.action, SignalAction.HOLD)
        self.assertEqual(event.type, "strategy.signal")
        self.assertEqual(stream.topic, "candles.1m")
        self.assertEqual(error.code, "invalid_request")
        self.assertEqual(indicator.indicator, "ema")
        self.assertEqual(backtest.initial_capital, Decimal("10000.0"))
        self.assertEqual(live_run.status, LiveRunStatus.RUNNING)
