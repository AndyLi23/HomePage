from flask import Blueprint, render_template
from HomePage.backend.jokes.get_filter_jokes import get_jokes
from HomePage.backend.news.news import get_all_news, websites_
from HomePage.backend.stocks.stocks import get_all_stock
from HomePage.backend.today.today import get_today
from random import randint

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    websites = {
        "CNN": ["https://www.cnn.com/specials/last-50-stories", ["cd__headline-text"]],
        "New York Times": ["https://www.nytimes.com/", ["css-1cmu9py esl82me0", "balancedHeadline"]],
        "Washington Post": ["https://www.washingtonpost.com/", []],
        "Wall Street Journal": ["https://www.wsj.com/", []],
        "The Atlantic": ["https://www.theatlantic.com/most-popular/", ["hed"]],
    }
    news = get_all_news(websites, 10)
    all_news = []
    for i in websites.keys():
        if i in news.keys():
            l = list(zip(news[i].keys(), news[i].values()))
            temp = set()
            for i in range(5):
                while True:
                    j = l[randint(0, len(l)-1)]
                    if j not in temp:
                        temp.add(j)
                        break
                    else:
                        pass
            all_news.extend(temp)
    s = get_all_stock()
    for k, v in s.items():
        v['price'] = k + " " + v['price'] + \
            "." * (15-len(k + " " + v['price']))
    return render_template('index.html', news=all_news, jokes=get_jokes(), today=get_today(), stocks=s)
