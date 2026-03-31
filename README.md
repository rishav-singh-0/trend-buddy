# Trend Buddy

Trend Buddy is an open-source trading companion for market analysis, backtesting, portfolio tracking, and automated execution workflows.

## Project Structure

```text
apps
└── web                          # Vue.js frontend application
services
├── api-gateway                  # Go – unified REST/WebSocket entry point
├── backtesting                  # Python – backtest strategies and calculate PnL
├── broker-gateway               # Go – broker communication (orders, candles, portfolio)
├── data-ingestion               # Go – historic data fetching & WebSocket candle management
├── database-service             # Go – sole interface to the database
├── indicator-engine             # Go – mathematical indicators on candle data
├── live-runner                  # Go – deploy strategies to paper or live markets
├── portfolio-analytics          # Python – portfolio-level analytics and reporting
└── strategy-engine              # Python – composable strategies using indicators & logic
packages
├── go
│   ├── contracts                # Shared Go request/response contracts
│   └── platform                 # Shared Go platform utilities
└── python                       # Shared Python library (trend_buddy_shared)
config                           # Application and environment configuration
infra
├── compose                      # Docker Compose override / profile files
└── docker                       # Dockerfiles for each service
db                               # Database migrations and seed data
docs                             # Project documentation
└── getting-started.md           # Onboarding guide
tools                            # Developer helper scripts and tooling
AGENTS.md                        # AI agent / coding guidelines
docker-compose.yml               # Default development runtime definition
go.mod                           # Go module definition
go.sum                           # Go dependency checksums
Makefile                         # Build, run, and Docker commands (make up, etc.)
README.md                        # This file – project overview
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
