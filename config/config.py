#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/29 11:14
"""
import os


class DevelopmentConfig:
    HOST = 'localhost'
    PORT = 9527
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Zengminghao_1997@10.10.76.1:13306/fisher'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '97ab1951-3548-4b9a-8f74-5310b552335b'
    TRAP_HTTP_EXCEPTIONS = True

    # EMAIL
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'zmh376170361@vip.qq.com'
    MAIL_PASSWORD = 'zhkytoxtvejfcaji'
    MAIL_DEFAULT_SENDER = 'zmh376170361@vip.qq.com'
    MAIL_SUBJECT_PREFIX = '[FISHER]'

    # REDIS
    REDIS_URL = "redis://10.10.76.1:16379/0"

    # EXPIRES TIME
    RESET_TOKEN_EXPIRE_TIME = 60 * 60 * 3


class ProductionConfig:
    DEBUG = False
    ENV = 'production'
    PORT = os.getenv('port', 8000)
