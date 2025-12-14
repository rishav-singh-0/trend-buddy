import logging
from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

# print(kite.login_url())

# data = kite.generate_session(os.getenv("KITE_REQUEST_TOKEN"), api_secret=os.getenv("KITE_API_SECRET"))
kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))

# Place an order
try:
    order_id = kite.place_order(tradingsymbol="INFY",
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                variety=kite.VARIETY_AMO,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC,
                                validity=kite.VALIDITY_DAY)

    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))

# Fetch all orders
print(kite.orders())

# Get instruments
kite.instruments()
