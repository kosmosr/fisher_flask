#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:30
"""
import time

from app import Book
from app.log import logger
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
        # self.md5_params = md5_params
        # self.book_service = BookCacheService(self.md5_params)

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def search_by_keyword(self, keyword, start, count=10):
        schema = BookSchema(many=True)
        # if self.book_service.data_exist_redis():
        #     data = self.book_service.data
        #     self.__fill_collection(data['total'], data)
        # else:
        url = self.keyword_url.format(keyword, count, YuShuBook.cal_start(start))
        data = HTTP.get(url)
        dumps = schema.dump(data['books']).data
        # books = {'books': dumps, 'total': data['total']}
        # TODO: 异步
        # self.book_service.save_data(books, True)
        self.__fill_collection(data['total'], dumps)

    def search_by_isbn(self, isbn):
        schema = BookSchema()
        # if self.book_service.data_exist_redis():
        #     data = self.book_service.data
        #     self.__fill_single(data)
        # else:
        url = self.isbn_url.format(isbn)
        data = HTTP.get(url)
        # self.book_service.save_data(data)
        dumps = schema.dump(data).data
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


def load_data(app, data, isbns):
    with app.app_context():
        starttime = time.time()
        book_isbns = [result[0] for result in Book.query.filter(Book.isbn.in_(isbns)).with_entities(Book.isbn).all()]
        different = list(set(isbns).difference(set(book_isbns)))
        book_data = [book for book in data['books'] if book['isbn'] in different]
        schema = BookSchema(strict=True)
        for book in book_data:
            result = schema.load(book)
            entity = result.data
            db.session.add(entity)
        db.session.commit()
        endtime = time.time()
        logger.info(f'关键字持久化耗时: {(endtime-starttime)}s')
