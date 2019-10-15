"""
@File : base.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/27
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    # SQLAlchemy新增一个方法，commit和 rollback
    @contextmanager
    def auto_commit(self):
        try:
            # yield后直接返回回去，执行核心代码
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 软删除，**kwargs是一个字典
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # 补全基类下filter_by方法
        return super(Query, self).filter_by(**kwargs)


# 重写自己的基类方法实现自己的业务逻辑
# 替换，用自己自定义的Query
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    # 不能create_time中以default = datetime()的形式记录生成时间
    # 类变量和实例变量的区别，类变量的调用时发生在类创建的过程，而实例变量是发生在对象实例化的过程中
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    # 实例化一个模型就记录该模型的生成时间
    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 动态语言
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 判断当前的对象的key是否有跟模型同名的属性
            if hasattr(self, key) and key != id:
                setattr(self, key, value)

    # 将create_time转换为python时间类型
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
