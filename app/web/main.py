import json

from flask import render_template, current_app

from app.models.gift import Gift
from app.view.book import BookViewModel
from . import web

__author__ = '七月'


@web.route('/', methods=['GET'])
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
