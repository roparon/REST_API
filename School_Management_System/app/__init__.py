from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Api
from app.resources.user import Users, User
from app.extensions import db # type: ignore





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db.init_app(app)
api = Api(app)





