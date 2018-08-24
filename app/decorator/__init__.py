#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/23 14:37
"""
from functools import wraps

from app.common.redis_key import login_url_key
from ext.redis import redis


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        redis.delete(login_url_key)
        redis.sadd(login_url_key, func.__name__)
        return func

    return wrapper()
