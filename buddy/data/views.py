import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from datetime import date, timedelta

from django.views import View
from .populate import add_symbols, add_candle_1day

from decouple import config
from binance import Client

client = Client(config('API_KEY'), config('API_SECRET'))

class SymbolView(View):

    def get(self, request, *args, **kwargs):
        # add_candle_1day("BTCUSDT")
        # Defining Timespan for candles
        today = date.today()
        time_span = today - timedelta(days=400)
        
        # API call to binence
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, time_span.strftime("%b %d, %y"))
        print(klines)
        
        return HttpResponse("Working!!")