#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/3 17:09
"""


class HttpCode:
    def __init__(self, code: int):
        self.http_code = code


class ErrorCode(HttpCode):
    def __init__(self, http, code: str = None, message: str = None):
        super(ErrorCode, self).__init__(http)
        self.code = code
        self.message = message


OK = HttpCode(200)

# 当服务器创建数据成功时，应该 返回此状态码。常见的应用场景是使用 POST 提交用户信息，如：
# 添加了新用户
# 上传了图片
# 创建了新活动
CREATED = HttpCode(201)

# 该状态码表示服务器已经接受到了来自客户端的请求，但还未开始处理。常用短信发送、邮件通知、模板消息推送等这类很耗时需要队列支持的场景中
Accepted = HttpCode(202)

# 该状态码表示响应实体不包含任何数据，其中：
# 在使用 DELETE 方法删除资源 成功 时，必须 返回该状态码
# 使用 PUT、PATCH 方法更新数据 成功 时，也 应该 返回此状态码
NotContent = HttpCode(204)

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
