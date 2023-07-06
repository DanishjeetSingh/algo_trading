"""
Purpose:
    This script will be used to get tweets of jimcramer and send it to the
    gpt api to get stock tickers to sell.
"""
import re
from configparser import ConfigParser
import openai
import requests


def clean_tweet(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    return text


def get_tweets(bearer_token, username='jimcramer'):
    count = 50

    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count={count}&include_rts=false"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }
    response = requests.get(url, headers=headers)
    tweets = response.json()

    tweet_texts = [clean_tweet(tweet["text"]) for tweet in tweets] if tweets.get('text') else []

    return tweet_texts


def get_stocks(api_key, bearer_token):
    tweet_texts = get_tweets(bearer_token)
    openai.api_key = api_key

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{tweet_texts} Jim Cramer recommends selling the following stock tickers: ",
        max_tokens=32,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    matches = re.findall(r'\b[A-Z]+\b', response.choices[0].text)

    return matches


if __name__ == "__main__":
    config = ConfigParser(interpolation=None)
    config.read('config.ini')
    twitter_bearer_token = config['TWITTER_CREDS']['bearer_token']

    stock_matches = get_stocks(api_key=config['OPENAI']['api_key'], bearer_token=twitter_bearer_token)
    print(stock_matches)
