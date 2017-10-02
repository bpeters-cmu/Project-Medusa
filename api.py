from flask import request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from models import User
import traceback

auth = HTTPBasicAuth()

class Register(Resource):

    def get(self):
        print('entering get')
        try:
            return self.app_service.get_schedule()
        except:
            return '400'

    def post(self):
        data = request.get_json(force=True)
        try:
            self.app_service.create_schedule(data)
            return '200'
        except BaseException as e:
            print('Exception: ', str(e))
            return '400'


class Login(Resource):
    @auth.get_password
    def get_password(user):
        user = User.query.filter_by(username=user)
        if user:
            return user.password
        return None

    @auth.login_required
    def get(self, id=None):
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
