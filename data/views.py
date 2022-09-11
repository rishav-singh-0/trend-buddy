from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date, timedelta
from django.views import View

from rest_framework import viewsets, generics, permissions
from data.serializers import ExchangeSerializers, FavouriteSerializers, SymbolSerializers, CandleSerializers

from data.models import Exchange, Favourite, Symbol, Candle
from data.populate import CryptoPopulate, NSEPopulate


class CryotoPopulateView(View):
    def get(self, request, *args, **kwargs):
        crypto = CryptoPopulate()
        result = crypto.populate_1day(request.user)
        # result = add_candle_1day('SOLBRL')
        # result = add_symbols()
        # print(result)
        if result:
            return HttpResponse("Success !!")
        return HttpResponse("Failure !!")

class NSEPopulateView(View):
    def get(self, request, *args, **kwargs):
        stock = NSEPopulate('INFY', from_date='14-05-2020', to_date='14-05-2022')
        stock.get_history_data()
        result = stock.save_candles()
        return HttpResponse(str(result))


class ExchangeView(viewsets.ModelViewSet):
    '''
    Taking data from db about all the Exchanges available
    '''
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializers
    permission_classes = [permissions.IsAuthenticated]

class SymbolView(viewsets.ModelViewSet):
    '''
    Taking data from db about all the symbols available
    '''
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        symbols = Symbol.objects.all()
        # processed_symbols = serializers.serialize('json', symbols)
        processed_symbols = []
        for item in symbols:
            processed_symbols.append({item.pk : item.symbol})
        return JsonResponse(processed_symbols, safe=False)


class FavouriteView(viewsets.ModelViewSet):
    '''
    Taking data from db about all the Exchanges available
    '''
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        symbol_id = request.POST['symbol_id']
        symbol = Symbol.objects.get(pk = symbol_id)
        favourite = True

        like_object, created = Favourite.objects.get_or_create(user_id = request.user, symbol_id = symbol)
        if not created:
            like_object.delete() # the user already favourited this symbol before
            favourite = False
        
        return JsonResponse({'favourite':favourite})

class CandleView(viewsets.ModelViewSet):
    '''
    Taking data from db and converting it to candlesticks
    '''
    queryset = Candle.objects.all()
    serializer_class = CandleSerializers
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     queryset = Candle.objects.all()
    #     try:
    #         symbol = Symbol.objects.get(symbol=symbol)
    #         candles = Candle.objects.filter(symbol=symbol)
    #     except Exception as e:
    #         return JsonResponse({'error': str(e)})
        
    #     processed_candlesticks = []
    #     for data in candles:
    #         candlestick = { 
    #             'time': data.time, 
    #             'open': data.open, 
    #             'high': data.high, 
    #             'low': data.low, 
    #             'close': data.close 
    #         }
    #         processed_candlesticks.append(candlestick)
            
    #     # return JsonResponse(processed_candlesticks, safe=False)
    #     return queryset
    
