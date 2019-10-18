from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app import db
from app.forms.drift import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from view_models.book import BookViewModel
from view_models.drift import DriftCollection
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    # 取当前交易的礼物id号
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的&_&，不能向自己所要书籍哦！')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    # post请求并且通过表单校验
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        # 发送请求短信
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                  wisher=current_user,
                  gift=current_gift)
        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter,
                           user_beans=current_user.beans, form=form)


# 鱼书漂流
@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)
    ).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


# 拒绝鱼书
@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        # 修改状态
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


# 撤销鱼书
@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 超权现象,多一步验证，
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id,
                                      id=did).first_or_404()
        # 不能将一个枚举类型赋值
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


# 成功邮寄
@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        # 当鱼书交易成功，需要修改gift表中对应书籍的状态，礼物赠送
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 加入心愿，有人赠送，发送Drift，鱼书结束，心愿达成
        wish = Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                                    launched=False).first()
        wish.launched = True
        # Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
        #                      launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


# 将相关的信息装载到drift模型中去
# 参数为form和当前对应的礼物
def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        # 将目标对象传入实现相关字段的复制
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        # 获取书籍的模型当日发，book是一个字典,BookViewModel是个对象，以点的方式取
        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
