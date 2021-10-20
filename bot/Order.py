'''
This file contains functionality of buying and selling
'''

from binance.enums import *

def order(client, side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

# class Order:
#     def __init__(self, client, side: str, symbol: str, quantity: float, order_type):
#         pass

        