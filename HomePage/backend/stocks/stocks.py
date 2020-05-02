from yfinance import Ticker
from queue import Queue
from threading import Thread
from humanize import intword

stocks_ = ["AAPL", "MSFT", "GOOG", "TSLA",
           "AMZN"]


def getStock(ticker, time):
    # get current prices
    print(ticker)
    c = Ticker(ticker)
    t = c.history(time)
    ans = {}
    # return based on change
    a = t.to_dict()["Open"].keys()
    days = [str(i.to_pydatetime()).split(" ")[0] for i in a]
    try:
        c = c.info
        mc = intword(c['marketCap'], format="%0.3f")
        inf = ticker + ": " + c["longName"] + "!Sector: " + \
            c['sector'] + "!Market Cap: $" + mc
    except:
        inf = ticker[1:] + " Index"
    if t["Close"][-1] > t["Close"][-2]:
        ans["price"] = "{: .2f}".format(t["Close"][-1])
        ans["change"] = "+{:.2f}%  ⬆".format(t["Close"]
                                             [-1] / t["Close"][-2])
        ans["history"] = inf + "|" + str(list(zip(days, t["Close"])))
    else:
        ans["price"] = "{: .2f}".format(t["Close"][-1])
        ans["change"] = "-{:.2f}%  ⬇".format(t["Close"]
                                             [-1] / t["Close"][-2])
        ans["history"] = inf + "|" + str(list(zip(days, t["Close"])))
    print(ticker)
    return ans


def get_all_stock(stocks=stocks_):
    print("starting stocks")
    temp = {}
    cc = len(stocks)

    def one():
        i = q.get()
        temp[i] = getStock(i, "2y")
        q.task_done()
    # queue of sites
    q = Queue(cc)
    for i in range(cc*2):
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
