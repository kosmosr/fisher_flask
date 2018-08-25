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
VALIDATE_RESERT_PASSWORD_ERROR = '输入密码不一样，请重新输入'

# 400
VALIDATE_ERROR = ErrorCode(BadRequest.http_code, '01', '校验错误')
USER_PASSWORD_ERROR = ErrorCode(BadRequest.http_code, '02', '密码错误')
SAVE_BOOK_ERROR = ErrorCode(BadRequest.http_code, '03', '这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')
USER_RAWPASSWORD_ERROR = ErrorCode(BadRequest.http_code, '04', '原密码错误，请重试')
SAVE_WISH_ERROR = ErrorCode(BadRequest.http_code, '05', '这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')

# 401
NOT_LOGIN = ErrorCode(Unauthorized.http_code, '01', '当前未登录')
TOKEN_INVALID = ErrorCode(Unauthorized.http_code, '02', 'TOKEN失效')

# 404
USER_NOT_EXIST = ErrorCode(NotFound.http_code, '01', '用户不存在或者被禁用')

# server
ServerError = ErrorCode(InternalServerError.http_code, '01', '内部错误')
