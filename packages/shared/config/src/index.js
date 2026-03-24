export function loadConfig(overrides = {}) {
  return {
    appName: "Trend Buddy",
    environment: overrides.environment ?? process.env.NODE_ENV ?? "development",
    database: {
      primary: overrides.primaryDatabase ?? "mysql",
      local: overrides.localDatabase ?? "sqlite"
    },
    marketData: {
      supportedIntervals: ["1m", "5m", "1d", "1wk", "1mo"],
      providers: ["nse", "yfinance", "alpha-vantage"]
    },
    risk: {
      maxOrderValue: overrides.maxOrderValue ?? 250000,
      maxPositionConcentrationPct: overrides.maxPositionConcentrationPct ?? 35
    }
  };
}
