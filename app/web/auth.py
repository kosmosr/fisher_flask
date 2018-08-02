from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app import db
from app.const.redis_key import reset_password_token_key
from app.const.status import TOKEN_INVALID
from app.forms.auth import RegisterForm, LoginForm, BaseForm, ResetPasswordForm
from app.models.user import User
from config import config
from ext.redis import redis
from utils.common import encode_token, decode_token, check_token
from utils.email import send_email
from . import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    args = request.get_json()
    if request.method == 'POST':
        with db.auto_commit():
            user = User()
            # user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html')


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
                token = encode_token(user.id)
                redis_key = reset_password_token_key.format(user.id)
                redis.setex(redis_key, token, time=config.RESET_TOKEN_EXPIRE_TIME)
                send_email(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=token)
                flash('一封邮件已发送到邮件' + email + ', 请及时查收')
                return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        payload = decode_token(token)
        # 验证token一致性
        redis_key = reset_password_token_key.format(payload['uid'])
        token_from_redis = redis.get(redis_key)
        if check_token(token, token_from_redis, payload):
            User.reset_password(payload['uid'], form.password1.data)
            return redirect(url_for('web.index'))
        else:
            flash(TOKEN_INVALID)
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
