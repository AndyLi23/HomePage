import yfinance as yf
import datetime
from queue import Queue
from threading import Thread

stocks_ = ["AAPL", "MSFT", "GOOG", "TSLA", "AMZN"]


def getStock(ticker, time):
    # get current prices
    t = yf.Ticker(ticker).history(time)
    ans = {}
    # return based on change
    if t["Close"][-1] > t["Close"][-2]:
        ans["change"] = str(t["Close"][-1]) + " ↑"
    else:
        ans["change"] = str(t["Close"][-1]) + " ↑"
    return ans


def get_all_stock(stocks=stocks_):
    ans = {}
    # multithreading
    cc = len(stocks)

    def one():
        i = q.get()
        ans[i] = getStock(i, "5d")
        q.task_done()

    q = Queue(cc)
    for i in range(cc):
        t = Thread(target=one)
        t.daemon = True
        t.start()

    for i in stocks:
        q.put(i)
    q.join()

    return ans
