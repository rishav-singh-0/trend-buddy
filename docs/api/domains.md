# API Domains

The API surface is domain-oriented rather than vendor-oriented.

| Domain | Route | Responsibility |
| --- | --- | --- |
| Market Data | `/market-data` | Ingest and query historical or realtime candles |
| Strategies | `/strategies` | List and configure supported strategy definitions |
| Backtests | `/backtests` | Run strategy simulations and parameter sweeps |
| Orders | `/orders` | Submit trade intents and track execution state |
| Portfolio | `/portfolio` | Retrieve holdings, exposure, sector distribution, and P&L views |
| Analytics | `/analytics` | Generate advisory-only fundamental and sentiment insights |
