#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:30
"""

from app import Book
from app.schema.model import BookSchema
from ext.db import db
from utils.httper import HTTP


# TODO: 查询数据持久化 减少访问API
class YuShuBook:
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'

    def __init__(self):
        self.total = 0
        self.books = []

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def search_by_keyword(self, keyword, start, count=10):
        schema = BookSchema(many=True)
        url = self.keyword_url.format(keyword, count, YuShuBook.cal_start(start))
        data = HTTP.get(url)
        dumps = schema.dump(data['books']).data
        self.__fill_collection(data['total'], dumps)

    def search_by_isbn(self, isbn):
        schema = BookSchema()
        book = Book.query.filter(Book.isbn == isbn).first()
        if book:
            dumps = schema.dump(book).data
        else:
            url = self.isbn_url.format(isbn)
            data = HTTP.get(url)
            if not data:
                self.total = 0
                return
            dumps = schema.dump(data).data
            with db.auto_commit():
                book = Book(**dumps)
                db.session.add(book)
        self.__fill_single(dumps)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, total: int, books: list):
        self.total = total
        self.books = books

    @staticmethod
    def cal_start(page):
        return (page - 1) * 10
