from flask import current_app, flash, redirect, url_for, render_template

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.base import db
from view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user
# from view_models.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    # 对于每一个礼物中的书籍，需要显示出想要人的数量
    # 1.根据每个礼物isbn去Wish表里查询与此书相关的人（需要循环遍历数据库）
    # 2.循环遍历礼物，取出isbn组成一个列表，使用in查询Wish中isbn列表中的心愿，计算数量（两次查询）
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # can_save_to_list函数放在user模型中，看作用户的行为，复用性更强
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已经存在你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂中完成此交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
        return redirect(url_for('web.my_gifts'))