#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 16:18
"""
from typing import List

from sqlalchemy import Column, Integer, Boolean, String, desc, func

from ext.db import db
from app.models.base import Base
from app.spiders.yushu_book import YuShuBook


class Gift(Base):
    __table_args = {'mysql_charset': 'utf8mb4'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_boook = YuShuBook()
        yushu_boook.search_by_isbn(self.isbn)
        return yushu_boook.first

    @classmethod
    def get_user_gifts(cls, uid):
        return Gift.query.filter_by(user_id=uid, launched=False).order_by(desc(Gift.create_time)).all()

    @classmethod
    def get_wish_counts(cls, isbns: List):
        counts = db.session.query(func.count(Wish.id), Wish.isbn) \
            .filter(Wish.launched == False, Wish.isbn.in_(isbns)) \
            .group_by(Wish.isbn).all()
        count_list = [{'count': count[0], 'isbn': count[1]} for count in counts]
        return count_list

    @classmethod
    def recent(cls):
        recent_gifts = Gift.query \
            .filter_by(launched=False) \
            .group_by(Gift.isbn) \
            .order_by(Gift.create_time) \
            .limit(30) \
            .distinct() \
            .with_entities(Gift) \
            .all()
        return recent_gifts


from app.models.wish import Wish
