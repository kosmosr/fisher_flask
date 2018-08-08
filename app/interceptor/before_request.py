#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/6 12:01
"""
from flask import request, g

from app.common.const import REQUEST_USER_ID
from app.log import logger
from ext import app
from utils.common import decode_token


@app.before_request
def before_request():
    logger.debug("request ip: %s, path: %s, args: %s, body: %s", request.remote_addr, request.path, request.args,
                 request.data)
    token = request.headers.get('token')
    if token:
        payload = decode_token(token)
        setattr(g, REQUEST_USER_ID, payload['uid'])
