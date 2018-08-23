#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/23 14:37
"""
from functools import wraps

from flask import g

from app.common import const
from app.common.const import NOT_LOGIN, USER_NOT_EXIST
from app.common.response import ErrorResponse
from app.models.user import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uid = getattr(g, const.REQUEST_USER_ID, None)
        if not uid:
            return ErrorResponse(NOT_LOGIN).make()
        user = User.query.filter(User.id == uid, User.is_deleted == False).first()
        if not user:
            return ErrorResponse(USER_NOT_EXIST).make()
        return func(*args, **kwargs)

    return wrapper
