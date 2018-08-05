#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/1 15:23
枚举
"""
from enum import IntEnum


class PendingStatus(IntEnum):
    # 等待
    Waiting = 1
    # 成功
    Success = 2
    # 拒绝
    Reject = 3
    # 撤销
    Redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            PendingStatus.Waiting.value: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            PendingStatus.Success.value: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄,交易成功'
            },
            PendingStatus.Reject.value: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            PendingStatus.Redraw.value: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            }
        }
        return key_map[status][key]
