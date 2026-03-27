from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from packages.core.market_data.provider import MarketDataProvider
from packages.core.market_data.storage import MarketDataStore
from packages.shared.config.settings import get_settings
from packages.shared.contracts.market_data import MarketCandlesResponse
from packages.integrations.market_data.yfinance_provider import YFinanceMarketDataProvider


@dataclass(frozen=True)
class ProviderDescriptor:
    name: str


class MarketDataService:
    def __init__(self, store: MarketDataStore, providers: dict[str, MarketDataProvider], default_provider: str) -> None:
        self._store = store
        self._providers = providers
        self._default_provider = default_provider

    def list_providers(self) -> list[ProviderDescriptor]:
        return [ProviderDescriptor(name=name) for name in sorted(self._providers)]

    def get_candles(
        self,
        *,
        symbol: str,
        interval: str,
        provider: Optional[str] = None,
        lookback: Optional[str] = None,
        refresh: bool = False,
    ) -> Optional[MarketCandlesResponse]:
        resolved_provider = provider or (self._default_provider if refresh else None)

        if resolved_provider is not None:
            return self.fetch_and_store_candles(
                symbol=symbol,
                interval=interval,
                provider=resolved_provider,
                lookback=lookback,
            )

        stored_batch = self._store.get_candles(symbol=symbol, interval=interval)
        if stored_batch is None:
            return None

        return MarketCandlesResponse(
            symbol=stored_batch.symbol,
            interval=stored_batch.interval,
            provider=stored_batch.provider,
            source="stored",
            candles=stored_batch.candles,
        )

    def fetch_and_store_candles(
        self, *, symbol: str, interval: str, provider: str, lookback: Optional[str] = None
    ) -> MarketCandlesResponse:
        adapter = self._providers.get(provider)
        if adapter is None:
            raise ValueError(f"Unsupported market data provider: {provider}")

        candles = adapter.fetch_candles(symbol=symbol, interval=interval, lookback=lookback)
        self._store.save_candles(symbol=symbol, provider=provider, interval=interval, candles=candles)
        return MarketCandlesResponse(
            symbol=symbol,
            interval=interval,
            provider=provider,
            source="provider",
            candles=candles,
        )


def create_market_data_service() -> MarketDataService:
    settings = get_settings()
    providers: dict[str, MarketDataProvider] = {
        "yfinance": YFinanceMarketDataProvider(),
    }
    return MarketDataService(
        store=MarketDataStore(settings.market_data_db_path),
        providers=providers,
        default_provider="yfinance",
    )
