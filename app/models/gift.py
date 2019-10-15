"""
@File : gift.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/27
"""

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook


# 快速定义对象，namedtuple
# EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15))
    launched = Column(Boolean, default=False)

    # 查询所有礼物
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    # 根据传入的一组isbn,到wish表中查询并计算出某个礼物的wish心愿数量
    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 关键字参数和条件表达式的区别
        # 分组，每个isbn对应wish的数量
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    # 属性描述符，将方法转化为属性，gift的特征
    # 通过isbn取数据
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 显示最近礼物   recent_gift = Gift.query.filter_by(launched=False).all()
    # 只显示一定数量（30）
    # 按照时间倒序排列，最新的排在最前面
    # 去重，同一本书籍的礼物不能重复出现，distinct(需要分组group_by),书籍的isbn
    # 对象代表一个礼物，具体
    # 类代表礼物这个事务，它是抽象，不是一个具体的“一个”

    @classmethod
    def recent(cls):
        # 链式调用，主体Query子函数，触发条件。all()
        from flask import current_app
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift