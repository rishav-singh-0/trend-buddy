export function createYFinanceProvider() {
  return {
    name: "yfinance",
    async fetchCandles({ symbol, interval }) {
      return [
        { open: 200, high: 202, low: 198, close: 199, volume: 8800, time: `${interval}-1` },
        { open: 199, high: 205, low: 197, close: 203, volume: 9500, time: `${interval}-2` },
        { open: 203, high: 208, low: 202, close: 207, volume: 10100, time: `${interval}-3` }
      ].map((candle) => ({ ...candle, symbol }));
    }
  };
}
