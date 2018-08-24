#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/24 15:46
"""
from ext import app


@app.before_first_request
def before_first_request():
    pass
