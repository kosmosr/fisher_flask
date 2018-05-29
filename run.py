#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:17
"""

from app.app import app

from config import dev

if __name__ == "__main__":
    app.run(host=dev.host, port=dev.port)
