
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
- Generate latest statergies' value (eg. rsi, macd, etc.) and show it in same table

## Bot

- Take data from binance websocket
- Automate using RQ-Worker
- Take statergies and from analysis app and generate buy or sell calls

## TODO

- Generate Technical page like [TradingView technical page](https://in.tradingview.com/symbols/MATICUSDT/technicals/)
- Portfolio for showing overall Profit and Loss
    
# Idea

- Use trading view to send buy and sell calls
- Partial buy and sell
- Pridict stoploss