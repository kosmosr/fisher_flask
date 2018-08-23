# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/7/16 21:10
"""
from app.common.httpcode import ErrorCode, BadRequest, InternalServerError, NotFound, Unauthorized

REQUEST_USER_ID = 'uid'

# validate
VALIDATE_NICKNAME_EXIST = '昵称已重复'
VALIDATE_EMAIL_EXIST = '昵称已重复'
VALIDATE_NICKNAME_ERROR = '昵称至少需要两个字符，最多10个字符'
VALIDATE_PASSWORD_ERROR = '密码不可以为空或者至少需要6个字符'

# 400
VALIDATE_ERROR = ErrorCode(BadRequest.http_code, '01', '校验错误')
USER_PASSWORD_ERROR = ErrorCode(BadRequest.http_code, '02', '密码错误')

# 401
NOT_LOGIN = ErrorCode(Unauthorized.http_code, '01', '当前未登录')
TOKEN_INVALID = ErrorCode(Unauthorized.http_code, '02', 'TOKEN失效')

# 404
USER_NOT_EXIST = ErrorCode(NotFound.http_code, '01', '用户不存在或者被禁用')

# server
ServerError = ErrorCode(InternalServerError.http_code, '01', '内部错误')
