#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:30
"""
from utils.httper import HTTP


# TODO: 查询数据持久化 减少访问API
class YuShuBook:
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_keyword(self, keyword, start, count=10):
        url = self.keyword_url.format(keyword, count, self.cal_start(start))
        data = HTTP.get(url)
        self.__fill_collection(data)

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        data = HTTP.get(url)
        self.__fill_single(data)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def cal_start(self, page):
        return (page - 1) * 10
