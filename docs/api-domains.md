# API Domains

The API surface is domain-oriented rather than vendor-oriented.

| Domain | Route | Responsibility |
| --- | --- | --- |
| Market Data | `/market-data` | `POST` ingests provider candles and `GET` can query stored candles or fetch on demand when `provider` is supplied |
| Strategies | `/strategies` | List and configure supported strategy definitions |
| Backtests | `/backtests` | Run strategy simulations over stored Candlestick history |
| Orders | `/orders` | Submit trade intents, apply Risk checks, and track execution state |
| Portfolio | `/portfolio` | Retrieve holdings, exposure, sector distribution, and P&L views |
| Analytics | `/analytics` | Generate advisory-only insights using market, backtest, and portfolio context |
