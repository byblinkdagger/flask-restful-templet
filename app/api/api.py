from flask import Blueprint, request, jsonify, current_app, g
from app.validator.forms import RegisterForm, LoginForm
from app.model.user import User
from app.model.collection import Collection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.lib.auth import login_check
from app.ext import db
from app.validator.error import ApiException

api = Blueprint('api', __name__)


@api.route('/v1/register', methods=['POST'])
def register():
    # application/json方式传递
    # data = request.json
    # form = ClientForm(data=data)

    # form-data方式传递
    data = request.form
    form = RegisterForm(formdata=data)
    # if form.validate():
    #     User.create_user(form.account.data,form.secret.data)
    #     return jsonify({
    #         'code': '000',
    #         'msg': '注册成功',
    #         "success": True
    #     })
    # else:
    #     return jsonify({
    #         'code': '001',
    #         'msg': '注册方式错误',
    #         "success": False
    #     })
    if form.validate_for_api():
        User.create_user(form.account.data, form.secret.data)
        return jsonify({
            'code': '000',
            'msg': '注册成功',
            "success": True
        })


@api.route('/v1/login', methods=['POST'])
def login():
    form = LoginForm(formdata=request.form)
    if form.validate_for_api():
        identity = User.verify(form.account.data, form.secret.data)
        # token 生成
        token = generate_auth_token(identity['uid'])
        return jsonify({
            'token': token.decode('ascii')
        })


# 生成token
def generate_auth_token(uid, scope=None, expiration=720):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid
    })


@api.route('/v1/user', methods=['POST'])
@login_check
def get_user():
    uid = g.user['uid']
    user = User.get_user(uid)
    return jsonify(user)
    # return jsonify({
    #     'code': '000',
    #     'msg': '成功',
    #     'user':{
    #         'userId': user.id,
    #         'account': user.account
    #     }
    # })
    # pass


# 添加收藏
@api.route('/v1/collection/add', methods=['POST'])
@login_check
def add_collection():
    uid = g.user['uid']
    c_id = request.form['c_id']
    collection = Collection.query.filter_by(id=c_id, user_id=uid).first()
    if collection:
        raise ApiException(code='001', msg='已添加收藏')
    else:
        collection = Collection.query.filter_by(id=c_id).first()
        collection.user_id = uid
        db.session.add(collection)
        db.session.commit()
        return jsonify({
            'code': '000',
            'msg': '添加成功',
            "success": True
        })


# 获取收藏
@api.route('/v1/collection/all', methods=['POST'])
@login_check
def get_collection():
    uid = g.user['uid']
    user = User.get_user(uid)
    return jsonify(user.collection)
