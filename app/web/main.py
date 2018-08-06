from flask import g

from app.common.const import REQUEST_USER_ID
from app.common.httpcode import OK
from app.common.response import SuccessResponse
from app.models.gift import Gift
from app.models.user import User
from app.view.book import BookViewModel
from . import api_v1

__author__ = 'kosmosr'


@api_v1.route('/', methods=['GET'])
def index():
    uid = getattr(g, REQUEST_USER_ID, None)
    recent_gifts = Gift.recent()
    recent = [BookViewModel(gift.book).to_json() for gift in recent_gifts]
    if uid:
        user = User.query.filter_by(id=uid).first()
        if user:
            recent.append({'nickname': user.nickname})
    return SuccessResponse(http_code=OK, data=recent).make()


@api_v1.route('/personal')
def personal_center():
    pass
