import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

#websites and URLs
websites_ = {
    "BuzzFeed": ["https://www.buzzfeed.com/trending", ["featured-card__headline link-gray", "js-card__link link-gray"]],
    "CNN": ["https://www.cnn.com/specials/last-50-stories", ["cd__headline-text"]],
    "New York Times": ["https://www.nytimes.com/", ["css-1cmu9py esl82me0", "balancedHeadline"]],
    "Huffington Post": ["https://www.huffpost.com/news/topic/trending-topics", ["card__headline card__headline--long"]],
    "NBC News": ["https://www.nbcnews.com/latest-stories", ["headline___38PFH"]],
    "Washington Post": ["https://www.washingtonpost.com/", []],
    "Wall Street Journal": ["https://www.wsj.com/", []],
    "The Atlantic": ["https://www.theatlantic.com/most-popular/", ["hed"]],
    "ABC News": ["https://abcnews.go.com/", []],
    "The Onion": ["https://www.theonion.com/", ["sc-1qoge05-0 eoIfRA"]],
    "Fox News": ["https://www.foxnews.com/", ["title title-color-default"]],
    "BBC News": ["https://www.bbc.com/news", ["gs-c-promo-heading__title gel-paragon-bold nw-o-link-split__text", "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"]],
    "POLITICO": ["https://www.politico.com/", ["js-tealium-tracking"]],
    "NPR News": ["https://www.npr.org/", ["title"]],
    "Reuters": ["https://www.reuters.com/", ["story-title"]],
    "Associated Press": ["https://apnews.com/", []],
    "CBS News": ["https://www.cbsnews.com/", ["item__hed"]]
}


# Get top from one site
def get_top(site, websites, n=10):
    top = {}
    # Get request
    s = requests.get(websites[site][0], headers={
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


def get_all_news(websites=websites_, n=5):
    ans = {}
    # how many threads
    cc = len(websites.keys())
    # get from one website

    def one():
        i = q.get()
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
