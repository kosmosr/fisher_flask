#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:47
"""
from marshmallow import Schema, fields, validate, validates, ValidationError

from app.common.const import VALIDATE_NICKNAME_ERROR, VALIDATE_PASSWORD_ERROR, VALIDATE_NICKNAME_EXIST, \
    VALIDATE_EMAIL_EXIST
from app.models.user import User


class PaginationValSchema(Schema):
    page = fields.Int(default=1, missing=1)
    per_page = fields.Int(default=10, missing=10)


class BookSearchValSchema(PaginationValSchema):
    keyword = fields.Str(required=True)


class LoginValSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR))


class RegisterValSchema(Schema):
    nickname = fields.Str(required=True, validate=validate.Length(min=2, max=10, error=VALIDATE_NICKNAME_ERROR))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR))

    @validates('nickname')
    def validate_nickname(self, value):
        user = User.query.filter_by(nickname=value).first()
        if user:
            raise ValidationError(message=VALIDATE_NICKNAME_EXIST)

    @validates('email')
    def validate_email(self, value):
        user = User.query.filter_by(email=value).first()
        if user:
            raise ValidationError(message=VALIDATE_EMAIL_EXIST)
