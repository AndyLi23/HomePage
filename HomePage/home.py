from flask import Blueprint, render_template
from HomePage.backend.jokes.get_filter_jokes import get_jokes
from HomePage.backend.news.news import get_all_news, websites_
from HomePage.backend.stocks.stocks import get_all_stock
from HomePage.backend.today.today import get_today
from random import randint, shuffle
from multiprocessing import Pool

bp = Blueprint('home', __name__)

websites = {
    "CNN": ["https://www.cnn.com/specials/last-50-stories", ["cd__headline-text"]],
    "New York Times": ["https://www.nytimes.com/", ["css-1cmu9py esl82me0", "balancedHeadline"]],
    "Washington Post": ["https://www.washingtonpost.com/", []],
    "Wall Street Journal": ["https://www.wsj.com/", []],
    "The Atlantic": ["https://www.theatlantic.com/most-popular/", ["hed"]],
}


def getWebsites():
    news = get_all_news(websites, 15)
    all_news = []
    for i in websites.keys():
        if i in news.keys():
            l = list(zip(news[i].keys(), news[i].values()))
            temp = set()
            for _ in range(5):
                while True:
                    j = l[randint(0, len(l)-1)]
                    new = (i + ": " + j[0], j[1])
                    if new not in temp:
                        temp.add(new)
                        break
                    else:
                        pass
            all_news.extend(list(temp))
    shuffle(all_news)
    return all_news


def getStock():
    st = get_all_stock()
    for k, v in st.items():
        v['price'] = k + " " + v['price'] + \
            "." * (15-len(k + " " + v['price']))
    return st


def getJokes():
    return get_jokes()


@bp.route('/')
def index():
    pool = Pool(processes=3)

    st = pool.apply_async(getStock)
    all_news = pool.apply_async(getWebsites)
    jokes = pool.apply_async(getJokes)
    pool.close()
    pool.join()

    return render_template('index.html', news=all_news.get(), jokes=jokes.get(), today=get_today(), stocks=st.get())
