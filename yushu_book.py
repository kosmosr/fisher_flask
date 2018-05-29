#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/22 16:30
"""
from httper import HTTP


class YuShuBook:
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'

    @classmethod
    def search_by_keyword(cls, keyword, start, count=10):
        url = cls.keyword_url.format(keyword, count, start)
        data = HTTP.get(url)
        return data

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        data = HTTP.get(url)
        return data
