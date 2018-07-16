#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/16 16:36
"""
import redis

from config import config

pool = redis.ConnectionPool.from_url(config.REDIS_URL)

redis = redis.Redis(connection_pool=pool)
