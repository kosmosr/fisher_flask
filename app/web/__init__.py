#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
from flask import Blueprint
from flask_login import LoginManager

web = Blueprint('web', __name__)
login_manager = LoginManager()

from app.web import auth, book, drift, gift, main, wish
