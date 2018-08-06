# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/7/16 21:10
"""
from app.common.httpcode import ErrorCode, BadRequest, InternalServerError, NotFound

REQUEST_USER_ID = 'uid'
TOKEN_INVALID = 'TOKEN失效'
# validate
VALIDATE_NICKNAME_EXIST = '昵称已重复'
VALIDATE_EMAIL_EXIST = '昵称已重复'
VALIDATE_NICKNAME_ERROR = '昵称至少需要两个字符，最多10个字符'
VALIDATE_PASSWORD_ERROR = '密码不可以为空或者至少需要6个字符'

# 400
VALIDATE_ERROR = ErrorCode(BadRequest.http_code, code='01', message='校验错误')
USER_PASSWORD_ERROR = ErrorCode(BadRequest.http_code, code='02', message='密码错误')

# 404
USER_NOT_EXIST = ErrorCode(NotFound.http_code, code='01', message='用户不存在')

# server
ServerError = ErrorCode(InternalServerError.http_code, message='内部错误')
