import re
from configparser import ConfigParser

from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

@app.get("/twitterdata/")
async def get_twitter_data(username: str, count: int = 100):
    def clean_tweet(text):
        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)

        # Remove mentions and hashtags
        text = re.sub(r"@\w+|#\w+", "", text)

        # Remove special characters and punctuations
        text = re.sub(r"[^\w\s]", "", text)

        # Remove extra whitespaces
        text = re.sub(r"\s+", " ", text)

        # Convert to lowercase
        text = text.lower()
        return text

    twitter_resp = requests.get(
        f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count={count}&include_rts=false",
        headers={
            "Authorization": f"Bearer {bearer_token}",
        },
    )

    tweets = []
    for tweet in twitter_resp.json():
        text_cleaned = clean_tweet(tweet["text"])
        tweets.append( text_cleaned
            # {
            #     "text": text_cleaned,
            #     "lang": tweet["lang"],
            #     "link": f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}",
            # }
        )
    return tweets


if __name__ == "__main__":
    config = ConfigParser(interpolation=None)
    config.read('config.ini')
    bearer_token = config['TWITTER_CREDS']['bearer_token']


    uvicorn.run(app, host="0.0.0.0", port=8000)
