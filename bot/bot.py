from data.models import Symbol, Candle
from analysis.statergy import Statergy

import websocket, json, pprint

from decouple import config
from binance.client import Client
from binance.enums import *


class Bot():
    '''
    Subscribes to binance webhook to get realtime candlesticl data and generates
    buy or sell calls based on `Statergies` discribed

    Input:
        - symbol
    '''

    def __init__(self, symbol):
        self.symbol = Symbol.objects.get(symbol=symbol)
        self.socket = f"wss://stream.binance.com:9443/ws/{self.symbol.symbol.lower()}@kline_1m"
        self.candle_list = []
        
    def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print("sending order:", side)
            # order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            # print(order)
        except Exception as e:
            print("an exception occured -", e)
            return False

        return True

    def on_open(self, ws):
        print('opened connection')

    def on_close(self, ws):
        print('closed connection')

    def on_message(self, ws, message):
        global closes
        
        # print('received message')
        json_message = json.loads(message)
        # pprint.pprint(json_message)

        raw_candle = json_message['k']

        is_candle_closed = raw_candle['x']

        # if True:
        if is_candle_closed:

            candle = Candle(
                symbol=self.symbol,
                time=raw_candle['t'],
                open=float(raw_candle['o']),
                high=float(raw_candle['h']),
                low=float(raw_candle['l']),
                close=float(raw_candle['c']),
                volume=float(raw_candle['v'])
            )
            # candle.save()

            print(f"candle closed at {candle.close}")
            self.candle_list.append(candle)
            print('No. of candles: ',len(self.candle_list))

            if len(self.candle_list) > 14:
                statergy = Statergy(self.candle_list)
                statergy.rsi(14, 70, 30)
                statergy.macd()


    def start(self):
        ws = websocket.WebSocketApp(
                self.socket, 
                on_open=self.on_open, 
                on_close=self.on_close,
                on_message=self.on_message
            )
        ws.run_forever()