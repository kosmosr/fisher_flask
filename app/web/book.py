#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
from flask import jsonify

from run import app
from utils.common import is_isbn_or_key
from yushu_book import YuShuBook


@app.route('/book/<keyword>/<page>')
def search(keyword, page):
    if is_isbn_or_key(keyword):
        data = YuShuBook.search_by_keyword(keyword, page)
    else:
        data = YuShuBook.search_by_isbn(keyword)

    return jsonify(data)
