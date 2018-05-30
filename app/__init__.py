#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import Flask

from config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    return app


def register_blueprint(app: Flask):
    from .web import v1
    app.register_blueprint(v1)
