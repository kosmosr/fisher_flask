#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import Flask

from app.models import db
from app.models.book import Book
from app.web import login_manager
from config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请登录查看'
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app: Flask):
    from .web import web
    app.register_blueprint(web)
