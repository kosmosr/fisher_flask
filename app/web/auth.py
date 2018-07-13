from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app import db, redis
from app.const.redis_key import token_key
from app.forms.auth import RegisterForm, LoginForm, BaseForm, ResetPasswordForm
from app.models.user import User
from utils.common import encode_token
from . import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账户不存在或者密码错误')
    return render_template('auth/login.html', form=form)
    pass


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = BaseForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).first_or_404()
            if user:
                from utils.email import send_email
                token = encode_token(user.id)
                redis_key = token_key.format(user.id)
                redis.set(redis_key, token)
                send_email(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=token)
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
