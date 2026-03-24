export const DOMAIN_ROUTES = Object.freeze({
  marketData: "/market-data",
  strategies: "/strategies",
  backtests: "/backtests",
  orders: "/orders",
  portfolio: "/portfolio",
  analytics: "/analytics"
});

export const REALTIME_EVENTS = Object.freeze({
  candleStored: "market-data.candle.stored",
  orderUpdated: "orders.status.updated",
  portfolioUpdated: "portfolio.snapshot.updated",
  analyticsReady: "analytics.insight.ready"
});

export const MARKET_DATA_PROVIDERS = Object.freeze([
  "nse",
  "yfinance",
  "alpha-vantage"
]);

export const BROKER_PROVIDERS = Object.freeze([
  "zerodha",
  "groww",
  "binance"
]);

export function createApiResponse(data, meta = {}) {
  return {
    data,
    meta: {
      generatedAt: new Date().toISOString(),
      ...meta
    }
  };
}

export function createRouteTable() {
  return Object.entries(DOMAIN_ROUTES).map(([domain, path]) => ({
    domain,
    path
  }));
}
