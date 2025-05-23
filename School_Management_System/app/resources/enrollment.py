from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.enrollment import EnrollmentModel
from app.extensions import db
from dateutil.parser import parse as parser_date


# Request Parser
enrollment_args = reqparse.RequestParser()
enrollment_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be blank!")
enrollment_args.add_argument('course_id', type=int, required=True, help="Course ID cannot be blank!")
enrollment_args.add_argument('enrollment_date', type=parser_date, required=True, help="Enrollment date cannot be blank!")
enrollment_args.add_argument('status', type=str, required=True, help="Status cannot be blank!")
enrollment_args.add_argument('fee_id', type=int, required=True, help="Fee ID cannot be blank!")
enrollment_args.add_argument('payment_status', type=str, required=True, help="Payment status cannot be blank!")
enrollment_args.add_argument('payment_date', type=parser_date)



# Fields for Marshalling
enrollment_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer,
    'enrollment_date': fields.String,
    'status': fields.String,
    'fee_id': fields.Integer,
    'payment_status': fields.String,
    'payment_date': fields.String
}


# Enrollment Resource
class Enrollments(Resource):
    @marshal_with(enrollment_fields)
    def get(self):
        enrollments = EnrollmentModel.query.all()
        if not enrollments:
            abort(404, message="Enrollments not found")
        return enrollments

    @marshal_with(enrollment_fields)
    def post(self):
        args = enrollment_args.parse_args()
        try:
            new_enrollment = EnrollmentModel(
                student_id=args['student_id'],
                course_id=args['course_id'],
                enrollment_date=args['enrollment_date'],
                status=args['status'],
                fee_id=args['fee_id'],
                payment_status=args['payment_status'],
                payment_date=args['payment_date']
            )
            db.session.add(new_enrollment)
            db.session.commit()
            return new_enrollment, 201
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error creating an enrollment {str(e)}")