# Trend Buddy Sequential Implementation Plan

This file defines the dependency-ordered implementation plan for Trend Buddy. It turns the architecture into a build sequence so each module is delivered only after its required contracts, runtime foundations, and upstream services exist.

Status legend: `[x]` repo-visible baseline already exists, `[ ]` work still required.

All work in this plan must follow `README.md`, `docs/architecture.md`, Docker-first execution via `make`, `uv` for Python tooling/services, and the documented service boundaries.

## Segment 1: Sequential Summary

1. Shared Foundations and Runtime Baseline
2. Database Service and Persistence Contracts
3. Broker Gateway and External Integrations
4. Data Ingestion and Market Data Pipeline
5. Indicator Engine
6. Strategy Engine
7. Backtesting Service
8. Live Runner
9. Portfolio Analytics
10. API Gateway and MCP Layer
11. Frontend Application
12. Cross-Cutting Hardening and Architecture Compliance

## Segment 2: Expanded Plan

### 1. Shared Foundations and Runtime Baseline

Why first: every service depends on shared contracts, runtime conventions, env wiring, Docker execution, and health surface consistency.

Unlocks: Phases 2-11.

- [x] Root runtime scaffolding exists through `Makefile`, `docker-compose.yml`, `infra/compose`, and `infra/docker`.
- [x] Shared Go platform and contract packages exist in `packages/go`.
- [x] Shared Python package baseline exists in `packages/python`.
- [x] Base health response contracts exist for Go and Python services.
- [x] Finalize shared domain contract ownership for candles, indicators, orders, trades, strategies, backtests, live runs, and analytics payloads.
- [x] Standardize service conventions for Go modules: `cmd` plus `internal/{app,config,ports,adapters,transport}`.
- [x] Standardize service conventions for Python modules: `src/...`, shared contracts, `uv`, and container-first execution.
- [x] Define common internal error, pagination, event, and streaming envelopes in shared packages.
- [x] Standardize health, readiness, dependency status, and degraded-mode response conventions across all services.
- [x] Align config generation, env naming, and service discovery conventions for all modules.
- [ ] Define the common test/runtime baseline for unit, contract, integration, and container smoke coverage.

### 2. Database Service and Persistence Contracts

Why second: most modules need stable storage contracts before they can safely persist or retrieve domain state.

Depends on Phase 1. Unlocks Phases 3-10.

- [x] `database-service` scaffolding exists with Go service layout, health routes, and a SQLite baseline adapter.
- [ ] Define persistence ownership for candles, orders, trades, positions, strategy configs, backtest results, analytics snapshots, and live run logs.
- [ ] Establish schema design, repository boundaries, migrations, seed flow integration, indexing, and retention rules.
- [ ] Define internal storage-facing contracts for CRUD and query operations without leaking database implementation details.
- [ ] Provide versioned persistence models for strategy definitions, execution history, and historical market data.
- [ ] Add database-only access enforcement so other modules never bypass this service.
- [ ] Add repository and migration tests that run in the Docker-first workflow.

### 3. Broker Gateway and External Integrations

Why here: broker communication should be built only after persistence and normalized internal contracts exist for orders, positions, and portfolio state.

Depends on Phase 2. Unlocks Phases 4, 8, and 9.

- [x] `broker-gateway` scaffolding exists with the standard Go service layout.
- [ ] Define normalized internal contracts for orders, executions, portfolio state, holdings, margins, and broker errors.
- [ ] Implement broker adapter interfaces so provider-specific behavior stays isolated inside adapters.
- [ ] Add broker connectivity for order placement, modification, cancellation, status lookup, positions, holdings, and portfolio retrieval.
- [ ] Persist broker-linked execution and account state through Database Service contracts instead of direct database access.
- [ ] Ensure no strategy logic, backtesting logic, or UI-specific aggregation enters this service.
- [ ] Add adapter and failure-path tests for rejects, downtime, partial fills, and normalization.

