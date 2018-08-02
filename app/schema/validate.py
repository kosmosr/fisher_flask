#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:47
"""
from marshmallow import Schema, fields, validate, validates

from app.const.status import VALIDATE_NICKNAME_ERROR, VALIDATE_PASSWORD_ERROR


class RegisterValSchema(Schema):
    nickname = fields.Str(required=True, validate=validate.Length(min=2, max=10, error=VALIDATE_NICKNAME_ERROR))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR))

    @validates('nickname')
    def validate_nickname(self, value):
        pass

