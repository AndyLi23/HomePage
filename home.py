from news import *
from queue import Queue
from threading import Thread
from stocks import *
from today import *


ans = get_all_news()
for i in ans.keys():
    print("\n" + i)
    for k, v in ans[i].items():
        print(k)

print("\n\n")

stocks = get_all_stock()
for i in stocks:
    print("\n" + i)
    print(stocks[i]['change'])

print("\n\n")

today = get_today()
for i in today:
    print(i)

print("\n")
