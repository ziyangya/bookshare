# """
# @File : test.py
# @Author: Zyeoh
# @Desc :
# @Date : 2019/9/29
# """
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+cymysql://root:eternal@127.0.0.1:3306/fisher"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy(app)
#
#
# class Book(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(50), nullable=False)
#     author = Column(String(50), default='未名')
#     binding = Column(String(20))
#     publisher = Column(String(50))
#     price = Column(String(20))
#     page = Column(Integer)
#     pubdate = Column(String(20))
#     isbn = Column(String(15), nullable=False, unique=True)
#     summary = Column(String(1000))
#     image = Column(String(50))
#
#
# if __name__ == '__main__':
#     db.create_all()
