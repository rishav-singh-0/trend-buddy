# AGENTS.md

This file is the working guide for AI agents contributing to `trend-buddy`.

## Project identity

- Name: `Trend Buddy`
- Purpose: open-source trading companion for market analysis, backtesting, portfolio tracking, and automated order execution.
- Primary architecture sources (must read):
  - `README.md`
  - `docs/architecture.md`
  - `docs/api-domains.md`

## Runtime and tooling

- Package Manager: uv (app python commands must use `uv run`)
- Container entrypoint: `Dockerfile`
- Default API port: `3000`

## Domain flow

1. Market data adapters ingest candlestick and fundamental inputs.
2. Data is normalized and stored through the data layer.
3. Strategies and backtesting consume stored history.
4. Order execution applies risk checks before routing to broker adapters.
5. Portfolio snapshots are rebuilt from order history.
6. Analytics publishes advisory-only insights that never bypass risk or execution boundaries.

## Domain ownership

### `packages/core/market-data`
- Fetches, normalizes, caches, and stores market data.
- Must use provider adapters from `packages/integrations/market-data`.

### `packages/core/strategies`
- Owns strategy definitions and evaluation.
- Current built-ins: `sma`, `rsi`, `custom-weighted`, `custom`.

### `packages/core/backtesting`
- Runs simulations from stored candlestick history and strategy definitions.
- Stores backtest results separately from live order data.

### `packages/core/risk`
- Applies pre-trade checks.
- Must remain reusable and independent from broker-specific code.

### `packages/core/orders`
- Validates order flow through risk first, then broker adapters.
- Must not embed broker-specific implementation logic directly.

### `packages/core/portfolio`
- Rebuilds positions and summary views from order history.
- Keeps holdings, sectors, and exposure logic centralized.

### `packages/core/analytics`
- Produces advisory insights only.
- Must never place orders or bypass risk.
