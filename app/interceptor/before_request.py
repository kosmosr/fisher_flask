#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/6 12:01
"""
from flask import request, g

from app.common.const import REQUEST_USER_ID, TOKEN_INVALID
from app.common.httpcode import OK
from app.common.redis_key import login_token_key
from app.common.response import ErrorResponse, SuccessResponse
from app.log import logger
from config import config
from ext import app
from ext.redis import redis
from utils.common import decode_token, check_token


@app.before_request
def before_request():
    logger.debug("request ip: %s, path: %s, args: %s, body: %s", request.remote_addr, request.path, request.args,
                 request.data)
    if request.method == 'OPTIONS':
        return SuccessResponse(OK).make()
    token = request.headers.get('token')
    if token:
        payload = decode_token(token)
        uid = payload['uid']
        key = login_token_key.format(uid)
        token_from_redis = redis.get(key)
        if check_token(token, token_from_redis):
            redis.setex(key, token, time=config.LOGIN_TOKEN_EXPIRE_TIME)
            setattr(g, REQUEST_USER_ID, uid)
        else:
            return ErrorResponse(TOKEN_INVALID).make()
