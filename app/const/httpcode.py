#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/3 17:09
"""
import json

from flask import current_app


class HttpCode:
    def __init__(self, code):
        self.code = code


class SuccessResponse:
    def __init__(self, data):
        self.code = OK.code
        self.data = data

    def build(self):
        return current_app.response_class(
            (json.dumps(self.data, ensure_ascii=False)),
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )


OK = HttpCode(200)
# 客户端错误 4xx
# 请求语法格式错误、无效的请求、无效的签名
BadRequest = HttpCode(400)

# 表示当前请求需要身份认证
# 未认证用户访问需要认证的 API
# access_token 无效/过期
Unauthorized = HttpCode(401)

# 当前请求需要没有权限访问
Forbidden = HttpCode(403)

# 表示用户请求的资源不存在
# 获取不存在的用户信息
# 访问不存在的地址
NotFound = HttpCode(404)

# 请求方法错误
MethodNotAllowd = HttpCode(405)

# 服务器错误 5xx
# 服务器出错时
InternalServerError = HttpCode(500)

# 服务暂不可用
ServiceUnavailable = HttpCode(503)
