# Trend Buddy
An OpenSource Trading bot

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### MakeFile

Run build make command with tests
```bash
make all
```

Build the application
```bash
make build
```

Run the application
```bash
make run
```
Create DB container
```bash
make docker-run
```

Shutdown DB Container
```bash
make docker-down
```

DB Integrations Test:
```bash
make itest
```

Live reload the application:
```bash
make watch
```

Run the test suite:
```bash
make test
```

Clean up binary from the last build:
```bash
make clean
```

# References
- https://github.com/binance/binance-spot-api-docs
- https://binance-docs.github.io/apidocs/spot/en/
- https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md


------------------------------------
Workflow
------------------------------------


# DATA
get data from binance api
store in sql
connect websocket with database

day candle for 400 days
15 min candle for 2 days

# VISUALISE
integrate `lightweight chart` in jinja2
take data from db and make chart

## ANALYSIS
use TA-Lib library and impliment some technical analysis on data from db

# ACTION
make buy or sell calls through binance api


------------------------------------
## Idea
- Generate Technical page like [TradingView technical page](https://in.tradingview.com/symbols/MATICUSDT/technicals/)
- Use trading view to send buy and sell calls
- Partial buy and sell
- Predict stoploss
- Use multiple indicators and give them priority or waitage
- Macro analysis for specific sectors like IT, electronics, pharma, consumer,
  bank, etc

#### Import orders
- Import csv files which are exported from brokers like Zerodha to populate the
  orders table

#### Profit and Loss Chart
- Portfolio for showing overall Profit and Loss
- Daily candlestick chart for profit and loss

#### Financial Calculator
- Sip calculator, select index or equity, select time duration, select amount
  per month, select amount growth % per month, calculate the final return
  compared to the total amount invested
- Cycle through daily, weekly, monthly candle data and check for candlestick
  patterns

### Tools Used
#### Data fetching
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Alpha Vantage](https://www.alphavantage.co/documentation/) (TODO)

#### Chart and Data Visualization
- [Lightweight Charts](https://github.com/tradingview/lightweight-charts)

#### Backtesting
- [VectorBT](https://github.com/polakowo/vectorbt)

### Analysis
Backtesting
Parameter Optimization(RSI)
Fundamental Analysis based on numbers

## Prompt
Generate a Go project(trend-buddy) with following standard design patterns with keeping in mind points like scalibility and simplicity.
This tool should contain modular design for
1. fetching and maintaining data
2. running backtests on any timeperiod of a data
3. execute paper-trade or actual trade orders (in future, it could support multiple broker platforms like zerodha, grow, dhan, etc.)
4. portfolio management to manage existing orders and portfolio
5. database management module: for storing all the tables and everything (use mysql for now, but keep the design in such a way to include multiple databases)
6. analytics using ai (fundamenta, sentiments, etc.)
7. Frontend module: can use any simple thing right now (in future maybe migrate to vue, but not sure)
------------------------------------

# Trend Buddy
An OpenSource Trading bot

# References
- https://github.com/binance/binance-spot-api-docs
- https://binance-docs.github.io/apidocs/spot/en/
- https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

# Features

## Data
- Makes api calls to binance and fetches realtime data
- Stores data in sqlite3 database
- Provides endpoints to access the data from db

### Remaining
- Automate fetching and storing in db, or use websocket somehow
- Use [asyncio](https://youtu.be/XdvBAh7pa5U)

## Analysis
- Get data from `data` app according to user's selection
- Show candlestick chart from TradingView widget
- Select favourite symbols from all available symbols
- Use `TA-Lib` for technical analysis

### Remaining
- Generate latest strategies' value (eg. rsi, macd, etc.) and show it in same
  table

## Bot
- Take data from binance websocket
- Automate using RQ-Worker
- Take strategies and from analysis app and generate buy or sell calls

### Remaining
- Add order history in db

## TODO
- Generate Technical page like [TradingView technical page](https://in.tradingview.com/symbols/MATICUSDT/technicals/)
    
# Idea
- Use trading view to send buy and sell calls
- Partial buy and sell
- Predict stoploss
- Use multiple indicators and give them priority or waitage
- Macro analysis for specific sectors like IT, electronics, pharma, consumer,
  bank, etc

## Import orders
- Import csv files which are exported from brokers like Zerodha to populate the
  orders table

## Profit and Loss Chart
- Portfolio for showing overall Profit and Loss
- Daily candlestick chart for profit and loss

## Financial Calculator 
- Sip calculator, select index or equity, select time duration, select amount
  per month, select amount growth % per month, calculate the final return
  compared to the total amount invested
- Cycle through daily, weekly, monthly candle data and check for candlestick
  patterns

# Tools Used

## Data fetching

- [yfinance](https://github.com/ranaroussi/yfinance)
- [Alpha Vantage](https://www.alphavantage.co/documentation/) (TODO)

## Chart and Data Visualization

- [Lightweight Charts](https://github.com/tradingview/lightweight-charts)

## Backtesting

- [VectorBT](https://github.com/polakowo/vectorbt)

# Installation

Install TA-Lib

- Using conda
```
conda install -c conda-forge ta-lib
```
- See [this](https://mrjbq7.github.io/ta-lib/install.html) if not using conda

Python dependencies
```
pip install -r requirements.txt
```
