from flask import g

from app.common.const import REQUEST_USER_ID, USER_NOT_EXIST
from app.common.response import SuccessResponse, ErrorResponse
from app.decorator import login_required
from app.models.gift import Gift
from app.models.user import User
from app.schema.model import BookSchema
from app.schema.view import UserPersonalSchema
from . import api_v1

__author__ = 'kosmosr'


@api_v1.route('/', methods=['GET'])
def index():
    recent_gifts = Gift.recent()
    schema = BookSchema(only=('title', 'summary', 'author', 'isbn', 'image'))
    recent = [schema.dump(gift.book).data for gift in recent_gifts]
    return SuccessResponse(data=recent)()


@login_required
@api_v1.route('/user', methods=['GET'])
def personal_center():
    uid = getattr(g, REQUEST_USER_ID)
    user = User.query.filter_by(id=uid).first()
    if not user:
        return ErrorResponse(USER_NOT_EXIST).make()
    schema = UserPersonalSchema()
    data = schema.dump(user.summary).data
    return SuccessResponse(data=data)()
