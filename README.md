# Algorithmic Trading using GPT and Alpaca

## Stock trading bot built on [Inverse Cramer Strategy](https://cleverandsmart22.medium.com/the-inverse-jim-cramer-strategy-a412235a45fe)

### How does it work?

- Get last 50 tweets from jim cramer's Twitter handle
- Feed it to a GPT model and ask for stock tickers to sell
- Buy the first stock with 90% of your buying power through Alpaca

### How to use this bot?

Setup a cron job to run ```trading.py```
```
crontab -e
```
the below command ensures the code runs at 9 AM from M-F (remember to change the time incase your machine is not in EST)
```
0 9 * * 1-5 python3 trading.py
```

### stuff to do

- [ ] the twitter endpoint doesn't work anymore, switch to scraping
- [ ] send the log messages to a discord server as well.

## helpful tips
- you can modify the logging in `trading.py` to be a `QueueHandler` and create a thread worker to capture those
- which later on can be captured by the discord bot in `bot.py` to send the messages to your channel.

## Helpful resources
- [fireship algo trading YT video](https://www.youtube.com/watch?v=BrcugNqRwUs)
- [machine learning stock prediction](https://www.youtube.com/watch?v=1O_BenficgE) 





