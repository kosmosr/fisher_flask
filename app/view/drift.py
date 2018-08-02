#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/2 10:55
"""
from typing import List

from app.const.enums import PendingStatus
from app.models.drift import Drift


class DriftCollection:
    def __init__(self, drifts: List, current_user_id: int):
        self.data = []
        self.current_user_id = current_user_id
        self.__parse(drifts)

    def __parse(self, drifts):
        self.data = [DriftViewModel(drift, self.current_user_id).data for drift in drifts]


class DriftViewModel:
    def __init__(self, drift: Drift, current_user_id: int):
        self.current_user_id = current_user_id
        self.data = self.__parse(drift)

    def requester_or_gifter(self, drift):
        if drift.requester_id == self.current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift: Drift):
        you_are = self.requester_or_gifter(drift)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_time.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'status_str': PendingStatus.pending_str(drift.pending, you_are)
        }
        return r
