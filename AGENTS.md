# AGENTS.md

This file is the working guide for AI agents contributing to `trend-buddy`.

## Project identity

- Name: `Trend Buddy`
- Purpose: open-source trading companion for market analysis, backtesting, portfolio tracking, and automated order execution.
- Current state: early modular-monolith scaffold with runnable backend HTTP API and placeholder adapters.
- Primary architecture sources:
  - `README.md`
  - `design.puml`
  - `docs/architecture/overview.md`
  - `docs/api/domains.md`
  - `docs/decisions/0001-modular-monolith.md`

## Ground truth

- The backend is a **modular monolith**, not microservices.
- `apps/api` is the single backend entrypoint.
- `apps/web` is only a frontend shell stub right now.
- Business logic belongs in `packages/core`.
- Vendor-specific logic belongs in `packages/integrations`.
- Persistence and cache abstractions belong in `packages/data`.
- Shared contracts, config, auth, logging, and utilities belong in `packages/shared`.
- Analytics is advisory-only and must not bypass risk or order-execution boundaries.

## Repo layout

```text
apps/
  api/
    src/app.js
    src/http-server.js
    src/server.js
  web/
    src/app-shell.js

packages/
  core/
    analytics/
    backtesting/
    market-data/
    orders/
    portfolio/
    risk/
    strategies/
  integrations/
    brokers/
      binance/
      groww/
      zerodha/
    market-data/
      alpha-vantage/
      nse/
      yfinance/
  data/
    cache/
    db/
    repositories/
  shared/
    auth/
    config/
    contracts/
    logging/
    utils/

tests/
  contract/
  integration/
  e2e/
  fixtures/

docs/
  architecture/
  api/
  decisions/

infra/
  docker/
  deployment/
  observability/
```

## Runtime and tooling

- Runtime: Node.js `>=20`
- Module system: ESM (`"type": "module"`)
- Start command: `npm run start`
- Test command: `npm test`
- Container entrypoint: `Dockerfile`
- Default API port: `3000`

## Live entrypoints

- `apps/api/src/app.js`
  - Composes the application and wires all modules together.
- `apps/api/src/http-server.js`
  - Exposes the backend over HTTP.
  - Has `/health` plus domain routes.
- `apps/web/src/app-shell.js`
  - Defines frontend navigation and dashboard surface only.

## API surface

Domain-oriented routes are defined in `packages/shared/contracts/src/index.js`.

- `/market-data`
- `/strategies`
- `/backtests`
- `/orders`
- `/portfolio`
- `/analytics`
- `/health`

Shared realtime event names:

- `market-data.candle.stored`
- `orders.status.updated`
- `portfolio.snapshot.updated`
- `analytics.insight.ready`

## Domain ownership

### `packages/core/market-data`
- Fetches, normalizes, caches, and stores market data.
- Must use provider adapters from `packages/integrations/market-data`.

### `packages/core/strategies`
- Owns strategy definitions and evaluation.
- Current built-ins: `sma`, `rsi`, `custom-weighted`.

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

## Adapter ownership

### Broker adapters

Located in `packages/integrations/brokers/*`.

- `zerodha`
- `groww`
- `binance`

Rules:

- Keep broker SDK and payload mapping logic inside these adapters.
- Return normalized order results that core modules can consume.
- Do not leak vendor naming or payload shapes into route handlers or shared contracts.

### Market-data adapters

Located in `packages/integrations/market-data/*`.

- `nse`
- `yfinance`
- `alpha-vantage`

Rules:

- Normalize raw market data before it reaches core modules.
- Keep provider-specific API quirks inside the adapter.
- `alpha-vantage` is planned and currently scaffolded as a placeholder.

## Data layer

- `packages/data/repositories/src/index.js` currently provides in-memory repositories.
- `packages/data/cache/src/index.js` currently provides in-memory caching.
- `packages/data/db/schema.sql` is the first SQL schema scaffold.
- Intended production direction:
  - MySQL as primary application database
  - SQLite only for local/dev or lightweight offline use

