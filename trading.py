"""
Purpose:
    This script will be used to call the alpaca account with the stock to buy in the beginning of the day,
    at the end of the day we cancel all the orders and liquidate
"""

from configparser import ConfigParser
from alpaca.trading.client import TradingClient
from gpt import get_stocks
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

config = ConfigParser(interpolation=None)
config.read('config.ini')
api_key = config['ALPACA']['api_key']
secret_key = config['ALPACA']['secret_key']

trading_client = TradingClient(api_key, secret_key, paper=True)

account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")

buy_stocks = get_stocks()
print(buy_stocks)

# Setting parameters for our buy order
market_order_data = MarketOrderRequest(
                      symbol=buy_stocks[0],
                      qty=1,
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.GTC
                  )

# Submitting the order and then printing the returned object
market_order = trading_client.submit_order(market_order_data)
for property_name, value in market_order:
  print(f"\"{property_name}\": {value}")