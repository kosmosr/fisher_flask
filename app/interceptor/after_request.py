#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/21 10:32
"""
import json

from ext import app


@app.after_request
def response_handler(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,token,captcha-id'
    response.headers['Access-Control-Expose-Headers'] = 'captcha-id'
    # if response.headers['Content-Type'] == "application/json":
    #     # data = json.loads(response.data.decode())
    app.logger.info(f"response is {json.loads(response.data.decode('utf-8'))}")
    return response
