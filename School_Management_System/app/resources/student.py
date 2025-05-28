from flask_restful import Resource, reqparse, fields, marshal_with, abort
from app.models import StudentModel
from app.extensions import db
from dateutil.parser import parse as date_parse


#Request Parser
student_args = reqparse.RequestParser()
student_args.add_argument('first_name', type=str, help='First name of the student cannot be blank', required=True)
student_args.add_argument('last_name', type=str, help='Last name of the student cannot be blank', required=True)
student_args.add_argument('student_id', type=str, help='Student ID of the student cannot be blank', required=True)
student_args.add_argument('email', type=str, help='Email of the student cannot be blank', required=True)
student_args.add_argument('date_of_birth', type=date_parse)
student_args.add_argument('enrolment_date', type=date_parse)

# Fields for marshalling
student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'student_id': fields.String,
    'email': fields.String,
    'date_of_birth': fields.DateTime,
    'enrolment_date': fields.DateTime
}

# Student Resource
class Students(Resource):
    @marshal_with(student_fields)
    def get(self):
        """Get all students
        ---
        tags:
            - Students
        summary: Retrieve all students
        description: This endpoint retrieves all students from the system.
        responses:
            200:
                description: List of all students retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the student
                            first_name:
                                type: string
                                description: The first name of the student
                            last_name:
                                type: string
                                description: The last name of the student
                            student_id:
                                type: string
                                description: The student ID
                            email:
                                type: string
                                description: The email address of the student
                            date_of_birth:
                                type: string
                                format: date-time
                                description: The date of birth of the student
                            enrolment_date:
                                type: string
                                format: date-time
                                description: The enrolment date of the student
            404:
                description: No students found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Students not found!
        """
        students = StudentModel.query.all()
        if not students:
            abort(404, message="Students not found")
        return students

    @marshal_with(student_fields)
    def post(self):
        """Create a new student
        ---
        tags:
            - Students
        summary: Create a new student
        description: This endpoint creates a new student in the system.
        parameters:
            - in: body
              name: student
              description: Student data
              required: true
              schema:
                  type: object
                  required:
                      - first_name
                      - last_name
                      - student_id
                      - email
                  properties:
                      first_name:
                          type: string
                          description: The first name of the student
                      last_name:
                          type: string
                          description: The last name of the student
                      student_id:
                          type: string
                          description: The student ID
                      email:
                          type: string
                          description: The email address of the student
                      date_of_birth:
                          type: string
                          format: date-time
                          description: The date of birth of the student
                      enrolment_date:
                          type: string
                          format: date-time
                          description: The enrolment date of the student
        responses:
            201:
                description: Student created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created student
                        first_name:
                            type: string
                            description: The first name of the student
                        last_name:
                            type: string
                            description: The last name of the student
                        student_id:
                            type: string
                            description: The student ID
                        email:
                            type: string
                            description: The email address of the student
                        date_of_birth:
                            type: string
                            format: date-time
                            description: The date of birth of the student
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrolment date of the student
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = student_args.parse_args()
        student = StudentModel(**args)
        db.session.add(student)
        db.session.commit()
        return student, 201
    
class Student(Resource):
    @marshal_with(student_fields)
    def get(self, id):
        """Get a specific student by ID
        ---
        tags:
            - Students
        summary: Retrieve a student by ID
        description: This endpoint retrieves a specific student by their ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the student
        responses:
            200:
                description: Student retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the student
                        first_name:
                            type: string
                            description: The first name of the student
                        last_name:
                            type: string
                            description: The last name of the student
                        student_id:
                            type: string
                            description: The student ID
                        email:
                            type: string
                            description: The email address of the student
                        date_of_birth:
                            type: string
                            format: date-time
                            description: The date of birth of the student
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrolment date of the student
            404:
                description: Student not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Student not found!
        """
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message="Student not found")
        return student
    @marshal_with(student_fields)
    def put(self, id):
        """Update a student by ID
        ---
        tags:
            - Students
        summary: Update a student
        description: This endpoint updates an existing student's information.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the student
            - in: body
              name: student
              description: Updated student data
              required: true
              schema:
                  type: object
                  required:
                      - first_name
                      - last_name
                      - student_id
                      - email
                  properties:
                      first_name:
                          type: string
                          description: The first name of the student
                      last_name:
                          type: string
                          description: The last name of the student
                      student_id:
                          type: string
                          description: The student ID
                      email:
                          type: string
                          description: The email address of the student
                      date_of_birth:
                          type: string
                          format: date-time
                          description: The date of birth of the student
                      enrolment_date:
                          type: string
                          format: date-time
                          description: The enrolment date of the student
        responses:
            200:
                description: Student updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the student
                        first_name:
                            type: string
                            description: The first name of the student
                        last_name:
                            type: string
                            description: The last name of the student
                        student_id:
                            type: string
                            description: The student ID
                        email:
                            type: string
                            description: The email address of the student
                        date_of_birth:
                            type: string
                            format: date-time
                            description: The date of birth of the student
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrolment date of the student
            404:
                description: Student not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Student not found!
        """
        args = student_args.parse_args()
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message="Student not found")
        # for key, value in args.items():
        #     setattr(student, key, value)
        student.first_name = args['first_name']
        student.last_name = args['last_name']
        student.student_id = args['student_id']
        student.email = args['email']
        student.date_of_birth = args['date_of_birth']
        student.enrolment_date = args['enrolment_date']
        db.session.commit()
        return student

    def delete(self, id):
        """Delete a student by ID
        ---
        tags:
            - Students
        summary: Delete a student
        description: This endpoint deletes a student from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the student
        responses:
            204:
                description: Student deleted successfully
            404:
                description: Student not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Student not found!
        """
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message="Student not found")
        db.session.delete(student)
        db.session.commit()
        return '', 204




