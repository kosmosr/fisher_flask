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
        url = self.keyword_url.format(keyword, count, self.cal_start(start))
        data = HTTP.get(url)
        self.__fill_collection(data)

    def search_by_isbn(self, isbn):
        book = Book.query.filter(Book.isbn == isbn).first()
        schema = BookSchema()
        if not book:
            url = self.isbn_url.format(isbn)
            data = HTTP.get(url)
            book = schema.load(data).data
            with db.auto_commit():
                db.session.add(book)
            self.__fill_single(schema.dump(book).data)
        else:
            self.__fill_single(schema.dump(book).data)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def cal_start(self, page):
        return (page - 1) * 10


if __name__ == '__main__':
    yushu_book = YuShuBook()
    # yushu_book.search_by_keyword('鲁迅', start=32, count=20)
    yushu_book.search_by_isbn('9787115207012')
    print(yushu_book.books)
