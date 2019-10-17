"""
@File : __init__.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/19
"""

from flask import Blueprint, render_template

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
# AOP 思想，将处理代码集中在一方法，装饰器
def not_found(e):
    return render_template('404.html'), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import wish
from app.web import gift
from app.web import main
