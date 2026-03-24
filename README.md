# Trend Buddy

An Open-Source Trading Companion for Analysis, Backtesting, and Automated Trading.

## About the Project

Trend Buddy is a comprehensive, open-source trading bot designed for developers and trading enthusiasts. It provides a modular framework for fetching market data, running backtests, executing trades, and managing portfolios. The project aims to incorporate AI-powered analytics to provide deeper insights into market trends.

## Features

-   **Technical Analysis:** Generate technical analysis pages similar to TradingView.
-   **Automated Trading:**
    -   Execute buy/sell calls based on TradingView signals.
    -   Support for partial buy/sell orders.
    -   Predictive stop-loss calculation.
-   **Strategy Management:**
    -   Utilize multiple indicators with customizable weights and priorities.
    -   Sector-specific macro analysis (e.g., IT, Pharma, Banking).
-   **Portfolio Management:**
    -   Import order history from brokers via CSV (e.g., Zerodha).
    -   Track overall and daily Profit & Loss with candlestick charts.
-   **Financial Tools:**
    -   SIP calculator with customizable parameters.
    -   Candlestick pattern detection across daily, weekly, and monthly timeframes.
-   **Backtesting & Optimization:**
    -   Run backtests on historical data for any time period.
    -   Optimize strategy parameters like RSI.
-   **AI-Powered Analytics:**
    -   Perform fundamental and sentiment analysis.

## Architecture

The repository now follows a modular monolith layout so the architecture is explicit in code, not only in diagrams. A central API application orchestrates communication between the frontend shell, domain modules, data abstractions, and vendor integrations.

### Core components

-   **Frontend (WebUI):** The graphical user interface where users can interact with the application, view portfolio performance, and configure strategies.
-   **API Gateway:** The single entry point for all frontend requests. It routes calls to the appropriate internal service, such as placing an order or fetching historical data.
-   **Market Data / Data Aggregator:** This module is responsible for fetching data from multiple external sources, including:
    -   Stock exchanges (`NSE`)
    -   Financial data providers (`yFinance`)
    -   Broker APIs (`Zerodha`, `Binance`)
    It provides both historical and real-time data to the Backtesting engine and the Data Manager.
-   **Data Manager:** The persistence layer of the application. It uses databases like `MySQL` and `Sqlite3` to store all candlestick data, fundamental data, and user portfolio information.
-   **Strategy Engine:** A reusable strategy layer for `SMA`, `RSI`, and weighted custom strategies.
-   **Backtesting Engine:** Enables users to test trading strategies (e.g., SMA, RSI, Custom) against historical data provided by the Data Manager.
-   **Order Execution (OE):** Manages the lifecycle of buy and sell orders. It interfaces with various broker APIs (`Zerodha`, `Groww`, `Binance`) to execute trades and then updates the Portfolio module.
-   **Portfolio Manager:** Tracks current holdings, monitors sector-wise portfolio distribution, and helps in managing risk.
-   **Risk Engine:** Applies reusable pre-trade guardrails such as order-size and concentration checks.
-   **Analytics Engine:** An AI-powered module dedicated to performing advanced analysis, such as fundamental and sentiment analysis, to provide deeper market insights.

### Repository layout

```text
apps/
  api/                      # Backend entrypoint and route orchestration
  web/                      # Frontend shell and navigation composition

packages/
  core/                     # Domain logic
  integrations/             # Broker and market-data adapters
  data/                     # Persistence and cache abstractions
  shared/                   # Contracts, config, logging, auth, utilities

tests/
  contract/
  integration/
  e2e/
  fixtures/

docs/
  architecture/
  api/
  decisions/
```

See [docs/architecture/overview.md](docs/architecture/overview.md), [docs/api/domains.md](docs/api/domains.md), and [docs/decisions/0001-modular-monolith.md](docs/decisions/0001-modular-monolith.md) for the reasoning behind the scaffold.

<details>
<summary>View Architecture Diagram (PlantUML)</summary>

```plantuml
@startuml Trend Buddy
skin rose

state Frontend: WebUI
state "API Gateway" as API

package "Core Domains" {
  state "Market Data" as MarketData
  state "Strategy Engine" as Strategy
  state "Backtesting" as Backtesting
  state "Order Execution" as Orders
  state "Portfolio Manager" as Portfolio
  state "Risk Engine" as Risk
  state "Analytics" as Analytics
}

state "Data Manager" as DM: MySQL
DM: Sqlite3

package "Integrations" {
  state "Market Providers" as Providers
  Providers: NSE
  Providers: yFinance
  Providers: Alpha Vantage

  state "Broker APIs" as Brokers
  Brokers: Zerodha
  Brokers: Groww
  Brokers: Binance
}

' Flow
Frontend --> API : User Interaction
API --> MarketData : Ingest and Query Data
API --> Strategy : Strategy Configuration
API --> Backtesting : Simulate Strategies
API --> Orders : Buy/Sell Calls
API --> Portfolio : Holdings and P&L
API --> Analytics : Advisory Insights

MarketData --> Providers : Fetch Historical and Realtime Candles
MarketData --> DM : Store Candlestick and Fundamental Data
Backtesting --> DM : Load Historical Candles
Backtesting --> Strategy : Evaluate Rules
Orders --> Risk : Pre-trade Checks
Orders --> Brokers : Execute Orders
Orders --> Portfolio : Reflect Filled Orders
Portfolio --> DM : Persist Snapshots
Analytics --> DM : Persist Reports

@enduml
```

</details>

## Technology Stack

### Data Fetching
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Alpha Vantage](https://www.alphavantage.co/documentation/) (Planned)

### Charting & Visualization
- [Lightweight Charts](https://github.com/tradingview/lightweight-charts)

### Backtesting
- [VectorBT](https://github.com/polakowo/vectorbt)

## API References
- [Binance Spot API Docs](https://github.com/binance/binance-spot-api-docs)
- [Binance API Docs (Spot)](https://binance-docs.github.io/apidocs/spot/en/)
- [Binance Web Socket Streams](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)

## Current scaffold

-   `apps/api/src/app.js` composes the backend modules and exposes domain routes.
-   `apps/api/src/http-server.js` runs the backend as an HTTP service with JSON endpoints and a `/health` route.
-   `apps/web/src/app-shell.js` defines the frontend navigation and dashboard surface.
-   `packages/core/*` contains runnable domain modules for market data, strategies, backtesting, orders, portfolio, analytics, and risk.
-   `packages/integrations/*` contains provider adapters for brokers and market-data sources.
-   `tests/` contains contract, integration, and end-to-end smoke tests that verify the architecture stays connected.

## Docker

Build and run the backend container with:

```bash
docker build -t trend-buddy .
docker run --rm -p 3000:3000 trend-buddy
```

Available routes include `/health`, `/market-data`, `/strategies`, `/backtests`, `/orders`, `/portfolio`, and `/analytics`.
