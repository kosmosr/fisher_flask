#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/16 16:33
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'web.login'
login_manager.login_message = '请登录查看'
