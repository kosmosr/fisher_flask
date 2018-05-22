#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:17
"""

from flask import Flask

from config import dev

app = Flask(__name__)
app.config.from_object(dev)


@app.route('/')
def index():
    return 'hello'


if __name__ == "__main__":
    app.run(host=dev.host, port=dev.port)
