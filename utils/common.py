#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 15:57
"""
from datetime import datetime
from config import config

import jwt


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
