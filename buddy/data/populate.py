from .models import Symbol, Candle
from datetime import date, timedelta

from decouple import config
from binance import Client

client = Client(config('API_KEY'), config('API_SECRET'))

def add_symbols():
    try:
        # getting data from binance api
        tickers = client.get_all_tickers()

        # getting data from db
        old_symbols = Symbol.objects.all()
        
        # adding only new symbols in db
        new_symbols = []
        for item in tickers:
            symbol = Symbol(symbol = item['symbol'])
            if not old_symbols.filter(symbol=item['symbol']):
                new_symbols.append(symbol)

        Symbol.objects.bulk_create(new_symbols)
        return True

    except Exception as e:
        print(str(e))
        return False

def add_candle_1day(symbol):
    '''
    Pass a symbol and get its 400 days back candlestick data
    '''
    try:
        # Checking if Symbol exists in db
        symbol = Symbol.objects.get(symbol=symbol)
        previous_candles = Candle.objects.filter(symbol=symbol)
        latest_candle_time = 0
        for item in previous_candles:
            if item.time > latest_candle_time:
                latest_candle_time = item.time
        
        # Defining Timespan for candles
        today = date.today()
        time_span = today - timedelta(days=400)
        
        # API call to binence
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, time_span.strftime("%b %d, %y"))
        
        # Adding candles all at ones
        new_klines = []
        for item in reversed(klines):
            candle = Candle(
                symbol=symbol,
                time=item[0],
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                volume=item[5]
            )
            
            # adding only new symbols in db
            check_time = item[0]
            if check_time > latest_candle_time:
                new_klines.append(candle)
            else:
                return new_klines
        return new_klines
            

    except Exception as e:
        print(e)
        return False

def populate_1day():
    # updating symbols
    add_symbols()

    symbols = Symbol.objects.all()
    new_candles = []
    for item in symbols:
        new_candles.extend(add_candle_1day(item))
        print(f"Added {item}")
    Candle.objects.bulk_create(new_candles)

if __name__=='__main__':
    add_symbols()