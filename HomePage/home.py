from flask import Blueprint, render_template
from HomePage.backend.jokes.get_filter_jokes import get_jokes
from HomePage.backend.news.news import get_all_news
from HomePage.backend.stocks.stocks import get_all_stock
from HomePage.backend.today.today import get_today
from random import randint, shuffle
from os import fork


bp = Blueprint('home', __name__)

websites = {
    "Billboard": ["https://www.billboard.com/charts/hot-100"],
    "CNN": ["https://www.cnn.com/specials/last-50-stories", ["cd__headline-text"]],
    "Washington Post": ["https://www.washingtonpost.com/", []],
    "Wall Street Journal": ["https://www.wsj.com/", []],
    "The Atlantic": ["https://www.theatlantic.com/most-popular/", ["hed"]]
}


def getWebsites():
    news = get_all_news(websites, 15)
    music = news["Billboard"]
    del news["Billboard"]
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
    return (all_news, music)


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
    x = fork()
    global st
    global all_news
    global music
    if x:
        st = getStock()
    else:
        all_news, music = getWebsites()
    jokes = getJokes()
    try:
        return render_template('index.html', news=all_news, jokes=jokes, today=get_today(), stocks=st, music=music)
    except:
        all_news, music = getWebsites()
        return render_template('index.html', news=all_news, jokes=jokes, today=get_today(), stocks=getStock(), music=music)
