from data.models import Symbol, Candle
from analysis.statergy import macd, rsi

import websocket, json, pprint

from decouple import config
from binance.client import Client
from binance.enums import *

global symbol, candle_list


candle_list = []

class Bot():
    def __init__(self, symbol):
        self.symbol = Symbol.objects.get(symbol=symbol)
        self.socket = f"wss://stream.binance.com:9443/ws/{self.symbol.symbol.lower()}@kline_1m"
        
    def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
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
            candle_list.append(candle)
            print(len(candle_list))
            # macd(candle_list)
            if len(candle_list) > 14:
                rsi(candle_list[-15:], 14, 70, 30)


    def main(self):
        ws = websocket.WebSocketApp(
                self.socket, 
                on_open=self.on_open, 
                on_close=self.on_close,
                on_message=self.on_message
            )
        ws.run_forever()