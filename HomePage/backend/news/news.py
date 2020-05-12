from requests import get
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from datetime import datetime

#websites and URLs

# Get top from one site

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}


def get_top(site, websites, n=10):
    top = {}
    # Get request
    s = get(websites[site][0], headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
    soup = BeautifulSoup(s.content, features="html.parser")
    # parse soup based on site
    if site == "BuzzFeed" or site == "Huffington Post":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}, href=True):
                top[j.get_text()] = j['href']
    elif site == "CNN":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text()] = "https://cnn.com" + \
                    j.find_parent(href=True)['href']
    elif site == "BBC News":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text()] = "https://www.bbc.com" + \
                    j.find_parent(href=True)['href']
    elif site == "New York Times":
        for j in soup.find_all("span", attrs={"class": None}):
            if j.find_parent(href=True) and "nytimes.com" not in j.find_parent(href=True)['href']:
                top[j.get_text()] = "https://www.nytimes.com" + \
                    j.find_parent(href=True)['href']
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            if j.find_parent(href=True) and "nytimes.com" not in j.find_parent(href=True)['href']:
                top[j.get_text()] = "https://www.nytimes.com" + \
                    j.find_parent(href=True)['href']
    elif site == "NBC News" or site == "NPR News":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                if j.find_parent(href=True):
                    top[j.get_text()] = j.find_parent(href=True)['href']
    elif site == "Washington Post":
        for j in soup.find_all(attrs={"data-pb-placeholder": "Write headline here"}, href=True):
            top[j.get_text().strip()] = j['href']
    elif site == "Wall Street Journal":
        for i in soup.find_all("a", href=True):
            if "articles" in i['href'].split("/") and len(i.get_text().split(" ")) > 4:
                top[i.get_text()] = i['href']
    elif site == "The Atlantic":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text().strip()] = "https://www.theatlantic.com" + \
                    j.find_parent(href=True)['href']
    elif site == "ABC News":
        for j in soup.find_all(attrs={"data-analytics": "cid=clicksource_4380645_3_mobile_web_only_headlines_headlines_hed"}, href=True):
            top[j.get_text()] = j['href']
    elif site == "The Onion":
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            top[j.get_text()] = j.find_parent(href=True)['href']
    elif site == "Fox News" or site == 'Reuters':
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            if j.find(href=True):
                top[j.get_text()] = j.find(href=True)['href']
    elif site == "POLITICO":
        for j in soup.find_all(attrs={"class": websites[site][1][0]}, href=True):
            if len(j.get_text().split(" ")) > 3:
                top[j.get_text()] = j['href']
    elif site == "Associated Press":
        for j in soup.find_all("a", attrs={"data-key": "related-story-link"}, href=True):
            top[j.get_text().split("By")[0]] = "https://apnews.com" + j['href']
    elif site == "CBS News":
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            if j.find_parent(href=True):
                if len(j.get_text().strip().split(" ")) > 3:
                    top[j.get_text()] = j.find_parent(href=True)['href']
    ans = {}
    # get top n results
    k = list(top.keys())
    for i in range(n):
        if i < len(k):
            ans[k[i].strip()] = top[k[i]]
    # return results
    print(site)
    return ans


def getTop100():
    bs = BeautifulSoup(get("https://www.billboard.com/charts/hot-100").content,
                       features="html.parser")
    print("gottem")
    ans = []
    cur = "1"
    for i in bs.find_all(attrs={"class": "chart-element__information"}):
        tx = [h for h in i.get_text().strip().split("\n") if h]
        ans.append(cur + " - " + tx[0] + " - " + tx[1])
        cur = str(int(cur)+1)
    return ans


def get_today():
    map_ = {"01": "January", "02": "February", "03": "March",
            "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
    today_ = str(datetime.today()).split(" ")[0].split("-")

    # URL
    URL = "https://www.historynet.com/today-in-history/" + \
        map_[today_[1]] + "-" + today_[2]
    ans = []
    # get website
    p = get(URL, headers=headers)
    # parse for dates
    soup = BeautifulSoup(p.content, "html.parser")
    for i in soup.find_all(attrs={"class": "war-event"}):
        s = i.get_text().strip().split("\n\n")
        ans.append(s[0].strip() + ": " + s[1].strip())
    return ans


def get_all_news(websites, n=5):
    ans = {}
    # how many threads
    cc = len(websites.keys())
    # get from one website

    def one():
        i = q.get()
        if i == "Billboard":
            print("starting music")
            ans[i] = getTop100()
            print("done music")
        elif i == "Today":
            print("starting today")
            ans[i] = get_today()
            print("done today")
        else:
            try:
                ans[i] = get_top(i, websites, n)
            except:
                pass
        q.task_done()
    # queue of sites
    q = Queue(cc)
    for i in range(cc):
        t = Thread(target=one)
        t.daemon = True
        t.start()

    for i in websites.keys():
        q.put(i)
    q.join()

    return ans
