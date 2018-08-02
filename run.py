#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:17
"""
from app import create_app
from config import config
from ext import app

server = create_app(app=app)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)
