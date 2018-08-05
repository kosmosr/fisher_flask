#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import Flask

from app.interceptor.error import default_handler
from app.models.book import Book
from config import config
from ext import login_manager, mail
from ext.db import db


def create_app(app: Flask):
    app.config.from_object(config)
    # app.register_error_handler(Exception, default_handler)
    register_blueprint(app)

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    return app


def register_blueprint(app: Flask):
    from .web import api_v1
    app.register_blueprint(api_v1)
