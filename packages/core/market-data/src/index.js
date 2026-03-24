import { REALTIME_EVENTS } from "../../../shared/contracts/src/index.js";

export function createMarketDataModule({ repositories, providers, cache, logger }) {
  return {
    listProviders() {
      return Object.keys(providers);
    },
    async ingestCandles({ provider, symbol, interval = "1d" }) {
      const adapter = providers[provider];
      if (!adapter) {
        throw new Error(`Unsupported market data provider: ${provider}`);
      }

      const candles = await adapter.fetchCandles({ symbol, interval });
      const normalized = candles.map((candle) => ({
        provider,
        symbol,
        interval,
        ...candle
      }));

      repositories.candles.insertMany(normalized);
      cache.set(`${provider}:${symbol}:${interval}`, normalized);

      return {
        event: REALTIME_EVENTS.candleStored,
        count: normalized.length,
        provider,
        symbol,
        log: logger.info("Stored candlestick data", { provider, symbol, interval })
      };
    },
    listCandles(symbol) {
      return repositories.listCandlesBySymbol(symbol);
    }
  };
}
