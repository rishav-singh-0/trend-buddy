# Trend Buddy

Trend Buddy is an open-source trading companion for market analysis, backtesting, portfolio tracking, and automated execution workflows.

## Project Structure

```text
apps
└── web
services
├── api-gateway
├── backtesting
├── broker-gateway
├── data-ingestion
├── database-service
├── indicator-engine
├── live-runner
├── portfolio-analytics
└── strategy-engine
packages
├── go
│   ├── contracts
│   └── platform
└── python
config
infra
├── compose
└── docker
db
docs
└── getting-started.md
tools
AGENTS.md
docker-compose.yml
go.mod
go.sum
Makefile
README.md
```

## Runtime Strategy
1. Go services own latency-sensitive online paths:
   - `api-gateway`
   - `broker-gateway`
   - `data-ingestion`
   - `database-service`
   - `indicator-engine`
   - `live-runner`
2. Python services own research-heavy and analytics-heavy paths:
   - `backtesting`
   - `strategy-engine`
   - `portfolio-analytics`
3. Frontend lives in `apps/web`.
4. Shared cross-language contracts live in `packages/go/contracts` and `packages/python/src/trend_buddy_shared/contracts`.
5. Docker Compose is the default development runtime and Python is always executed through `uv`.

## Architecture Components
1. Data Fetching module
	- Fetches historic data
	- Manages websocket and missing candels
2. Database management - only point of contact from and to the database
3. Frontend - Communicates through only our services (through rest and websocket)
4. Broker service - Communicates to broker for candle-stick data, order execution and portfolio information
5. Indecator API - Seperate service for doing mathematics on the given period of candels and retriving when called by backtesting or frontend
6. Strategy Maker - Collection of statergy which is combination of indecators and some logical data operations on the data. This can be used for backtesting as well as live trading.
7. Backtesting Service - Backtest given statergy for provided time, calculates PNL
8. Live Strategy Runner - Deploys the strategy, either for testing or through actual market.
9. Each service should expose MCP apis so that it could be later probed to AI
