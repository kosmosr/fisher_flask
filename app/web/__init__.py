#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
from flask import Blueprint

v1 = Blueprint('v1', __name__, url_prefix='/v1')

from app.web import book
