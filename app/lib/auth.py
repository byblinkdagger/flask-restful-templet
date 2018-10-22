from functools import wraps
from flask import current_app,request,g,jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from app.validator.error import ApiException


def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        data = verify_auth_token(token)
        if data:
            g.user = data
        else:
            raise ApiException(msg='token无效')
        return f(*args, **kwargs)
    return decorator


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise ApiException(msg='token无效')
    except SignatureExpired:
        raise ApiException(msg='token超时',error_code=402)
    uid = data['uid']
    return {'uid':uid}