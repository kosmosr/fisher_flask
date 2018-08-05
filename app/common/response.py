# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/8/5 20:20
"""
import string

from flask import make_response, jsonify

from app.common.httpcode import HttpCode


class SuccessResponse:
    def __init__(self, http_code: HttpCode, data='', pagination=False):
        self.code = http_code.code
        self.data = data
        self.pagination = pagination

    def make(self):
        if not self.pagination:
            return make_response(jsonify(self.data), self.code)
        else:
            dict = {
                'data': self.data,
                'meta': {'pagination': self.data}
            }
            return make_response(jsonify(dict), self.code)


class ErrorResponse:
    def __init__(self, http_code: int, msg: string, code=None):
        self.http_code = http_code
        self.code = code
        self.message = msg

    def make(self):
        dict = {
            'error_code': str(self.http_code) + str(self.code) if self.code is not None else self.http_code,
            'message': self.message
        }
        return make_response(jsonify(dict), self.http_code)
