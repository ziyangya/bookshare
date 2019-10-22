"""
@File : user.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/27
"""
from math import floor

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    # __tablename__ = 'User'， 定义表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    # 定义密码的字段名字
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 属性读取，getter
    @property
    def password(self):
        return self._password

    # 属性写入，setter，进行预处理
    @password.setter
    def password(self, raw):
        # 加密原始密码
        self._password = generate_password_hash(raw)

    # 将明文密码hash并且进行比较
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 是否可以发送Drift,鱼豆够多，每索取两本书，自己得送出一本书
    def can_send_drift(self):
        if self.beans < 1:
            return False
        # 成功送出的书籍数量
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        # 从drift中查询
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    # 保存是否赠送的书籍
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        # 在鱼书的api中查看是否存在此是isbn
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送者和索要者

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()

        # 既不在不在赠送清单，也不在心愿清单才能添加
        if not gifting and not wishing:
            return True
        else:
            return False

    # 生成带用户加密id的token
    def generate_token(self, expiration=600):
        # 可以看做序列化器
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 将用户写入s
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # 如何获取更新密码的用户，通过token的信息拿到用户的id
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        # 过期或者伪造的token
        try:
            # 读取token
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            # 通过用户的id号将用户模型查出来
            user = User.query.get(uid)
            # 修改用户密码，提交到数据库
            user.password = new_password
        return True

    # 有具体的意义，使用频率高，可以定义在模型下面，如果只是适配一个页面的话，定义在viewmodel下更合适
    # 用户的简介
    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + "/" + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