Do not assume current in-memory repositories are production-ready. If you add persistence, preserve the current abstractions instead of coupling core modules directly to a database driver.

## Shared layer

- `packages/shared/contracts`
  - Route names, provider lists, event names, API response shape
- `packages/shared/config`
  - Centralized configuration loading and defaults
- `packages/shared/logging`
  - Logging helpers
- `packages/shared/auth`
  - Role-based helpers
- `packages/shared/utils`
  - Generic utility functions

If a type, route, event, or provider enum is shared across modules, add it here instead of duplicating strings.

## Current implementation limits

- Market-data and broker adapters are placeholders, not real live integrations.
- Backend persistence is currently in-memory.
- There is no real frontend application yet, only a shell definition.
- There is no package-lock file or installed dependency tree in the repo.
- Tests are present, but they require Node to run.

## Naming and consistency rules

Use these spellings consistently:

- `API Gateway`
- `Market Data`
- `Data Aggregator`
- `Strategy`
- `Candlestick`
- `Groww`
- `Alpha Vantage`

Do not reintroduce old typos like `Aggrigator`, `Statergy`, `Candelstick`, or `Grow`.

## Editing rules for AI agents

- Preserve the modular-monolith structure unless explicitly asked to redesign it.
- Keep core domain logic separate from integrations.
- Prefer extending existing shared contracts over inventing local one-off shapes.
- Avoid vendor-specific logic in route handlers.
- Do not make analytics execution-capable unless the user explicitly redesigns that boundary.
- Keep files small and responsibility-focused.
- Add only the minimum comments needed to clarify non-obvious logic.
- Do not delete or overwrite unrelated user changes.

## When adding features

### Adding a new route

1. Add or update shared route constants in `packages/shared/contracts`.
2. Add domain behavior in the appropriate `packages/core/*` module.
3. Wire the route in `apps/api/src/app.js`.
4. Add at least one contract, integration, or end-to-end test.
5. Update `README.md` and docs if the public API changed.

### Adding a new broker

1. Create a new adapter in `packages/integrations/brokers/<name>/src/index.js`.
2. Normalize its result shape to match existing broker adapters.
3. Register it in `apps/api/src/app.js`.
4. Update shared provider lists if needed.
5. Add tests covering execution and failure handling.

### Adding a new market-data provider

1. Create a new adapter in `packages/integrations/market-data/<name>/src/index.js`.
2. Normalize candle payloads before they enter the core module.
3. Register it in `apps/api/src/app.js`.
4. Update provider lists in `packages/shared/contracts`.
5. Add tests for ingestion and normalization.

### Replacing in-memory persistence

1. Keep the repository abstraction stable.
2. Introduce a concrete data implementation behind `packages/data`.
3. Avoid spreading database client calls into core modules.
4. Update tests to cover persistence behavior, not only in-memory behavior.

## Test expectations

Important test files:

- `tests/contract/routes.test.js`
- `tests/integration/application.test.js`
- `tests/e2e/trading-flow.test.js`

Whenever possible, verify:

- Route table still matches the public API.
- The app still composes all planned modules.
- The flow `ingest -> backtest -> place order -> portfolio -> analytics` still works.

## Docker expectations

- Root `Dockerfile` runs the backend service.
- Root `.dockerignore` excludes local noise and build artifacts.
- If you change the runtime entrypoint or startup command, update:
  - `Dockerfile`
  - `package.json`
  - `README.md`

## Safe operating notes

- The git worktree may contain unrelated user changes.
- Do not revert unrelated modifications unless explicitly asked.
- If a requested change conflicts with current architecture decisions, prefer updating docs and contracts together so code and design stay aligned.
- If the environment lacks Node or Docker, state that clearly instead of pretending runtime verification happened.

## Recommended workflow for AI agents

1. Read `README.md`, `design.puml`, and this file first.
2. Inspect the relevant module before changing anything.
3. Keep changes inside the correct boundary.
4. Update tests with behavioral changes.
5. Update docs when the public interface or architecture meaning changes.
6. Report what changed, what was verified, and what could not be verified.
