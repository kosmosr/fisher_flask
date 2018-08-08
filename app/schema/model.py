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
        return data

    @post_load
    def make_entity(self, data):
        return Book(**data)
