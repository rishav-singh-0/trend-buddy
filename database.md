data:
    symbols:
        time
        open
        high
        low
        close
        volume


DATA
get data from binance api
store in sql
connect websocket with database

day candle for 400 days
15 min candle for week
min candle for a day


VISUALISE
integrate `lightweight chart` in jinja2
take data from db and make chart

ANALYSIS
use TA-Lib library and impliment some technical analysis on data from db

ACTION
make buy or sell calls through binance api