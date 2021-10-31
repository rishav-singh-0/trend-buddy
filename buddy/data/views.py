from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views import View

from decouple import config
from binance import Client

client = Client(config('API_KEY'), config('API_SECRET'))

class SymbolView(View):

    def get(self, request, *args, **kwargs):
        # prices = client.get_all_tickers()
        # print(prices)
        klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2021")
        print(klines)
        
        return HttpResponse("Working!!")