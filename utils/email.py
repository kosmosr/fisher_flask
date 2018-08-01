#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/13 14:49
"""
from threading import Thread

from flask import render_template, Flask, current_app
from flask_mail import Message

from ext import mail


def send_async_email(app: Flask, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


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
    app = current_app._get_current_object()
    mail_thread = Thread(target=send_async_email, name='mail_thread', args=[app, msg])
    mail_thread.start()
