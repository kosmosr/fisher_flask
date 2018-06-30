#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/29 11:14
"""


class DevelopmentConfig:
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://user:password@host:port/fisher'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    DEBUG = False
    ENV = 'production'
