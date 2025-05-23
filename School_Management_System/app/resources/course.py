from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.course import CourseModel
from app.extensions import db



# Request Parser
course_args = reqparse.RequestParser()
course_args.add_argument('code', type=str, required=True, help="Course code cannot be blank!")
course_args.add_argument('name', type=str, required=True, help="Course name cannot be blank!")
course_args.add_argument('credits', type=int, required=True, help="Course credits cannot be blank!")
course_args.add_argument('teacher_id', type=int, required=False, help="Teacher ID for the course")



# Fields for Marshalling
course_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'credits': fields.Integer,
    'teacher_id': fields.Integer,
    'enrollment_date': fields.String
}

# Course Resource
class Courses(Resource):
    @marshal_with(course_fields)
    def get(self):
        courses = CourseModel.query.all()
        if not courses:
            abort(404, message="Courses not found")
        return courses

    @marshal_with(course_fields)
    def post(self):
        args = course_args.parse_args()
        try:
            new_course = CourseModel(
                code=args['code'],
                name=args['name'],
                credits=args['credits'],
                teacher_id=args['teacher_id']
            )
            db.session.add(new_course)
            db.session.commit()
            return new_course, 201
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error creating a course {str(e)}")

# Course Resource by ID
class Course(Resource):
    @marshal_with(course_fields)
    def get(self, id):
        course = CourseModel.query.get(id)
        if not course:
            abort(404, message="Course not found")
        return course

    @marshal_with(course_fields)
    def put(self, id):
        args = course_args.parse_args()
        course = CourseModel.query.get(id)
        if not course:
            abort(404, message="Course not found")
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course, 200
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error updating the course {str(e)}")

    def delete(self, id):
        course = CourseModel.query.get(id)
        if not course:
            abort(404, message="Course not found")
        try:
            db.session.delete(course)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error deleting the course {str(e)}")
