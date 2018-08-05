#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/1.0')

from app.web import auth, book, drift, gift, main, wish
