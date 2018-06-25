#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:33
"""
import requests


class HTTP:

    @staticmethod
    def get(url, json=True):
        data = requests.get(url)
        if data.status_code != 200:
            return {} if json else ''
        else:
            return data.json() if json else data.text
