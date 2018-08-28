#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/6 12:01
"""
from flask import request, g

from app.common.const import REQUEST_USER_ID, TOKEN_INVALID, USER_NOT_EXIST, ENDPOINT_NOT_EXIST
from app.common.redis_key import login_token_key, login_url_key
from app.common.response import ErrorResponse, SuccessResponse
from app.log import logger
from config import config
from ext import app
from ext.redis import redis
from utils.common import decode_token, check_token


@app.before_request
def before_request():
    logger.debug("request ip: %s, path: %s, args: %s, body: %s", request.remote_addr, request.path, request.args,
                 request.data.decode('utf-8'))
    if request.method == 'OPTIONS':
        return SuccessResponse()()
    login_urls = set([url.decode('utf-8') for url in redis.smembers(login_url_key)])
    try:
        if request.endpoint.split('.')[-1] in login_urls:
            return check_request_token()
    except AttributeError as err:
        logger.error(err)
        return ErrorResponse(ENDPOINT_NOT_EXIST).make()


def check_user_valid(uid):
    from app.models.user import User
    user = User.query.filter(User.id == uid, User.is_deleted == False).first()
    if not user:
        return False
    return True


def check_request_token():
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
    else:
        return ErrorResponse(TOKEN_INVALID).make()
