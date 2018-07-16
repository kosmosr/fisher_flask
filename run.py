#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:17
"""
from app import create_app
from config import config

app = create_app()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
