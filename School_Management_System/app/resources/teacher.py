from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.teacher import TeacherModel
from app.extensions import db


teacher_args = reqparse.RequestParser()
teacher_args.add_argument('first_name', type=str, required=True, help="First Name is required")
teacher_args.add_argument('last_name', type=str, required=True, help="Last Name is required")
teacher_args.add_argument('email', type=str, required=True, help="Email is required")
teacher_args.add_argument('phone', type=str)
teacher_args.add_argument('department', type=str)
teacher_args.add_argument('credits', type=int, help="Credits is required")

teacher_fields = {
    'id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    'email':fields.String,
    'phone':fields.String,
    'department':fields.String,
    'credits':fields.Integer,
    'courses':fields.String,
    'hire_date':fields.String
}


class Teachers(Resource):
    @marshal_with(teacher_fields)
    def get(self):
        teachers = TeacherModel.query.all()
        if not teachers:
            abort(404, message="Teachers not found")
        return teachers
    
    @marshal_with(teacher_fields)
    def post(self):
        args = teacher_args.parse_args()
        try:
            new_teacher = TeacherModel(
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                phone=args['phone'],
                department=args['department'],
                credits=args['credits']
                )
            db.session.add(new_teacher)
            db.session.commit()
            return new_teacher, 201
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error creating a teacher{str(e)}")


#create a resource by implementig the get a specific teacher by id, edit, delete

class Teacher(Resource):
    @marshal_with(teacher_fields)
    def get(self, id):
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message="Teacher not found")
        return teacher, 200
    

class Teacher(Resource):
    @marshal_with(teacher_fields)
    def patch(self, id):
        args = teacher_args.parse_args()
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message="Teacher not found")
        try:
            if args['first_name']:
                teacher.first_name = args['first_name']
            if args['last_name']:
                teacher.last_name = args['last_name']
            if args['email']:
                teacher.email = args['email']
            if args['phone']:
                teacher.phone = args['phone']
            if args['department']:
                teacher.department = args['department']
            if args['credits']:
                teacher.credits = args['credits']
            db.session.commit()
            return teacher, 200
        
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error updating a teacher{str(e)}")


class Teacher(Resource):
    def delete(self, id):
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message="Teacher not found")
        try:
            db.session.delete(teacher)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error deleting a teacher{str(e)}")