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


class ProductionConfig:
    DEBUG = False
    ENV = 'production'
