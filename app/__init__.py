"""
@File : __init__.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/19
"""
from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或者注册'

    # 注册mail插件
    mail.init_app(app)

    with app.app_context():
        db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
