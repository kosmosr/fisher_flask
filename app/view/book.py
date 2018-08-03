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
        self.binding = data['binding'] or ''

    @property
    def intro(self):
        return '/'.join([intro for intro
                         in [self.author, self.publisher, self.price] if intro])

    def to_json(self):
        return {
            'title': self.title,
            'publisher': self.publisher,
            'pages': self.pages,
            'author': self.author,
            'price': self.price,
            'summary': self.summary,
            'isbn': self.isbn,
            'image': self.image,
            'pubdate': self.pubdate,
            'binding': self.binding
        }


class BookCollection:
    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.books = []

    def fill_data(self, keyword, yushu_book: YuShuBook):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
