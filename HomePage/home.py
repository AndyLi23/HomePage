from flask import Blueprint, render_template
from backend.jokes.get_filter_jokes import get_jokes
from backend.news.news import get_all_news, websites_
from backend.stocks.stocks import get_all_stock
from backend.today.today import get_today

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('index.html', sites=websites_, news=get_all_news(), jokes=get_jokes(), today=get_today(), stocks=get_all_stock())
