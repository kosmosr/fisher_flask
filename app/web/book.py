#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""
import json

from flask import jsonify, request, current_app

from app.forms.book import BookForm
from app.spiders.yushu_book import YuShuBook
from app.view.book import BookCollection
from app.web import v1
from utils.common import is_isbn_or_key


@v1.route('/book', methods=['GET'])
def search():
    form = BookForm(request.args)
    books = BookCollection()

    if form.validate():
        keyword = form.keyword.data
        page = form.page.data
        yushu_book = YuShuBook()

        if is_isbn_or_key(keyword):
            yushu_book.search_by_keyword(keyword, page)
            books.fill_data(keyword, yushu_book)
        else:
            yushu_book.search_by_isbn(keyword)
            books.fill_data(keyword, yushu_book)
        return current_app.response_class(
            (json.dumps(books, ensure_ascii=False, default=lambda o: o.__dict__)),
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )
    else:
        return jsonify({'errmsg': '参数错误'})


@v1.route('/test', methods=['GET'])
def test():
    return jsonify({'data': 'tnk'})
