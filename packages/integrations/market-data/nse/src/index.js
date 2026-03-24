export function createNseProvider() {
  return {
    name: "nse",
    async fetchCandles({ symbol, interval }) {
      return [
        { open: 100, high: 104, low: 99, close: 102, volume: 12000, time: `${interval}-1` },
        { open: 102, high: 106, low: 101, close: 105, volume: 14400, time: `${interval}-2` },
        { open: 105, high: 107, low: 103, close: 106, volume: 15100, time: `${interval}-3` }
      ].map((candle) => ({ ...candle, symbol }));
    }
  };
}
