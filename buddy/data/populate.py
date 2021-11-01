from .models import Symbol, Candle
from datetime import date, timedelta

from decouple import config
from binance import Client

client = Client(config('API_KEY'), config('API_SECRET'))

def add_symbols():
    try:
        tickers = client.get_all_tickers()
        objs = [
            Symbol(
                symbol=item['symbol']
            )
            for item in tickers
        ]
        bulk_symbols = Symbol.objects.bulk_create(objs)
        return bulk_symbols

    except Exception as e:
        return str(e)

def add_candle_1day(symbol):
    try:
        # Checking if Symbol exists in db
        symbol = Symbol.objects.get(symbol=symbol)
        
        # Defining Timespan for candles
        today = date.today()
        time_span = today - timedelta(days=400)
        
        # API call to binence
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, time_span.strftime("%b %d, %y"))
        
        # Adding candles all at ones
        objs = [
            Candle(
                symbol=symbol,
                time=item[0]/1000,
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                volume=item[5]
            )
            for item in klines
        ]
        bulk_candles = Candle.objects.bulk_create(objs)
        return bulk_candles

    except Exception as e:
        print(e)
        return False
    
if __name__=='__main__':
    add_symbols()