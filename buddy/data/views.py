from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date, timedelta
from django.views import View

from data.models import Symbol, Candle
from .populate import add_symbols, add_candle_1day, populate_1day


class PopulateView(View):

    def get(self, request, *args, **kwargs):
        result = populate_1day()
        # result = add_candle_1day('SOLBRL')
        # result = add_symbols()
        print(result)
        if result:
            return HttpResponse("Success !!")
        return HttpResponse("Failure !!")


class SymbolView(View):
    '''
    Taking data from db about all the symbols available
    '''
    
    def get(self, request, *args, **kwargs):
        symbols = Symbol.objects.all()
        # processed_symbols = serializers.serialize('json', symbols)
        processed_symbols = []
        for item in symbols:
            processed_symbols.append({item.pk : item.symbol})
        return JsonResponse(processed_symbols, safe=False)


class CandleView(View):
    '''
    Taking data from db and converting it to candlesticks
    '''

    def get(self, request, symbol, *args, **kwargs):

        try:
            symbol = Symbol.objects.get(symbol=symbol)
            candles = Candle.objects.filter(symbol=symbol)
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
        processed_candlesticks = []
        for data in candles:
            candlestick = { 
                'time': data.time, 
                'open': data.open, 
                'high': data.high, 
                'low': data.low, 
                'close': data.close 
            }
            processed_candlesticks.append(candlestick)
            
        return JsonResponse(processed_candlesticks, safe=False)