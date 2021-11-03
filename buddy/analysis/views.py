from django.shortcuts import render
from django.views import View

from data.models import Symbol, Candle


class SymbolListView(View):

    def get(self, request, *args, **kwargs):

        symbols = Symbol.objects.all()
        favourite_symbol = []

        for favourite in request.user.favourites.all(): # likes is the related name used in models
            favourite_symbol.append(favourite.symbol_id)
        print('symbols:',favourite_symbol)
        return render(request, 'analysis/all-symbols.html', {'symbols': symbols, 'favourites': favourite_symbol})


class ChartView(View):

    def get(self, request, symbol, *args, **kwargs):

        processed_candlesticks = []
        symbol = Symbol.objects.get(symbol=symbol)
        candles = Candle.objects.filter(symbol=symbol)
        
        for data in candles:
            candlestick = { 
                'time': data.time, 
                'open': data.open, 
                'high': data.high, 
                'low': data.low, 
                'close': data.close 
            }
            processed_candlesticks.append(candlestick)

        return render(request, 'analysis/chart.html', {'data': processed_candlesticks})


class SelectionFormView():
    pass

class AnalysisView(View):
    
    def get(self, request, *args, **kwargs):
        
        return render(request, 'analysis/analysis.html', {'data': ''})