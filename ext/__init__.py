#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/16 16:33
"""
import os

from flask import Flask
from flask_mail import Mail

from config import config

instance_path = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'app')
app = Flask(import_name=instance_path, root_path=instance_path)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail()
