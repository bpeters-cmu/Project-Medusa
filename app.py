from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import config

application = Flask(__name__)
api = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = config.db_url

db = SQLAlchemy(application)

from api import Instance, Register

api.add_resource(Instance, '/instances')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=False)
