from data.models import Symbol, Candle
from bot.models import Trade
from time import mktime
from datetime import date, timedelta, datetime

# Crypto
from decouple import config
from binance import Client

# Stock
from io import StringIO
from time import sleep
import requests
import pandas as pd
from  datetime import datetime, timedelta
import bs4


class CryptoPopulate():
    def __init__(self):
        self.client = Client(config('API_KEY'), config('API_SECRET'))

    def add_symbols(self):
        try:
            # getting data from binance api
            tickers = self.client.get_all_tickers()

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

    def add_candle_1day(self, symbol, previous_candles):
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
            klines = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, time_span.strftime("%b %d, %y"))
            
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
                    volume=item[5],
                    no_of_trades=item[8]
                )
                new_klines.append(candle)

            Candle.objects.bulk_create(new_klines)
            return new_klines
                

        except Exception as e:
            print(e)
            return False

    def populate_1day(self, user):
        # updating symbols
        self.add_symbols()
        candles = []

        favourite_symbols = user.favourites.all()
        all_candles = Candle.objects.all()
        for item in favourite_symbols:
            candles = self.add_candle_1day(item.symbol_id, all_candles.filter(symbol=item.symbol_id))
        return candles

class NSEPopulate():
    '''
    input example: 
        - 'TCS' 
        - from_date='14-05-2015'
        - to_date='14-05-2022'
    output:
        populate the database with 'TCS' symbol
    '''
    
    session = None
    symbol = None

    def __init__(self, symbol, 
                 from_date=(datetime(datetime.today().year - 1, datetime.today().month,datetime.today().day).strftime("%d-%m-%Y")),
                 to_date=(datetime.today().strftime("%d-%m-%Y"))
             ):
        self.head = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        self.session = requests.session()
        self.symbol=symbol
        self.from_date=from_date
        self.to_date=to_date
        self.df=pd.DataFrame()
        # print("Preparing...")
        
    def get_history_data(self):
        '''
        Check if timeframe is over 2 years because NSE does not allow more
        than 2 years at a time
        '''
        dataframe = pd.DataFrame()
        
        # calculating dates
        from_date = datetime.strptime(self.from_date, "%d-%m-%Y")
        to_date = datetime.strptime(self.to_date, "%d-%m-%Y")
        diff = to_date.year - from_date.year
        if diff<=2:
            # single request works if date diffrence is less than 2 years
            dataframe = self._get_equity_data(self.from_date, self.to_date)

        else:
            # fetch data in parts of 2 years segment
            for i in range(0,int(diff/2)+1):
                d = to_date.year - (i+1)*2
                if d < from_date.year:
                    d = from_date.year 

                date1=datetime(d, from_date.month, from_date.day).strftime("%d-%m-%Y")
                date2=datetime(to_date.year - i*2, to_date.month, to_date.day).strftime("%d-%m-%Y")
                dataframe.append(self._get_equity_data(date1, date2))
                
                # adding some delay before making next request
                sleep(0.2)
        return dataframe

    def _get_equity_data(self, from_date, to_date):
        '''
        Gets equity data from NSE in 2 years time segment
        '''
        print("Fetching...", from_date)
        self.session.get("https://www.nseindia.com", headers=self.head)
        self.session.get("https://www.nseindia.com/get-quotes/equity?symbol=" + self.symbol, headers=self.head)  # to save cookies
        self.session.get("https://www.nseindia.com/api/historical/cm/equity?symbol="+self.symbol, headers=self.head)
        url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + self.symbol + \
            "&series=[%22EQ%22]&from=" + from_date + \
            "&to=" + to_date + "&csv=true"
        webdata = self.session.get(url=url, headers=self.head)
        dataframe = pd.read_csv(StringIO(webdata.text[3:]))
        self.filter_data(dataframe)
        return self.df

    def _date_srt_to_unix(self, row):
        # print(type(row))
        # DATE format = "14-05-2022"
        date = datetime.strptime(row['Date '], '%d-%b-%Y').timestamp()
        return int(date)

    def filter_data(self, dataframe):
        # dataframe['Date '] = dataframe.apply(self._date_srt_to_unix, axis=1)
        dataframe['Date '] = dataframe['Date '].map(lambda x: datetime.strptime(x, '%d-%b-%Y').timestamp()).astype(int)
        dataframe['OPEN '] = dataframe['OPEN '].replace('\D', '', regex=True).astype(int)/100
        dataframe['HIGH '] = dataframe['HIGH '].replace('\D', '', regex=True).astype(int)/100
        dataframe['LOW '] = dataframe['LOW '].replace('\D', '', regex=True).astype(int)/100
        dataframe['PREV. CLOSE '] = dataframe['PREV. CLOSE '].replace('\D', '', regex=True).astype(int)/100
        dataframe['ltp '] = dataframe['ltp '].replace('\D', '', regex=True).astype(int)/100
        dataframe['close '] = dataframe['close '].replace('\D', '', regex=True).astype(int)/100
        dataframe['vwap '] = dataframe['vwap '].replace('\D', '', regex=True).astype(int)/100
        dataframe['52W H '] = dataframe['52W H '].replace('\D', '', regex=True).astype(int)/100
        dataframe['52W L '] = dataframe['52W L '].replace('\D', '', regex=True).astype(int)/100
        dataframe['VALUE '] = dataframe['VALUE '].replace('\D', '', regex=True).astype(int)/100
        # print(dataframe.head())
        # print(dataframe['Date '].dtype)
        self.df = dataframe
        
    def save_csv(self):
        if not self.df.empty:
            self.df.to_csv(self.symbol+'.csv',index=False)
    
    def save_candles(self):
        symbol = Symbol.objects.filter(symbol=self.symbol)[0]
        prev_candles = Candle.objects.filter(symbol=symbol)
        # old_symbols = Symbol.objects.all()
        candles = []
        for index, data in self.df.iterrows():
            candle = Candle(
                symbol=symbol,
                time=data['Date '],
                open=data['OPEN '],
                high=data['HIGH '],
                low=data['LOW '],
                close=data['close '],
                volume=data['VOLUME '],
                no_of_trades=data['No of trades ']
            )
            if(not prev_candles.filter(time=data['Date '])): 
                candles.append(candle)
        try:
            Candle.objects.bulk_create(candles)
        except Exception as e:
            print(e)
        return candles

    def getId(self, name):
        '''
        Search atring and get its symbol name

        input: 'tata motors'
        output: TATAMOTORSEQN
        '''
        search_url = 'https://www.nseindia.com/api/search/autocomplete?q={}'
        get_details = 'https://www.nseindia.com/api/quote-equity?symbol={}'
        self.session.get('https://www.nseindia.com/', headers=self.head)
        search_results = self.session.get(url=search_url.format(name), headers=self.head)
        search_result = search_results.json()['symbols'][0]['symbol']

        company_details = self.session.get(url=get_details.format(search_result), headers=self.head)
        return company_details.json()['info']['identifier']

class CsvTradePopulate():
    def __init__(self, user):
        self.user = user
        self.csv_data = pd.DataFrame()
        self.trade_list = []

    def read_csv(self, path):
        with open(path) as f:
            self.csv_data = pd.read_csv(f)
    
    def format_zerodha(self):
        # self.csv_data['order_execution_time'] = pd.to_datetime(self.csv_data['order_execution_time'], format="%Y-%m-%dT%H:%M:%S")
        self.csv_data['order_execution_time'] = self.csv_data['order_execution_time'].map(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S').timestamp()).astype(int)
        self.csv_data['trade_type'] = self.csv_data['trade_type'].str.upper()
        print(self.csv_data)
    
    def add_trade(self):
        for index, data in self.csv_data.iterrows():
            print(data['symbol'])
            trade = Trade(
                user_id = self.user,
                symbol_id = Symbol.objects.get(symbol=data['symbol']),
                trade_type = data['trade_type'],
                quantity = data['quantity'],
                price = data['price'],
                order_execution_time = data['order_execution_time']
            )
            self.trade_list.append(trade)

    def save_trade(self):
        try:
            Trade.objects.bulk_create(self.trade_list)
        except Exception as e:
            print(e)
        return self.trade_list
