import pandas as pd
from .models import Symbol, Candle

class BaseDataFetcher():
    def __init__(self, symbol):
        self.symbol = symbol
        self.candle_data = pd.DataFrame()

    def fetch_data(self, start_date, end_date):
        # TODO: Validate date format
        raise NotImplementedError("Subclasses must implement this method")

    def filter_data(self, data):
        # TODO: Implement data filtartation logic
        raise NotImplementedError("Subclasses must implement this method")

    def save_to_database(self):
        symbol = Symbol.objects.filter(symbol=self.symbol)[0]
        existing_times = set(Candle.objects.filter(symbol=self.symbol).values_list('time', flat=True))
        new_candles = []

        for _, data in self.candle_data.iterrows():
            if data['time'] not in existing_times:
                candle = Candle(
                    symbol=symbol,
                    time=data['time'],
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    volume=data['volume'],
                )
                new_candles.append(candle)
        try:
            # print(new_candles)
            Candle.objects.bulk_create(new_candles)
        except Exception as e:
            print(e)

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.candle_data)
        df.to_csv(filename, index=False)

