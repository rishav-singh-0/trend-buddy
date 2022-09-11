import os
from rest_framework import serializers
from .models import Favourite, Exchange, Symbol, Candle


class ExchangeSerializers(serializers.ModelSerializer):
    '''
    This is Serializer for Track model
    '''
    class Meta:
        model = Exchange
        fields = '__all__'

class SymbolSerializers(serializers.ModelSerializer):
    '''
    This is Serializer for Track model
    '''
    class Meta:
        model = Symbol
        fields = '__all__'

class  CandleSerializers(serializers.ModelSerializer):
    '''
    This is Serializer for Track model
    '''
    class Meta:
        model = Candle
        fields = '__all__'

class FavouriteSerializers(serializers.ModelSerializer):
    '''
    This is Serializer for Track model
    '''
    class Meta:
        model = Favourite
        fields = '__all__'