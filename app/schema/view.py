#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/22 10:14
"""
from marshmallow import Schema, fields


class TradeSchema(Schema):
    user_name = fields.Str()
    time = fields.Str()
    id = fields.Int()


class TradeModelSchema(Schema):
    total = fields.Int(default=0)
    trades = fields.Nested(TradeSchema, many=True)


class BookDetailViewSchema(Schema):
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
    has_in_gifts = fields.Bool(default=False)
    has_in_wishes = fields.Bool(default=False)
    wishes = fields.Nested(TradeModelSchema)
    gifts = fields.Nested(TradeModelSchema)
