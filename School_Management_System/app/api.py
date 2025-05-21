from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app import db, api, app





#Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db. Column(db.String(80), unique=True, nullable=False)
    email = db. Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.username} {self.email}"

# Request Parser
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help = "Username cannot be blank!")
user_args.add_argument('email', type=str, required=True, help = "email cannot be blank!")


# Output fields
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

# Resource for all users
class Users(Resource):
    @marshal_with(user_fields)
    #Getting all the users
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message ='Users not found')
        return users
    

    # create a user
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        new_user = UserModel(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, 'User not found!')
        return user, 200

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, 'No user with that id')
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user, 200
    
    @marshal_with(user_fields)
    def delete(sef, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort (404, 'Cannot delete a none existing user')
        db.session.delete(user)
        db.session.commit()
        return 'User deleted succesfully'

# API Endpoints
from app.api import User, Users
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')

