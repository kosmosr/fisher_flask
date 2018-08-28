#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:47
"""
from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load

from app.common.const import VALIDATE_NICKNAME_ERROR, VALIDATE_PASSWORD_ERROR, VALIDATE_NICKNAME_EXIST, \
    VALIDATE_EMAIL_EXIST, VALIDATE_RESERT_PASSWORD_ERROR
from app.models.user import User


class PaginationValSchema(Schema):
    page = fields.Int(default=1, missing=1)
    per_page = fields.Int(default=10, missing=10)


class BookSearchValSchema(PaginationValSchema):
    keyword = fields.Str(required=True)


class LoginValSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(),
                       error_messages={'required': '请输入邮箱'})
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                          error_messages={'required': '请输入密码'})


class RegisterValSchema(Schema):
    nickname = fields.Str(required=True, validate=validate.Length(min=2, max=10, error=VALIDATE_NICKNAME_ERROR),
                          error_messages={'required': '请输入昵称'})
    email = fields.Str(required=True, validate=validate.Email(), error_messages={'required': '请输入邮箱'})
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                          error_messages={'required': '请输入密码'})

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


class ResetEmailValSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(), error_messages={'required': '请输入邮箱'})


class ForgetPasswordValSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                          error_messages={'required': '请输入密码'})
    password2 = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                           error_messages={'required': '请输入密码'})

    @pre_load
    def pre_load(self, data):
        if data['password2'] != data['password']:
            raise ValidationError(message=VALIDATE_RESERT_PASSWORD_ERROR)


class ChangePasswordValSchema(Schema):
    old_password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                              error_messages={'required': '请输入旧密码'})
    new_password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                              error_messages={'required': '请输入新密码'})
    confirm_password = fields.Str(required=True, validate=validate.Length(min=6, max=32, error=VALIDATE_PASSWORD_ERROR),
                                  error_messages={'required': '请再一次输入新密码'})

    @pre_load
    def pre_load(self, data):
        if data['confirm_password'] != data['new_password']:
            raise ValidationError(message=VALIDATE_RESERT_PASSWORD_ERROR)


class DriftValSchema(Schema):
    recipient_name = fields.Str(required=True,
                                validate=validate.Length(min=2, max=20, error='收件人姓名长度必须在2到20个字符之间'),
                                error_messages={'required': '请输入收件人姓名'})
    mobile = fields.Str(required=True,
                        validate=validate.Regexp('^1[0-9]{10}$', error='请输入正确的手机号'),
                        error_messages={'required': '请输入收件人手机号'})
    message = fields.Str()
    address = fields.Str(required=True,
                         validate=validate.Length(min=10, max=70, error='地址要大于10个字'),
                         error_messages={'required': '请输入收件人地址'})
    gift_id = fields.Int(required=True, error_messages={'required': 'required gift_id'})


class DriftPendingStatusSchema(Schema):
    status = fields.Int(required=True, validate=validate.Range(min=2, max=4),
                        error_messages={'required': 'required status'})
