#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import request, render_template, flash

from app.forms.book import BookForm
from app.spiders.yushu_book import YuShuBook
from app.view.book import BookCollection, BookViewModel
from app.web import web
from utils.common import is_isbn_or_key


@web.route('/book/search', methods=['GET'])
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
        # return current_app.response_class(
        #     (json.dumps(books, ensure_ascii=False, default=lambda o: o.__dict__)),
        #     mimetype=current_app.config['JSONIFY_MIMETYPE']
        # )
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])
