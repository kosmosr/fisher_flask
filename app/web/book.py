#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
from flask import jsonify, request

from app.forms.book import BookForm
from app.web import v1
from utils.common import is_isbn_or_key
from app.spiders.yushu_book import YuShuBook


@v1.route('/book')
def search():
    form = BookForm(request.args)
    if form.validate():
        keyword = form.keyword.data
        page = form.page.data
        if is_isbn_or_key(keyword):
            data = YuShuBook.search_by_keyword(keyword, page)
        else:
            data = YuShuBook.search_by_isbn(keyword)

        return jsonify(data)
    else:
        dict = ([v for k, v in form.errors.items()])
        return jsonify({'errmsg': dict})
