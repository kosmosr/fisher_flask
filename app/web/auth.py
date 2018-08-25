from flask import request, g

from app import db
from app.common.const import USER_NOT_EXIST, USER_PASSWORD_ERROR, REQUEST_USER_ID, TOKEN_INVALID, NOT_LOGIN, \
    USER_RAWPASSWORD_ERROR
from app.common.httpcode import CREATED, OK, NotContent, Accepted
from app.common.redis_key import reset_password_token_key, login_token_key
from app.common.response import SuccessResponse, ErrorResponse
from app.decorator import login_required
from app.models.user import User
from app.schema.validate import RegisterValSchema, LoginValSchema, ResetEmailValSchema, ForgetPasswordValSchema, \
    ChangePasswordValSchema
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
        data = {'token': token, 'nickname': user.nickname}
        return SuccessResponse(OK, data=data).make()
    else:
        return ErrorResponse(USER_PASSWORD_ERROR).make()


# 发送重置密码邮件
@api_v1.route('/reset/email', methods=['POST'])
def forget_password_request():
    schema = ResetEmailValSchema(strict=True)
    email = schema.load(request.get_json()).data['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return ErrorResponse(USER_NOT_EXIST).make()
    token = generate_token(user.id, reset_password_token_key, config.RESET_TOKEN_EXPIRE_TIME)
    forget_url = config.FRONT_RESET_EMAIL_URL
    send_email(email, '重置你的密码', 'email/reset_password.html', user=user, token=token, forget_url=forget_url)
    return SuccessResponse(Accepted).make()


# 重置密码
@api_v1.route('/reset/password/<token>', methods=['PATCH'])
def forget_password(token):
    schema = ForgetPasswordValSchema(strict=True)
    password = schema.load(request.get_json()).data['password']
    payload = decode_token(token)
    # 验证token一致性
    redis_key = reset_password_token_key.format(payload['uid'])
    token_from_redis = redis.get(redis_key)
    if check_token(token, token_from_redis):
        User.reset_password(payload['uid'], password)
        redis.delete(redis_key)
        return SuccessResponse(NotContent).make()
    else:
        return ErrorResponse(TOKEN_INVALID).make()


# 登录态重置密码
@login_required
@api_v1.route('/change/password', methods=['PATCH'])
def change_password():
    uid = getattr(g, REQUEST_USER_ID, None)
    if uid:
        schema = ChangePasswordValSchema(strict=True)
        data = schema.load(request.get_json()).data
        old_password = data['old_password']
        new_password = data['new_password']
        user = User.query.filter_by(id=uid).first()
        if not user:
            return ErrorResponse(USER_NOT_EXIST).make()
        if not user.check_password(old_password):
            return ErrorResponse(USER_RAWPASSWORD_ERROR).make()
        User.reset_password(user.id, new_password)
        return SuccessResponse(NotContent).make()
    else:
        return ErrorResponse(NOT_LOGIN).make()


# 注销
@login_required
@api_v1.route('/users', methods=['DELETE'])
def logout():
    uid = getattr(g, REQUEST_USER_ID, None)
    if uid:
        key = login_token_key.format(uid)
        redis.delete(key)
        return SuccessResponse(NotContent).make()
    else:
        return ErrorResponse(NOT_LOGIN).make()