### 4. Data Ingestion and Market Data Pipeline

Why here: ingestion depends on broker/provider access for live and historical feeds and on database persistence for storing normalized candles and gap-repair results.

Depends on Phases 2-3. Unlocks Phases 5-8.

- [x] `data-ingestion` scaffolding exists with the standard Go service layout.
- [ ] Define normalized candle and market-data contracts in shared packages before downstream consumers rely on them.
- [ ] Implement historical OHLCV fetch flows through approved provider or broker integrations.
- [ ] Implement websocket/live stream ingestion, reconnect handling, and stream lifecycle management.
- [ ] Add candle normalization, deduplication, gap detection, and backfill workflows.
- [ ] Store normalized historical and repaired candle data through Database Service APIs only.
- [ ] Publish clean market data for approved downstream consumers without embedding indicator or strategy logic.
- [ ] Add tests for normalization, gap filling, reconnect handling, and persistence behavior.

### 5. Indicator Engine

Why here: indicator computation requires stable candle retrieval contracts and persisted market data before it can be reused safely by strategy and backtesting modules.

Depends on Phases 2 and 4. Unlocks Phases 6-7.

- [x] `indicator-engine` scaffolding exists with the standard Go service layout.
- [ ] Define indicator request/response contracts, parameter schemas, and validation behavior.
- [ ] Implement reusable indicator functions and composable indicator pipelines.
- [ ] Read candle ranges through Database Service contracts rather than direct broker or raw provider access.
- [ ] Add stateless or cache-backed execution boundaries without turning the service into a storage owner.
- [ ] Ensure indicator computation remains separate from strategy logic and business entity storage.
- [ ] Add deterministic tests for indicator math, validation, and DB-backed reads.

### 6. Strategy Engine

Why here: strategy composition should begin only after indicator contracts and shared market-data assumptions are stable.

Depends on Phase 5. Unlocks Phases 7-8.

- [x] `strategy-engine` Python package, entrypoint, and baseline health test exist.
- [ ] Define the strategy definition format, versioning model, and validation rules.
- [ ] Define signal contracts for entry, exit, hold, metadata, and failure cases.
- [ ] Implement reusable strategy composition from indicator inputs plus rule logic.
- [ ] Ensure the same strategy logic can be reused by both backtesting and live execution paths.
- [ ] Load and persist strategy metadata through approved Database Service interfaces rather than direct database access.
- [ ] Ensure the service never places broker orders directly.
- [ ] Add unit and integration tests for strategy schema validation, rule evaluation, and signal generation.

### 7. Backtesting Service

Why here: backtesting depends on strategy definitions, indicator outputs, and historical candle access already being stable.

Depends on Phases 2, 4, 5, and 6. Must not begin before strategy contracts are stable. Unlocks Phase 10 and frontend backtest flows in Phase 11.

- [x] `backtesting` Python package, entrypoint, and baseline health test exist.
- [ ] Define backtest request, simulation parameter, result summary, and trade-log contracts.
- [ ] Integrate with Strategy Engine for reusable strategy loading and signal generation.
- [ ] Integrate with Database Service and/or approved historical data surfaces for candle retrieval.
- [ ] Integrate with Indicator Engine for reusable indicator calculations.
- [ ] Implement fills, slippage, brokerage, fee handling, drawdown, PnL, and win-rate calculations.
- [ ] Persist backtest runs, summaries, and trade logs through Database Service contracts.
- [ ] Add deterministic tests for historical simulation, PnL math, and payload contracts.

### 8. Live Runner

Why here: live orchestration only becomes viable after strategy signals, live market data, broker execution, and persistence are all available.

Depends on Phases 2, 3, 4, and 6. Unlocks Phases 9-11.

