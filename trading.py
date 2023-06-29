"""
Purpose:
    This script will be used to call the alpaca account with the stock to buy in the beginning of the day,
    at the end of the day we cancel all the orders and liquidate
"""

import logging
from configparser import ConfigParser
from datetime import datetime

from alpaca.trading.client import TradingClient
from gpt import get_stocks
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config = ConfigParser(interpolation=None)
config.read('config.ini')

trading_client = TradingClient(api_key=config['ALPACA']['api_key'], secret_key=config['ALPACA']['secret_key'], paper=True)

buy_stocks = get_stocks(api_key=config['OPENAI']['api_key'], bearer_token = config['TWITTER_CREDS']['bearer_token'])

liquidate = trading_client.close_all_positions(cancel_orders=True)
# print(liquidate)
if liquidate:
    logging.info('Liquidated all positions and canceled orders')
else:
    logging.info("Nothing to liquidate")

# Setting parameters for our buy order
if not buy_stocks:
    logging.info(f'No stocks to buy today')
else:
    market_order_data = MarketOrderRequest(
                          symbol=buy_stocks[0],
                          qty=1,
                          side=OrderSide.BUY,
                          time_in_force=TimeInForce.DAY
                      )
    logging.info(f'Buying {buy_stocks[0]}')
    market_order = trading_client.submit_order(market_order_data)
    logging.info(f'Submitted buy order: {market_order}')

