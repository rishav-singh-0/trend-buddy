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
