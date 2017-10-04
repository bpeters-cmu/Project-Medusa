from flask import request, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
import traceback
import app_service

auth = HTTPBasicAuth()

class Register(Resource):
    def __init__():
        from models import User

    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = User(data['username'], data['password'], data['tenancy_ocid'],
            data['user_ocid'], data['fingerprint'], data['private_key'], data['region'])
            new_user.insert();
            return '200'
        except BaseException as e:
            print('Exception: ', str(e))
            return '400'


class Instance(Resource):
    def __init__(self):
        from models import User

    @auth.login_required
    def get(self, id=None):
        data = request.get_json(force=True)

        try:
            return app_service.get_instances(g.user)

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
