from backend.news.news import get_all_news, websites_
from queue import Queue
from threading import Thread
from backend.stocks.stocks import get_all_stock
from backend.today.today import get_today
from backend.jokes.get_filter_jokes import get_jokes
from random import randint

# print headlines
ans = get_all_news()
for i in websites_.keys():
    if i in ans.keys():
        print("\n" + i)
        for k, v in ans[i].items():
            print(k)

print("\n\n")

# print stocks
stocks = get_all_stock()
for i in stocks:
    print("\n" + i)
    print(stocks[i]['change'])

print("\n\n")

# print historical occourances
today = get_today()
for i in today:
    print(i)

print("\n")

# print random jokes
jokes = get_jokes()
for i in range(5):
    print(jokes[randint(0, len(jokes))][0].strip())

print("\n")
