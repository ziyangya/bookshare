"""
@File : config.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/18
"""
DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:eternal@127.0.0.1:3306/fisher"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '\xd6\x1d\xce{\xf2Q\xed\xf7\x12\xf3\x104\x05}<\x83\xc3\xe6#\x1d\x14\xddC\xdc'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = True
MAIL_USERNAME = '1637699498@qq.com'
MAIL_PASSWORD = 'yabviphnosgtcddi'
