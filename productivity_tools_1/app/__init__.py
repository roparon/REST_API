from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
rest_api = Api(app)

from app.api.resources import ChatResource
rest_api.add_resource(ChatResource, '/api/chat')

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app import routes, models
