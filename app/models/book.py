"""
@File : book.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/20
"""
from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    page = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass
