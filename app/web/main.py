import json

from flask import render_template, current_app, jsonify

from app.models.gift import Gift
from app.view.book import BookViewModel
from . import web

__author__ = '七月'


@web.route('/', methods=['GET'])
def index():
    recent_gifts = Gift.recent()
    recent = [BookViewModel(gift.book).to_json() for gift in recent_gifts]
    print(recent)
    return jsonify(recent)


@web.route('/personal')
def personal_center():
    pass
