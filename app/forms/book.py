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


class DriftForm(Form):
    recipient_name = StringField(validators=[validators.data_required(),
                                             validators.length(min=2, max=20,
                                                               message='收件人姓名长度必须在2到20个字符之间')])
    mobile = StringField(validators=[validators.data_required(),
                                     validators.regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField()
    address = StringField(validators=[validators.data_required(),
                                      validators.length(min=10, max=70, message='地址要大于10个字')])
