function createCollection(name) {
  const items = [];

  return {
    name,
    insert(record) {
      items.push(record);
      return record;
    },
    insertMany(records) {
      items.push(...records);
      return records;
    },
    list() {
      return [...items];
    },
    clear() {
      items.length = 0;
    }
  };
}

export function createInMemoryRepositories() {
  const candles = createCollection("candles");
  const fundamentals = createCollection("fundamentals");
  const orders = createCollection("orders");
  const backtests = createCollection("backtests");
  const analytics = createCollection("analytics");
  const portfolioSnapshots = createCollection("portfolioSnapshots");

  return {
    candles,
    fundamentals,
    orders,
    backtests,
    analytics,
    portfolioSnapshots,
    listCandlesBySymbol(symbol) {
      return candles.list().filter((candle) => candle.symbol === symbol);
    }
  };
}
