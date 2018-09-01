# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/7/16 21:10
"""
from app.common.httpcode import ErrorCode, BadRequest, InternalServerError, NotFound, Unauthorized, Forbidden

REQUEST_USER_ID = 'uid'

SATISFY_WISH_MSG = '已向他/她发送了一封邮件，如果他/她愿意接受你的赠送,你将收到一个鱼漂'

# validate
VALIDATE_NICKNAME_EXIST = '昵称已重复'
VALIDATE_EMAIL_EXIST = '邮箱已重复'
VALIDATE_NICKNAME_ERROR = '昵称至少需要两个字符，最多10个字符'
VALIDATE_PASSWORD_ERROR = '密码不可以为空或者至少需要6个字符'
VALIDATE_RESERT_PASSWORD_ERROR = '输入密码不一样，请重新输入'

# 400
VALIDATE_ERROR = ErrorCode(BadRequest.http_code, '01', '校验错误')
USER_PASSWORD_ERROR = ErrorCode(BadRequest.http_code, '02', '密码错误')
SAVE_BOOK_ERROR = ErrorCode(BadRequest.http_code, '03', '这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')
USER_RAWPASSWORD_ERROR = ErrorCode(BadRequest.http_code, '04', '原密码错误，请重试')
SAVE_WISH_ERROR = ErrorCode(BadRequest.http_code, '05', '这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')
SATISFY_WISH_ERROR = ErrorCode(BadRequest.http_code, '06', '你还没有上传此书，'
                                                           '请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
SEND_DRIFT_IS_YOURSELF = ErrorCode(BadRequest.http_code, '07', '这本书是你自己的，不能向自己索要书籍噢')
REDRAW_GIFT_ERROR = ErrorCode(BadRequest.http_code, '08', '这个礼物正处于交易状态，请先前往鱼漂完成该交易')
BOOK_ISBN_ERROR = ErrorCode(BadRequest.http_code, '09', '输入的ISBN错误，请核准后再输入')
SATISFY_WISHER_ERROR = ErrorCode(BadRequest.http_code, '10', '对方尚未把此书加入到心愿清单，无法向对方赠送')

# 401
NOT_LOGIN = ErrorCode(Unauthorized.http_code, '01', '当前未登录')
TOKEN_INVALID = ErrorCode(Unauthorized.http_code, '02', 'TOKEN失效')

# 403
USER_CANNOT_DRIFT = ErrorCode(Forbidden.http_code, '01', '用户鱼豆不足或者不满足发起条件')

# 404
USER_NOT_EXIST = ErrorCode(NotFound.http_code, '01', '用户不存在或者被禁用')
ENDPOINT_NOT_EXIST = ErrorCode(NotFound.http_code, '02', '访问路由不存在')

# server
ServerError = ErrorCode(InternalServerError.http_code, '01', '内部错误')
