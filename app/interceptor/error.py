#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:53
"""
from marshmallow import ValidationError

from ext import app


@app.errorhandler(ValidationError)
def request_error(e):
    pass
