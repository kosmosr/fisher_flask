#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/8 16:27
"""
from app import Book
from app.common.redis_key import book_cache_key
from app.schema.model import BookSchema
from ext.db import db
from ext.redis import redis
from utils.common import bytes_to_dict


class BookCacheService:
    def __init__(self, book_params: str):
        self.key = book_cache_key
        self.params = book_params
        self.format_key = self.key.format(self.params)

    def data_exist_redis(self):
        data = redis.get(self.format_key)
        # 缓存存在
        if data:
            self.data = bytes_to_dict(data)
            return True
        else:
            return False

    def save_data(self, data: dict, many: bool = False):
        if not many:
            schema = BookSchema(strict=True)
            book = schema.load(data).data

            with db.auto_commit():
                db.session.add(book)
        else:
            schema = BookSchema(strict=True, many=True)
            books = schema.load(data['books']).data
            isbns = [book.isbn for book in books]
            distinct_books = self.distinct_books(isbns, books)
            with db.auto_commit():
                db.session.add_all(distinct_books)
        redis.set(self.format_key, data)

    def distinct_books(self, isbns, books: list):
        book_isbns = [result[0] for result in Book.query.filter(Book.isbn.in_(isbns)).with_entities(Book.isbn).all()]
        different = list(set(isbns).difference(set(book_isbns)))
        book_data = [book for book in books if book.isbn in different]
        return book_data
