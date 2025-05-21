from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Api
from app.resources.user import Users, User
from app.extensions import db
from config import Config






app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)



# API Endpoints
from app.resources.user import User, Users
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')





