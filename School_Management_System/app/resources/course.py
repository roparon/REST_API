from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.course import CourseModel
from app.extensions import db



# Request Parser
# Arguments for CourseModel
course_args = reqparse.RequestParser()
course_args.add_argument('code', type=str, required=True, help="Course code cannot be blank!")
course_args.add_argument('name', type=str, required=True, help="Course name cannot be blank!")
course_args.add_argument('credits', type=int, required=True, help="Course credits cannot be blank!")
course_args.add_argument('teacher_id', type=int, required=False, help="Teacher ID for the course")
