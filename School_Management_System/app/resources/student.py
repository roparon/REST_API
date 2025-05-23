from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.student import StudentModel
from app.extensions import db
from dateutil.parser import parse as parse_date


# request parser for student
student_args = reqparse.RequestParser()
student_args.add_argument('first_name', type=str, required=True, help="First Name of the student cannot be blank")
student_args.add_argument('last_name', type=str, required=True, help="Last Name of the student cannot be blank")
student_args.add_argument('student_id', type=str, required=True, help="Student ID cannot be blank")
student_args.add_argument('email', type=str, required=True, help="Email of the student cannot be blank")
student_args.add_argument('date_of_birth', type=parse_date)
student_args.add_argument('Enrollment_date', type=parse_date)



# student fields for marshalling
student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'student_id': fields.String,
    'email': fields.String,
    'date_of_birth': fields.String,
    'enrollment_date': fields.String
}

# student resource
class Students(Resource):
    @marshal_with(student_fields)
    def get(self):
        students = StudentModel.query.all()
        if not students:
            abort(404, message="Students not found")
        return students

    @marshal_with(student_fields)
    def post(self):
        args = student_args.parse_args()
        try:
            new_student = StudentModel(
                first_name=args['first_name'],
                last_name=args['last_name'],
                student_id=args['student_id'],
                email=args['email'],
                date_of_birth=args['date_of_birth'],
                enrollment_date=args['enrollment_date']
            )
            db.session.add(new_student)
            db.session.commit()
            return new_student, 201
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error creating a student{str(e)}")

    @marshal_with(student_fields)
    def put(self, id):
        args = student_args.parse_args()
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message="Student not found")
        try:
            student.first_name = args['first_name']
            student.last_name = args['last_name']
            student.student_id = args['student_id']
            student.email = args['email']
            student.date_of_birth = args['date_of_birth']
            student.enrollment_date = args['enrollment_date']
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error updating a student{str(e)}")

    @marshal_with(student_fields)
    def delete(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message="Student not found")
        try:
            db.session.delete(student)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error deleting a student{str(e)}")