from django.shortcuts import render, HttpResponse
from django.views import View

from data.models import Symbol, Candle

class ChartView(View):

    def get(self, request, *args, **kwargs):

        processed_candlesticks = []
        symbol = Symbol.objects.get(symbol="BTCUSDT")
        candles = Candle.objects.filter(symbol=symbol)
        print(candles)
        
        for data in candles:
            candlestick = { 
                'time': data.time, 
                'open': data.open, 
                'high': data.high, 
                'low': data.low, 
                'close': data.close 
            }
            processed_candlesticks.append(candlestick)

        return render(request, 'analysis/index.html', {'data': processed_candlesticks})