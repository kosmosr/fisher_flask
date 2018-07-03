#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 9:06
"""
from app.spiders.yushu_book import YuShuBook


class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.publisher = data['publisher']
        self.pages = data['pages'] or ''
        self.author = '、'.join(data['author'])
        self.price = data['price']
        self.summary = data['summary'] or ''
        self.isbn = data['isbn']
        self.image = data['image']
        self.pubdate = data['pubdate']
        self.binding = data['binding']

    @property
    def intro(self):
        return '/'.join([intro for intro
                         in [self.author, self.publisher, self.price] if intro])


class BookCollection:
    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.books = []

    def fill_data(self, keyword, yushu_book: YuShuBook):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls._cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls._cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def _cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
