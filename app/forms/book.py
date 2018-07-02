#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/30 16:45
"""
from wtforms import Form, StringField, validators, IntegerField


class BookForm(Form):
    keyword = StringField('keyword', [validators.data_required(), validators.Length(min=1, max=25)])
    page = IntegerField('page', default=1)
