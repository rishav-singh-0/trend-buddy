import io
from rest_framework import serializers
from .models import Favourite, Exchange, Symbol, Candle
from django.contrib.auth.models import User
from .populate import CsvTradePopulate
import pandas as pd


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
    
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, data):
        print(data,'\n\n')
        # print(data['file'].read())
        trade_data = CsvTradePopulate(User.objects.get(username='rishav'))
        decoded_file = data['file'].read().decode()
        io_string = io.StringIO(decoded_file)
        trade_data.csv_data = pd.read_csv(io_string)
        trade_data.format_zerodha()
        trade_data.add_trade()
        
        return trade_data.save_trade()[0]
        
    class Meta:
        fields = ('file',)