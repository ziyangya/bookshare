from flask import render_template, request, redirect, url_for, flash

from app.libs.email import send_mail
from . import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from app.models.base import db
from flask_login import login_user, logout_user

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    # 验证form，当为post时
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # user.nickname = form.nickname.data
        # form.data包含了客户端提交过来的所有参数
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将账号密码写入到 cookies 中
            login_user(user, remember=True)
            # next 查询参数，记录跳转回去页面的地址
            next = request.args.get('next')
            #  防止重定向攻击
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # first_or_404
            # callable可调用对象，简化对象下方法的调用。模糊了对象和函数的的区别，统一调用接口
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, '重置你的密码',
                      'email/reset_password.html', user=user, token=user.generate_token())
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已经更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    # 清空浏览器的cookies
    logout_user()
    return redirect(url_for('web.index'))
