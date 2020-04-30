import yfinance as yf
import datetime
from queue import Queue
from threading import Thread
import datetime
import requests
from bs4 import BeautifulSoup as BS

# Map to months
map_ = {"01": "January", "02": "February", "03": "March",
        "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
today_ = str(datetime.datetime.today()).split(" ")[0].split("-")

# URL
URL = "https://www.historynet.com/today-in-history/" + \
    map_[today_[1]] + "-" + today_[2]

# headers for request
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}


def get_today():
    ans = []
    # get website
    p = requests.get(URL, headers=headers)
    # parse for dates
    soup = BS(p.content, "html.parser")
    for i in soup.find_all(attrs={"class": "war-event"}):
        s = i.get_text().strip().split("\n\n")
        ans.append(s[0].strip() + ": " + s[1].strip())
    return ans
