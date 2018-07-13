#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/29 11:14
"""


class DevelopmentConfig:
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:Zengminghao_1997@www.mollysu.top:3306/fisher'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '97ab1951-3548-4b9a-8f74-5310b552335b'

    # EMAIL
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'zmh376170361@vip.qq.com'
    MAIL_PASSWORD = 'zhkytoxtvejfcaji'
    MAIL_DEFAULT_SENDER = 'zmh376170361@vip.qq.com'
    MAIL_SUBJECT_PREFIX = '[FISHER]'

    # REDIS
    REDIS_URL = "redis://www.mollysu.top:6379/0"


class ProductionConfig:
    DEBUG = False
    ENV = 'production'
