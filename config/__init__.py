#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 14:59
"""
prod = False

if prod:
    from .config import ProductionConfig

    config = ProductionConfig
else:
    from .config import DevelopmentConfig

    config = DevelopmentConfig
