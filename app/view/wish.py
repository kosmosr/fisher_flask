#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/12 9:49
"""
from typing import List

from app.schema.model import BookSchema


class MyWishes:

    def __init__(self, wishes_of_mine: List, gift_count_list: List):
        self.gifts = []

        self.__gifts_of_mine = wishes_of_mine
        self.__wish_count_list = gift_count_list
        self.gifts = self.__parse()

    def __parse(self):
        return [self.__matching(gift) for gift in self.__gifts_of_mine]

    def __matching(self, gift):
        schema = BookSchema()
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
                break
        r = {
            'id': gift.id,
            'book': schema.dump(gift.book).data,
            'wishes_count': count
        }

        return r
