from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url

db = SQLAlchemy(app)

from api import Login, Register

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(debug=True)
