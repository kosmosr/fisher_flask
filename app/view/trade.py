#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/10 10:33
"""

from app.models.user import User


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self._parse(goods)

    def _parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(trade) for trade in goods]

    @staticmethod
    def __map_to_trade(single):
        return {
            'user_name': User.query.filter_by(id=single.user_id).first().nickname,
            'time': single.create_time.strftime('%Y-%m-%d'),
            'id': single.id
        }
