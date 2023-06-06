"""
Purpose:
    This script will be used to call the server running in app.py to access tweets of jimcramer and send it to the
    gpt api to get stock tickers to buy.
"""

import requests

username = "jimcramer"
count = 50

url = f"http://localhost:8000/twitterdata/?username={username}&count={count}"
response = requests.get(url)

tweets = response.json()
print(tweets)
