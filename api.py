from flask import request, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from models import User
import traceback

auth = HTTPBasicAuth()

class Register(Resource):

    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = User(data['username'], data['password'], data['tenancy_ocid'],
            data['user_ocid'], data['fingerprint'], data['private_key_path'], data['region'])
            new_user.insert();
            return '200'
        except BaseException as e:
            print('Exception: ', str(e))
            return '400'


class Login(Resource):

    @auth.login_required
    def get(self, id=None):
        data = request.get_json(force=True)
        try:
            if not id:
                return self.app_service.get_appointments()
            else:
                return self.app_service.get_appointment(id)

        except BaseException as e:
            print('Exception: ', str(e))
            return '400'

    def post(self):
        data = request.get_json(force=True)
        try:
            return self.app_service.create_appointment(data)
        except BaseException as e:
            print('Exception: ', str(e))
            return '400'

    @auth.get_password
    def get_password(user):
        user = User.query.filter_by(username=user).first()
        if user:
            return user.password
        return None

    @auth.verify_password
    def verify_password(username, password):
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True
