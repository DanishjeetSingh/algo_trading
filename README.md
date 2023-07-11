# Algorithmic Trading using GPT and Alpaca

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


## Helpful resources
- [fireship algo trading YT video](https://www.youtube.com/watch?v=BrcugNqRwUs)
- [machine learning stock prediction](https://www.youtube.com/watch?v=1O_BenficgE) 





