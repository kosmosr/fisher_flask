from flask import jsonify, make_response

from app.models.gift import Gift
from app.view.book import BookViewModel
from . import api_v1

__author__ = '七月'


@api_v1.route('/', methods=['GET'])
def index():
    recent_gifts = Gift.recent()
    recent = [BookViewModel(gift.book).to_json() for gift in recent_gifts]
    print(recent)
    success = {'success': 'ok'}
    return make_response(jsonify(success), 400)


@api_v1.route('/personal')
def personal_center():
    pass
