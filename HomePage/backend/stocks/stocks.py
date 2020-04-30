import yfinance as yf
import datetime
from queue import Queue
from threading import Thread

stocks_ = ["DJI", "AAPL", "MSFT", "GOOG", "TSLA", "AMZN"]


def getStock(ticker, time):
    # get current prices
    t = yf.Ticker(ticker).history(time)
    ans = {}
    # return based on change
    a = t.to_dict()["Open"].keys()
    days = [str(i.to_pydatetime()).split(" ")[0] for i in a]
    if t["Close"][-1] > t["Close"][-2]:
        ans["price"] = "{: .2f}".format(t["Close"][-1])
        ans["change"] = "+{:.2f}%  ⬆".format(t["Close"]
                                             [-1] / t["Close"][-2])
        ans["history"] = ticker + "|" + str(list(zip(days, t["Close"][-5:])))
    else:
        ans["price"] = "{: .2f}".format(t["Close"][-1])
        ans["change"] = "-{:.2f}%  ⬇".format(t["Close"]
                                             [-1] / t["Close"][-2])
        ans["history"] = ticker + "|" + str(list(zip(days, t["Close"][-5:])))
    return ans


def get_all_stock(stocks=stocks_):
    temp = {}
    cc = len(stocks)

    def one():
        i = q.get()
        temp[i] = getStock(i, "7d")
        q.task_done()
    # queue of sites
    q = Queue(cc)
    for i in range(cc):
        t = Thread(target=one)
        t.daemon = True
        t.start()

    for i in stocks:
        q.put(i)
    q.join()

    ans = {}

    for i in stocks:
        ans[i] = temp[i]

    return ans


print(get_all_stock())
