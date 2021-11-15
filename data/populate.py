from .models import Symbol, Candle
from time import mktime
from datetime import date, timedelta, datetime

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

def add_candle_1day(symbol, previous_candles):
    '''
    Pass a symbol and queryset of previous candles for same symbol
    Checking latest date of candle from db and adding further days candle till present date
    Returns its 400 days back candlestick data at max
    Assuming that no data is missing from between two candles
    '''

    try:
        # Checking if Symbol exists in db
        latest_candle_time = 0
        for item in previous_candles:
            if item.time > latest_candle_time:
                latest_candle_time = item.time
        
        # Defining Timespan for candles
        today = date.today()
        time_span = today - timedelta(days=400)
        
        # returning if latest date is today
        unix_time_today = mktime(datetime.strptime(today.isoformat(), "%Y-%m-%d").timetuple())
        if latest_candle_time/1000 == unix_time_today:
            return []

        # API call to binence
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, time_span.strftime("%b %d, %y"))
        
        # Adding candles all at ones
        new_klines = []
        for item in reversed(klines):

            check_time = item[0]
            if check_time <= latest_candle_time:
                break

            # adding only new symbols in db
            candle = Candle(
                symbol=symbol,
                time=item[0],
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                volume=item[5]
            )
            new_klines.append(candle)

        Candle.objects.bulk_create(new_klines)
        return new_klines
            

    except Exception as e:
        print(e)
        return False

def populate_1day(user):
    # updating symbols
    add_symbols()
    candles = []

    favourite_symbols = user.favourites.all()
    all_candles = Candle.objects.all()
    for item in favourite_symbols:
        candles = add_candle_1day(item.symbol_id, all_candles.filter(symbol=item.symbol_id))
    return candles
