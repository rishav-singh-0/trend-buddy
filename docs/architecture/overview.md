# Architecture Overview

Trend Buddy is scaffolded as a modular monolith with one backend application and clear internal boundaries.

## Runtime shape

- `apps/web` contains presentation concerns only.
- `apps/api` is the API entrypoint for REST and realtime routes.
- `packages/core` contains domain logic for market data, strategies, backtesting, orders, portfolio, analytics, and risk.
- `packages/integrations` contains all vendor-specific adapters.
- `packages/data` contains persistence and cache abstractions.
- `packages/shared` contains contracts and platform utilities shared across the workspace.

## Domain flow

1. Market data adapters ingest candlestick and fundamental inputs.
2. Data is normalized and stored through the data layer.
3. Strategies and backtesting consume stored history.
4. Order execution applies risk checks before routing to broker adapters.
5. Portfolio snapshots are rebuilt from order history.
6. Analytics publishes advisory-only insights that never bypass risk or execution boundaries.
