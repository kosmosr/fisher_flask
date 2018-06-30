#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:17
"""

from app import create_app
from config import dev

app = create_app()

if __name__ == "__main__":
    app.run(host=dev.host, port=dev.port)
