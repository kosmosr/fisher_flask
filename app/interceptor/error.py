#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 16:53
"""

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.common.const import VALIDATE_ERROR, ServerError
from app.common.httpcode import ErrorCode
from app.common.response import ErrorResponse
from app.log import logger
from ext import app


@app.errorhandler(HTTPException)
def default_handler(e):
    if isinstance(e, HTTPException):
        logger.error(e)
        return ErrorResponse(ErrorCode(http=e.code, message=e.name)).make()


@app.errorhandler(ValidationError)
def request_error(e):
    logger.error(e)
    return ErrorResponse(VALIDATE_ERROR).make()


@app.errorhandler(Exception)
def default_handler(e):
    logger.exception(e)
    return ErrorResponse(ServerError).make()
