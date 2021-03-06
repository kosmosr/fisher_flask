#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 15:57
"""
import hashlib
from datetime import datetime

import jwt

from config import config
from ext.redis import redis


def is_isbn_or_key(keyword: str):
    """
    判断关键字
    :param keyword: 关键字 isbn
    :return: True 关键字, False ISBN
    """
    if len(keyword) == 13 and keyword.isdigit():
        return False
    short_q = keyword.replace('-', '')
    if '-' in keyword and len(short_q) == 10 and short_q.isdigit():
        return False
    return True


def encode_token(uid):
    payload = {
        'uid': uid,
        'timestamp': datetime.now().timestamp()
    }
    token = jwt.encode(payload, key=config.SECRET_KEY).decode()
    return token


def decode_token(token):
    payload = jwt.decode(token, key=config.SECRET_KEY)
    return payload


def generate_token(uid, key: str, expire_time: int):
    token = encode_token(uid)
    redis_key = key.format(uid)
    redis.setex(redis_key, token, time=expire_time)
    return token


def check_token(token, token_from_redis):
    """
    检验token有效性
    :param token:
    :param token_from_redis:
    :return:
    """
    if token_from_redis and token_from_redis.decode() == token:
        return True
    else:
        return False


def md5_n(data: str, n: int = 1) -> str:
    if n == 0:
        return data
    else:
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5_n(md5.hexdigest(), n - 1)


def bytes_to_dict(data: bytes) -> dict:
    return eval(str(data, encoding='utf-8'))
