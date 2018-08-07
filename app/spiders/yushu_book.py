#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:30
"""
import time
from threading import Thread

from flask import current_app

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

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def search_by_keyword(self, keyword, start, count=10):
        url = self.keyword_url.format(keyword, count, YuShuBook.cal_start(start))
        data = HTTP.get(url)
        schema = BookSchema(many=True)
        result = schema.load(data['books']).data
        dumps = schema.dump(result).data
        isbns = [book['isbn'] for book in data['books']]
        # 持久化
        app = current_app._get_current_object()
        load_data_thread = Thread(target=load_data, name='load_data', args=[app, data, isbns])
        load_data_thread.start()
        data['books'] = dumps
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
