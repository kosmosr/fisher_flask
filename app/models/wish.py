#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/3 13:54
"""
from typing import List

from sqlalchemy import Column, Integer, String, desc, func

from app.models.base import Base
from app.spiders.yushu_book import YuShuBook
from ext.db import db


class Wish(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    isbn = Column(String(15), nullable=False)
    launched = db.Column(db.Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        return Wish.query.filter_by(user_id=uid, launched=False, is_deleted=False).order_by(
            desc(Wish.create_time)).all()

    @classmethod
    def get_gift_counts(cls, isbns: List):
        counts = db.session.query(func.count(Gift.isbn), Gift.isbn) \
            .filter(Gift.launched == False, Gift.isbn.in_(isbns), Gift.is_deleted == False) \
            .group_by(Gift.isbn).all()
        count_list = [{'count': count[0], 'isbn': count[1]} for count in counts]
        return count_list

    @property
    def book(self):
        yushu_boook = YuShuBook()
        yushu_boook.search_by_isbn(self.isbn)
        return yushu_boook.first


from app.models.gift import Gift
