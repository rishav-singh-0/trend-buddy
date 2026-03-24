export function createAlphaVantageProvider() {
  return {
    name: "alpha-vantage",
    planned: true,
    async fetchCandles({ symbol, interval }) {
      return [
        { open: 50, high: 51, low: 49, close: 50.5, volume: 3000, time: `${interval}-1` },
        { open: 50.5, high: 52, low: 50, close: 51.5, volume: 3250, time: `${interval}-2` },
        { open: 51.5, high: 53, low: 51, close: 52.25, volume: 3400, time: `${interval}-3` }
      ].map((candle) => ({ ...candle, symbol }));
    }
  };
}
