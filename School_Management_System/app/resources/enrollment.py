from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.enrollment import EnrollmentModel
from app.extensions import db
from dateutil.parser import parse as parser_date


# Request Parser
enrollment_args = reqparse.RequestParser()
enrollment_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be blank!")
enrollment_args.add_argument('course_id', type=int, required=True, help="Course ID cannot be blank!")
enrollment_args.add_argument('status', type=str, required=True, help="Status cannot be blank!")
enrollment_args.add_argument('fee_id', type=int, required=True, help="Fee ID cannot be blank!")
enrollment_args.add_argument('payment_status', type=str, required=True, help="Payment status cannot be blank!")
enrollment_args.add_argument('payment_date', type=str, required=True, help="Payment date cannot be blank!")



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
                status=args['status'],
            )
            db.session.add(new_enrollment)
            db.session.commit()
            return new_enrollment, 201
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error creating an enrollment {str(e)}")


# Enrollment Resource by ID
class Enrollment(Resource):
    @marshal_with(enrollment_fields)
    def get(self, id):
        enrollment = EnrollmentModel.query.get(id)
        if not enrollment:
            abort(404, message="Enrollment not found")
        return enrollment

    @marshal_with(enrollment_fields)
    def put(self, id):
        args = enrollment_args.parse_args()
        enrollment = EnrollmentModel.query.get(id)
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            enrollment.student_id = args['student_id']
            enrollment.course_id = args['course_id']
            enrollment.status = args['status']
            db.session.commit()
            return enrollment
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error updating the enrollment {str(e)}")


    @marshal_with(enrollment_fields)
    def patch(self, id):
        args = enrollment_args.parse_args()
        enrollment = EnrollmentModel.query.get(id)
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            if args['student_id']:
                enrollment.student_id = args['student_id']
            if args['course_id']:
                enrollment.course_id = args['course_id']
            if args['status']:
                enrollment.status = args['status']
            db.session.commit()
            return enrollment
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error updating the enrollment {str(e)}")


    @marshal_with(enrollment_fields)
    def delete(self, id):
        enrollment = EnrollmentModel.query.get(id)
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            db.session.delete(enrollment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error deleting the enrollment {str(e)}")