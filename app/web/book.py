"""
@File : book.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/19
"""
from flask import flash, render_template, request
from flask_login import current_user
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)
        books.fill(yushu_book, q)

        # return json.dumps(books, default=lambda o: o.__dict__)
        # return jsonify(books.__dict__)
    else:
        flash('搜索的关键字不符合要求，重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 是否登录状态
    if current_user.is_authenticated:
        # 是否为赠送者
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        # 是否为索要者
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    # 取所有赠送者的信息和索要者的信息,只是得到query的封装，还有一条触发的语句
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 视图模型的转换
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html', book=book,
                           has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)
