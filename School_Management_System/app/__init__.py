from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Api
from app.resources.user import Users, User
from app.resources.teacher import Teachers, Teacher
from app.resources.student import Students, Student
from app.resources.enrollment import Enrollments, Enrollment
from app.resources.course import Courses, Course
from app.resources.fee import Fees, Fee
from app.extensions import db
from config import Config
from flask_migrate import Migrate





app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



# API Endpoints
from app.resources.user import User, Users
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Teachers, '/api/teachers')
api.add_resource(Teacher, '/api/teachers/<int:id>')
api.add_resource(Students, '/api/students')
api.add_resource(Student, '/api/students/<int:id>')
api.add_resource(Enrollments, '/api/enrollments')
api.add_resource(Enrollment, '/api/enrollments/<int:id>')
api.add_resource(Courses, '/api/courses')
api.add_resource(Course, '/api/courses/<int:id>')
api.add_resource(Fees, '/api/fees')
api.add_resource(Fee, '/api/fees/<int:id>')


