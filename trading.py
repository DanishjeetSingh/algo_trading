"""
Purpose:
    This script will be used to call the alpaca account with the stock to buy in the beginning of the day,
    at the end of the day we cancel all the orders and liquidate
"""

import logging
import time
from configparser import ConfigParser
from alpaca.trading.client import TradingClient
from gpt import get_stocks
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType

logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config = ConfigParser(interpolation=None)
config.read('config.ini')

trading_client = TradingClient(api_key=config['ALPACA']['api_key'], secret_key=config['ALPACA']['secret_key'], paper=True)

buy_stocks = get_stocks(api_key=config['OPENAI']['api_key'], bearer_token = config['TWITTER_CREDS']['bearer_token'])
# print(buy_stocks)

liquidate = trading_client.close_all_positions(cancel_orders=True)
# print(liquidate)
if liquidate:
    logging.info('Liquidated all positions and canceled orders')
else:
    logging.info("Nothing to liquidate")

# gotta wait for some time so the stocks can have some time to liquidate
time.sleep(100)
# getting account info after liquidation so buying power is maximum
account = trading_client.get_account()

# Setting parameters for our buy order
if not buy_stocks:
    logging.info(f'No stocks to buy today')
else:
    market_order_data = MarketOrderRequest(
                          symbol=buy_stocks[0],
                          # qty=1,
                          notional= int(float(account.buying_power) * 0.9),
                          side=OrderSide.BUY,
                          type= OrderType.MARKET,
                          time_in_force=TimeInForce.DAY
                      )
    logging.info(f'Buying {buy_stocks[0]}')
    market_order = trading_client.submit_order(market_order_data)
    logging.info(f'Submitted buy order: {market_order}')

