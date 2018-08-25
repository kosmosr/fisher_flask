#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/6 15:57
"""

from marshmallow import Schema, fields, post_load, pre_dump

from app import Book


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    binding = fields.Str()
    publisher = fields.Str()
    pages = fields.Str()
    price = fields.Str()
    pubdate = fields.Str()
    isbn = fields.Str()
    summary = fields.Str()
    image = fields.Str()

    @pre_dump
    def fill_data(self, data):
        if isinstance(data['author'], list):
            data['author'] = ','.join(data['author'])
        for k, _ in data.items():
            if data[k] is None:
                data[k] = ''
            if k == 'summary':
                data[k] = data[k].replace('\\n', '<br/>')
        return data

    @post_load
    def make_entity(self, data):
        return Book(**data)


class UserSchema(Schema):
    id = fields.Int()
    # 昵称
    nickname = fields.Str()
    # 电话号码
    phone_number = fields.Str()
    # 邮箱
    email = fields.Str()
    password = fields.Str()
    # 鱼豆
    beans = fields.Str()
    send_counter = fields.Str()
    receive_counter = fields.Str()
    wx_open_id = fields.Str()
    wx_name = fields.Str()
    update_time = fields.Str()
