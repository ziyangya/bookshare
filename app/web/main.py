from flask import render_template

from app.models import gift
from app.models.gift import Gift
from view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    # 通过礼物将书籍的数据显示出来
    recent_gifts = Gift.recent()
    # 获取最近上传图书，通过把gift转换为BookViewModel，需要拿到book的数据，（gift下book方法）
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
