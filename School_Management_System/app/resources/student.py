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