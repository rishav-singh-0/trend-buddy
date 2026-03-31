
## Repository Shape

- `apps/web` contains the Vue frontend.
- `services/` contains deployable services, with Go used for online latency-sensitive services and Python used for research-heavy modules such as backtesting and analytics.
- `packages/go` and `packages/python` contain shared contracts, clients and platform helpers.
- `config/` owns tracked base env config plus generated local env files.
- `infra/compose` and `infra/docker` own container orchestration and shared Docker build definitions.

## Architecture Components

---
### 1. Data Ingestion Service

**Scope**
- Fetch historical candle/OHLCV data
- Manage broker/data-provider websocket streams
- Detect and fill missing candles/gaps
- Normalize raw market data into internal format
- Publish cleaned market data to downstream services

**Should not do**
- Indicator calculations
- Strategy logic
- Order placement
- Direct frontend handling

---
### 2. Broker Gateway Service

**Scope**
- Single integration point with broker APIs
- Fetch live market feed if broker provides it
- Place/modify/cancel orders
- Fetch portfolio, margin, positions, holdings, order status
- Normalize broker-specific responses into internal models

**Should not do**
- Strategy decisions
- Backtesting
- UI-facing business aggregation

---
### 3. Database Service

**Scope**
- Only point of contact with database
- Store/retrieve candles, trades, orders, positions, strategy configs, backtest results, live run logs
- Provide query APIs to internal services
- Handle schema, indexing, retention, consistency

**Should not do**
- Business logic
- Direct broker calls
- Direct frontend logic

---
### 4. Indicator Engine API

**Scope**
- Compute indicators on requested candle ranges
- Expose reusable math functions and indicator pipelines
- Return computed indicator series to strategy/backtest/frontend
- Stateless or cache-backed service

**Should not do**
- Fetch raw data from broker directly
- Store business entities
- Execute strategy logic

---
### 5. Strategy Engine / Strategy Maker

**Scope**
- Define strategies as compositions of indicators + rule logic
- Maintain strategy definition format/versioning
- Generate entry/exit/hold signals
- Support both backtesting and live execution reuse

**Should not do**
- Place orders directly
- Compute PnL directly
- Manage database access directly

---
### 6. Backtesting Service

**Scope**
- Run strategy on historical data for a given period
- Request candles from Database/Data service
- Request indicator values from Indicator API
- Apply fills, slippage, brokerage, fees
- Calculate PnL, drawdown, win rate, stats, trade logs

**Should not do**
- Live execution
- Broker order placement
- Maintain strategy definitions

---
### 7. Live Strategy Runner

**Scope**
- Deploy/start/stop/pause live strategies
- Subscribe to live candles/events
- Feed live data into Strategy Engine
- Convert signals into execution requests through Broker Gateway
- Track runtime state, live logs, health, risk checks

**Should not do**
- Indicator math ownership
- Historical bulk backtesting
- Frontend rendering

---
### 8. Portfolio & Analytics Service

**Scope**
- Aggregate portfolio PnL, holdings, exposure, performance metrics
- Serve homepage analytics
- Combine broker data + stored execution history
- Provide watchlist metrics and live strategy summaries

**Should not do**
- Execute orders
- Define strategies
- Compute indicators internally

---
### 9. Frontend Service / UI

**Scope**
- Communicate only through REST/WebSocket APIs
- Show dashboards, charts, strategy panels, order book, live strategies
- No direct DB or broker access

**Should not do**
- Business logic
- Strategy execution logic
- Indicator computation locally beyond simple chart overlays

---
### 10. API Gateway / MCP Layer

**Scope**
- Unified API entry point for frontend and AI probing
- Expose MCP-compatible APIs for all services
- Authentication, authorization, rate limiting, routing
- Standard service discovery and tool descriptions for AI

**Should not do**
- Core trading/business logic
- Data storage
- Direct indicator or strategy ownership

---

### Architecture Diagram

```mermaid
%%{ init: { 'flowchart': { 'defaultRenderer': 'elk' } } }%%

flowchart TD
  %% External
  U[User / Trader]
  BR[Broker / Exchange]
  
  %% Internal Services
  FE[Frontend]
  BS[Broker Service]
  DFS[Data Fetching Service]
  IS[Indicator API]
  SS[Strategy Maker]
  BTS[Backtesting Service]
  LSR[Live Strategy Runner]
  DBS[Database Service]
  DB[(Trading Database)]
  
  %% User access
  U -->|REST / WebSocket| FE
  
  %% Frontend calls
  FE -->|charts / watchlist| DFS
  FE -->|portfolio / order book| BS
  FE -->|PnL / history / reports| DBS
  FE -->|create / edit strategy| SS
  FE -->|run backtest| BTS
  FE -->|deploy / monitor live strategy| LSR
  
  %% Broker-facing
  BR <--> |market data / orders / portfolio| BS
  BS -->|raw candles / ticks| DFS
  BS -->|order status / positions / holdings| DBS
  
  %% Data pipeline
  DFS -->|normalize data / fill missing candles| DBS
  DFS -->|live candle stream| LSR
  DFS -->|live chart stream| FE
  
  %% Strategy / indicator
  SS -->|indicator requests| IS
  SS <--> |strategy config| DBS
  IS -->|read candle range| DBS
  
  %% Backtesting
  BTS -->|load strategy| SS
  BTS -->|historical candles| DBS
  BTS -->|backtest result / PnL| DBS
  
  %% Live trading
  LSR -->|load strategy| SS
  LSR -->|place / modify / cancel order| BS
  LSR -->|runtime logs / trades / state| DBS
  
  %% Database
  DBS <--> DB
  
  %% Material Design theme classes
  classDef external fill:#ECEFF1,stroke:#607D8B,color:#263238,stroke-width:1.5px;
  classDef frontend fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:1.5px;
  classDef broker fill:#FFF3E0,stroke:#FB8C00,color:#E65100,stroke-width:1.5px;
  classDef data fill:#E0F7FA,stroke:#00ACC1,color:#006064,stroke-width:1.5px;
  classDef logic fill:#F3E5F5,stroke:#8E24AA,color:#4A148C,stroke-width:1.5px;
  classDef runtime fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:1.5px;
  classDef storage fill:#FBE9E7,stroke:#F4511E,color:#BF360C,stroke-width:1.5px;
  
  %% Class assignments
  class U,BR external;
  class FE frontend;
  class BS broker;
  class DFS,IS data;
  class SS,BTS logic;
  class LSR runtime;
  class DBS,DB storage;
```
