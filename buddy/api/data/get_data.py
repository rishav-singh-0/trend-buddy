import pandas as pd
import yfinance as yf
from datetime import datetime
from .models import Exchange, Symbol, Candle

class BaseDataFetcher():
    def __init__(self, symbol, exchange):
        self.symbol = Symbol.objects.filter(symbol=symbol)[0]
        self.exchange = Exchange.objects.filter(exchange=exchange)[0]
        self.candle_data = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        self.input_date_format="%d-%m-%Y"
        self.date_format="%d-%m-%Y"

    def fetch_data(self, start_date, end_date):
        # TODO: Validate date format
        raise NotImplementedError("Subclasses must implement this method")

    def filter_data(self, data):
        # TODO: Implement data filtartation logic
        raise NotImplementedError("Subclasses must implement this method")
    
    def format_date(self, date):
        '''
        Input date format is fixed, so this function changes the format to the
        type required by respective api
        '''
        date = datetime.strptime(date, self.input_date_format)
        return date.strftime(self.date_format)

    def save_to_database(self):
        existing_times = set(Candle.objects.filter(symbol=self.symbol).values_list('time', flat=True))
        new_candles = []

        for _, data in self.candle_data.iterrows():
            if data['time'] not in existing_times:
                candle = Candle(
                    symbol=self.symbol.symbol,
                    time=data['time'],
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    volume=data['volume'],
                )
                new_candles.append(candle)
        try:
            Candle.objects.bulk_create(new_candles)
        except Exception as e:
            print(e)
        return new_candles

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.candle_data)
        df.to_csv(filename, index=False)

