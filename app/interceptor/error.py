#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:53
"""

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.common.httpcode import InternalServerError, BadRequest
from app.common.response import ErrorResponse
from app.log import logger
from ext import app


@app.errorhandler(HTTPException)
def default_handler(e):
    if isinstance(e, HTTPException):
        logger.error(e)
        return ErrorResponse(e.code, msg=e.name).make()


@app.errorhandler(ValidationError)
def request_error(e):
    logger.error(e)
    return ErrorResponse(BadRequest.code, msg='校验错误', code='01').make()


@app.errorhandler(Exception)
def default_handler(e):
    logger.exception(e)
    return ErrorResponse(InternalServerError.code, msg='内部错误').make()
