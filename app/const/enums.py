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
