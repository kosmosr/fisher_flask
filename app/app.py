#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/29 10:48
"""
from flask import Flask

from config import dev

app = Flask(__name__)
app.config.from_object(dev)
