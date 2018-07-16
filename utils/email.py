#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/13 14:49
"""
from flask import render_template
from flask_mail import Message

from ext import mail


def send_email(to, subject, template, **kwargs):
    """

    :param to: 收件人
    :param subject: 标题
    :param template:
    :param kwargs:
    :return:
    """
    # msg = Message('测试邮件', body='Test', recipients=['376170361@qq.com'])
    msg = Message('[FISHER]' + ' ' + subject,
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
