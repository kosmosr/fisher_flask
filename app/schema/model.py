#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/6 15:57
"""
from datetime import datetime

from marshmallow import Schema, fields, pre_load, post_load, post_dump

from app import Book


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    binding = fields.Str()
    publisher = fields.Str()
    pages = fields.Int()
    price = fields.Decimal(places=2, default=0, as_string=True)
    pubdate = fields.Date()
    isbn = fields.Str()
    summary = fields.Str()
    image = fields.Str()

    @pre_load
    def fill_data(self, data):
        for k, v in data.items():
            if data[k] is None:
                keys = self.fields.keys()
                if k in keys:
                    if hasattr(self.fields[k], 'num_type'):
                        types = self.fields[k].num_type
                    else:
                        types = str
                    if not isinstance(data[k], types):
                        if hasattr(self.fields[k], 'num_type'):
                            data[k] = 0
                        else:
                            data[k] = ''
        if not isinstance(data['pages'], int):
            data['pages'] = ''.join(x for x in data['pages'] if ord(x) < 256)
        if not isinstance(data['price'], int):
            data['price'] = data['price'].split('元')[0]
        if isinstance(data['author'], list):
            data['author'] = ','.join(data['author'])
        for x in data['pubdate']:
            if ord(x) > 256:
                raw = ''.join(x for x in data['pubdate'] if ord(x) < 256)
                year = raw[:4]
                month = raw[4:5]
                day = raw[5:6]
                data['pubdate'] = '-'.join([year, month, day])
        return data

    @post_load
    def make_entity(self, data):
        return Book(**data)

    @post_dump
    def fill_pubdate(self, data):
        data['pubdate'] = datetime.strptime(data['pubdate'], '%Y-%m-%d').date().strftime('%Y-%m')
        return data
