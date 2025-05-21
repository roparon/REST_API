from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.user2 import UserModel
from app.extensions import db




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
def post(self):
        args = user_args.parse_args()
        try:
            existing_user = UserModel.query.filter_by(username=args['username']).first()
            if existing_user:
                abort(400, message="User with this username already exists")
            new_user = UserModel(username=args['username'], email=args['email'])
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"There was an error creating the user: {e}")
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



