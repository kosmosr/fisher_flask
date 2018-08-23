from flask import render_template, request, redirect, url_for, flash, g

from app import db
from app.common.const import USER_NOT_EXIST, USER_PASSWORD_ERROR, REQUEST_USER_ID, TOKEN_INVALID
from app.common.httpcode import CREATED, OK, NotContent, Unauthorized
from app.common.redis_key import reset_password_token_key, login_token_key
from app.common.response import SuccessResponse, ErrorResponse
from app.forms.auth import BaseForm, ResetPasswordForm
from app.models.user import User
from app.schema.validate import RegisterValSchema, LoginValSchema
from config import config
from ext.redis import redis
from utils.common import decode_token, check_token, generate_token
from utils.email import send_email
from . import api_v1

__author__ = 'kosmosr'


# 注册
@api_v1.route('/users', methods=['POST'])
def register():
    args = request.get_json()
    schema = RegisterValSchema(strict=True).load(args)
    with db.auto_commit():
        user = User()
        user.set_attrs(schema.data)
        db.session.add(user)
    return SuccessResponse(CREATED).make()


# 登录
@api_v1.route('/auth', methods=['POST'])
def login():
    schema = LoginValSchema(strict=True).load(request.get_json())
    data = schema.data
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return ErrorResponse(USER_NOT_EXIST).make()
    if user.check_password(data['password']):
        token = generate_token(user.id, login_token_key, config.LOGIN_TOKEN_EXPIRE_TIME)
        data = {'token': token}
        return SuccessResponse(OK, data=data).make()
    else:
        return ErrorResponse(USER_PASSWORD_ERROR).make()


@api_v1.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = BaseForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).first_or_404()
            if user:
                token = generate_token(user.id, reset_password_token_key, config.RESET_TOKEN_EXPIRE_TIME)
                send_email(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=token)
                flash('一封邮件已发送到邮件' + email + ', 请及时查收')
                return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@api_v1.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        payload = decode_token(token)
        # 验证token一致性
        redis_key = reset_password_token_key.format(payload['uid'])
        token_from_redis = redis.get(redis_key)
        if check_token(token, token_from_redis):
            User.reset_password(payload['uid'], form.password1.data)
            return redirect(url_for('web.index'))
        else:
            return ErrorResponse(TOKEN_INVALID).make()
    return render_template('auth/forget_password.html', form=form)


@api_v1.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


# 注销
@api_v1.route('/users', methods=['DELETE'])
def logout():
    uid = getattr(g, REQUEST_USER_ID, None)
    if uid:
        key = login_token_key.format(uid)
        redis.delete(key)
        return SuccessResponse(NotContent).make()
    else:
        return ErrorResponse(Unauthorized).make()
