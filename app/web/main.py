from app.common.httpcode import OK
from app.common.response import SuccessResponse
from app.models.gift import Gift
from app.view.book import BookViewModel
from . import api_v1

__author__ = 'kosmosr'


@api_v1.route('/', methods=['GET'])
def index():
    recent_gifts = Gift.recent()
    recent = [BookViewModel(gift.book).to_json() for gift in recent_gifts]
    return SuccessResponse(http_code=OK, data=recent).make()


@api_v1.route('/personal')
def personal_center():
    pass
