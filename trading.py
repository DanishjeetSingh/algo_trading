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

trading_client = TradingClient(api_key=config['ALPACA']['api_key'], secret_key=config['ALPACA']['secret_key'], paper=True)

# account = trading_client.get_account()
# for property_name, value in account:
#   print(f"\"{property_name}\": {value}")

buy_stocks = get_stocks(api_key=config['OPENAI']['api_key'])
# print(buy_stocks)
liquidate = trading_client.close_all_positions(cancel_orders=True)
print(liquidate)
# Setting parameters for our buy order
market_order_data = MarketOrderRequest(
                      symbol=buy_stocks[0],
                      qty=1,
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.UTC
                  )
print(f'currently buying {buy_stocks[0]}')
# cancel and liquidate and all the orders


# Submitting the order and then printing the returned object
market_order = trading_client.submit_order(market_order_data)

# print(len(market_order))
# for property_name, value in market_order:
  # print(f"\"{property_name}\": {value}")