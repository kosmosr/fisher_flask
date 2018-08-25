#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/23 14:37
"""
from functools import wraps

from flask import request, g

from app.common.const import USER_NOT_EXIST, REQUEST_USER_ID, TOKEN_INVALID
from app.common.redis_key import login_url_key, login_token_key
from app.common.response import ErrorResponse
from app.interceptor.before_request import check_user_valid
from config import config
from ext.redis import redis
from utils.common import decode_token, check_token

redis.delete(login_url_key)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        redis.sadd(login_url_key, func.__name__)
        return func

    return wrapper()


def can_login_url(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token', None)
        if token:
            payload = decode_token(token)
            uid = payload['uid']
            key = login_token_key.format(uid)
            token_from_redis = redis.get(key)
            if check_token(token, token_from_redis):
                if not check_user_valid(uid):
                    return ErrorResponse(USER_NOT_EXIST).make()
                redis.setex(key, token, time=config.LOGIN_TOKEN_EXPIRE_TIME)
                setattr(g, REQUEST_USER_ID, uid)
            else:
                return ErrorResponse(TOKEN_INVALID).make()
        return func(*args, **kwargs)

    return wrapper
