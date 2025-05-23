from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.student import StudentModel
from app.extensions import db


# request parser for student
student_args = reqparse.RequestParser()