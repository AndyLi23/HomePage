from requests import get
from bs4 import BeautifulSoup as BS
from time import time

t = time()


def getTop100():
    bs = BS(get("https://www.billboard.com/charts/hot-100").content,
            features="html.parser")
    ans = []
    cur = 1
    for i in bs.find_all(attrs={"class": "chart-element__information"}):
        ans.append((cur, i.get_text().strip()))
        cur += 1
    return ans


print(getTop100())
print(time() - t)
