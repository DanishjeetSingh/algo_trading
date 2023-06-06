"""
Purpose:
    This script will be used to call the server running in app.py to access tweets of jimcramer and send it to the
    gpt api to get stock tickers to sell.
"""
import re
from configparser import ConfigParser
import openai
import requests

username = "jimcramer"
count = 50

url = f"http://localhost:8000/twitterdata/?username={username}&count={count}"
response = requests.get(url)

tweets = response.json()
# print(tweets)

config = ConfigParser(interpolation=None)
config.read('config.ini')
openai.api_key = config['OPENAI']['api_key']

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="f{tweets} Jim Cramer recommends selling the following stock tickers: ",
  max_tokens=32, # max tokens to generate

  # either change temp or top_p not both
  temperature=0.7, # b/w 0 and 2, 0.7 will make it more random, 0.2 will make it more deterministic
  # 1 is default for top_p
  top_p=1, # to select the top tokens with a probability 1.0
  frequency_penalty=0, # a +ve val decreases model likelihood to repeat stuff
  presence_penalty=0, # a +ve val increases model likelihood to talk about new stuff
)

# the regex looks for the words with uppercase letters
matches = re.findall(r'\b[A-Z]+\b', response.choices[0].text)
print(matches)
