# Importing Libraries
import websocket
import json
import pprint
import talib
import numpy
from decouple import config
from binance.client import Client
from binance.enums import *


class Buddy:
    def __init__(self, symbol):
        
        self.symbol = symbol

        SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

        RSI_PERIOD = 14
        RSI_OVERBOUGHT = 70
        RSI_OVERSOLD = 30
        TRADE_SYMBOL = 'ETHUSD'
        TRADE_QUANTITY = 0.05

        closes = []
        in_position = False

        client = Client(config('API_KEY'), config('API_SECRET'))

    def on_open(ws):
        print('opened connection')

    def on_close(ws):
        print('closed connection')
    
    def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
        try:
            print("sending order")
            order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print(order)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False

        return True