- [x] `live-runner` scaffolding exists with the standard Go service layout.
- [ ] Define lifecycle contracts for deploy, start, pause, stop, runtime status, and control actions.
- [ ] Integrate live candle/event subscriptions from Data Ingestion.
- [ ] Integrate strategy evaluation through Strategy Engine instead of embedding strategy logic locally.
- [ ] Translate validated signals into Broker Gateway execution requests.
- [ ] Persist runtime state, live logs, positions, and execution outcomes through Database Service APIs.
- [ ] Add risk-check and recovery flows for disconnects, rejects, and degraded dependencies.
- [ ] Add tests for lifecycle orchestration, signal-to-order handoff, and operational failure paths.

### 9. Portfolio Analytics

Why here: analytics requires broker-backed account state plus stored execution history, so it should follow broker integration and live/backtest persistence.

Depends on Phases 2, 3, and 8. Unlocks Phases 10-11.

- [x] `portfolio-analytics` Python package, entrypoint, and baseline health test exist.
- [ ] Define analytics contracts for portfolio summaries, exposure, realized/unrealized PnL, watchlists, and live strategy summaries.
- [ ] Aggregate broker portfolio state with stored execution and performance history through approved service interfaces.
- [ ] Implement homepage analytics, watchlist metrics, and performance reporting flows.
- [ ] Ensure the service does not execute orders, define strategies, or compute indicators internally.
- [ ] Add tests for aggregation math, response contracts, and mixed broker-plus-history scenarios.

### 10. API Gateway and MCP Layer

Why here: the gateway should be built after downstream service responsibilities, contracts, and capabilities are defined so it can aggregate them without owning business logic.

Depends on Phases 2-9. Unlocks Phase 11 and AI-facing probing.

- [x] `api-gateway` scaffolding exists with standard Go service layout, HTTP server setup, route tests, and dependency-aware health aggregation.
- [ ] Define the unified public REST and WebSocket surface for charts, strategies, backtests, live runs, and analytics.
- [ ] Expand downstream dependency wiring to every core service with resilient internal client behavior.
- [ ] Add authentication, authorization, rate limiting, and service discovery behavior.
- [ ] Define and expose MCP-compatible APIs and tool descriptions for downstream services.
- [ ] Keep the gateway free of trading logic, persistence logic, indicator ownership, and strategy ownership.
- [ ] Add tests for routing, degraded dependencies, auth behavior, and MCP flows.

### 11. Frontend Application

Why here: frontend product flows should consume stable gateway and service APIs instead of forcing backend contracts to change around the UI.

Depends on Phase 10. Must not access DB or broker directly.

- [x] Vue app shell, router, chart view, stores, and probe-related frontend scaffolding exist in `apps/web`.
- [ ] Define frontend API client boundaries around the gateway REST and WebSocket surfaces.
- [ ] Build dashboard flows for charts, portfolio analytics, strategies, backtesting, and live strategy monitoring.
- [ ] Add UI flows for strategy creation/editing, backtest execution, and live-run control.
- [ ] Surface service health, degraded dependencies, and live connection state from gateway-backed APIs.
- [ ] Keep business logic, strategy execution logic, and direct indicator ownership out of the browser.
- [ ] Add component, route, and contract tests for frontend integrations.

### 12. Cross-Cutting Hardening and Architecture Compliance

Why last: hardening should consolidate once the primary service behaviors exist, while still enforcing boundaries across the whole system before production use.

Depends on Phases 1-11.

- [x] Health endpoint scaffolding exists across the current Go and Python services.
- [ ] Add observability standards for logs, metrics, tracing, request IDs, and dependency health across all modules.
- [ ] Add container integration tests that validate the intended multi-service flows inside the Docker runtime.
- [ ] Add contract tests for shared schemas across Go, Python, gateway, and frontend consumers.
- [ ] Complete MCP coverage and capability discovery for all services that should be AI-probable.
- [ ] Enforce architecture rules: no frontend-to-DB/broker access, no strategy logic in broker/data/database services, no direct broker placement from strategy engine.
- [ ] Enforce service layout conventions for Go and Python modules in CI or repository checks.
- [ ] Verify every major flow is implementable in dependency order without bypassing documented service boundaries.
