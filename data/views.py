from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.views import View

from rest_framework import viewsets, generics, permissions, views
from bot.models import Trade
from data.serializers import ExchangeSerializers, FavouriteSerializers, SymbolSerializers, CandleSerializers

from data.models import Exchange, Favourite, Symbol, Candle
from data.populate import CryptoPopulate, NSEPopulate, NSEList, PopulateYF

from django.core.serializers import json
json_serializer = json.Serializer()


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

class NSEPopulateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols_list = NSEList()
        _ = symbols_list.pull()
        new_symbols = symbols_list.save_symbols()
        result = json_serializer.serialize(new_symbols)
        return Response(result)

    def post(self, request, format=None):
        data = request.query_params
        # print(data)
        # stock = NSEPopulate(data['symbol'], from_date=data['from_date'], to_date=data['to_date'])
        stock = PopulateYF(data['symbol'], from_date=data['from_date'], to_date=data['to_date'])
        stock.get_history_data()
        result = stock.save_candles()
        result = json_serializer.serialize(result)
        # print(result, type(result))
        return Response(result)


class ExchangeView(views.APIView):
    '''
    Taking data from db about all the Exchanges available
    '''
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Exchange.objects.all()
        serializer = ExchangeSerializers(queryset, many=True)
        return Response(serializer.data)

class SymbolView(views.APIView):
    '''
    Taking data from db about all the symbols available
    '''
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        queryset = Symbol.objects.all()
        serializer = SymbolSerializers(queryset, many=True)
        return Response(serializer.data)


class FavouriteView(views.APIView):
    '''
    Taking data from db about all the Exchanges available
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get():
        queryset = Favourite.objects.all()
        serializer = FavouriteSerializers(queryset, many=True)
        return Response({'favourates': serializer.data})

    def post(self, request, *args, **kwargs):
        symbol_id = request.POST['symbol_id']
        symbol = Symbol.objects.get(pk = symbol_id)
        favourite = True

        like_object, created = Favourite.objects.get_or_create(user_id = request.user, symbol_id = symbol)
        if not created:
            like_object.delete() # the user already favourited this symbol before
            favourite = False
        
        return Response(favourite)

class CandleView(views.APIView):
    '''
    Taking data from db and converting it to candlesticks
    '''
    queryset = Candle.objects.all()
    serializer = CandleSerializers(queryset, many=True)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            symbol="TCS"
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
                'close': data.close,
                'volume': data.volume,
                'no_of_trades': data.no_of_trades
            }
            processed_candlesticks.append(candlestick)
            
        return Response(processed_candlesticks, safe=False)
