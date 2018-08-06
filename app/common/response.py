# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/8/5 20:20
"""

from flask import make_response, jsonify

from app.common.httpcode import HttpCode, ErrorCode


class SuccessResponse:
    def __init__(self, http_code: HttpCode, data='', pagination=None, other=None):
        self.code = http_code.http_code
        self.data = data
        self.pagination = pagination
        self.other = other

    def make(self):
        if not self.pagination:
            return make_response(jsonify(self.data), self.code)
        else:
            dict = {
                'data': self.data,
                'meta': {'pagination': self.pagination}
            }
            if self.other:
                dict['meta'].update(self.other)
            return make_response(jsonify(dict), self.code)


class ErrorResponse:
    def __init__(self, error_code: ErrorCode):
        self.http_code = error_code.http_code
        self.code = error_code.code
        self.message = error_code.message

    def make(self):
        dict = {
            'error_code': str(self.http_code) + str(self.code) if self.code is not None else self.http_code,
            'message': self.message
        }
        return make_response(jsonify(dict), self.http_code)
