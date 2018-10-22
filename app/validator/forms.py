from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length, ValidationError
from app.lib.enums import ClientType
from app.model.user import User
from .error import ApiException


class RegisterForm(Form):
    account = StringField(validators=[DataRequired(message='账号不能为空'), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, type):
        try:
            clienttype = ClientType(type.data)
        except ValueError as e:
            raise ApiException(msg='暂不支持此注册方式')
        pass

    def validate_account(self, account):
        if User.query.filter_by(account=account.data).first():
            raise ApiException(msg='该账号已经注册过')
        pass


    def validate_for_api(self):
        valid = super(RegisterForm, self).validate()
        if not valid:
            raise ApiException(msg=self.errors)
        return self

class LoginForm(Form):
    account = StringField(validators=[DataRequired(message='账号不能为空'), length(min=5, max=32)])
    secret = StringField(DataRequired(message='密码不能为空'))

    def validate_for_api(self):
        valid = super(LoginForm,self).validate()
        if not valid:
            raise ApiException(msg=self.errors)
        return self
