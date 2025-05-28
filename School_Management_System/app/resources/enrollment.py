from flask_restful import Resource, reqparse, fields, marshal_with, abort
from app.models.enrollment import EnrollmentModel
from app.extension import db
from datetime import datetime, timezone
from dateutil.parser import parse as date_parse


# Request Parser
enrollment_args = reqparse.RequestParser()
enrollment_args.add_argument('student_id', type=int, help='Student ID cannot be blank', required=True)
enrollment_args.add_argument('course_id', type=int, help='Course ID cannot be blank', required=True)
enrollment_args.add_argument('enrolment_date', type=date_parse)
enrollment_args.add_argument('grade', type=str, help='Grade must be provided')
enrollment_args.add_argument('status', type=str, help='Status must be provided')

# Fields for marshalling
enrollment_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer,
    'enrolment_date': fields.DateTime,
    'grade': fields.String,
    'status': fields.String
}

# Enrollment Resource
class Enrollments(Resource):
    @marshal_with(enrollment_fields)
    def get(self):
        """Get all enrollments
        ---
        tags:
            - Enrollments
        summary: Retrieve all enrollments
        description: This endpoint retrieves all enrollments from the system.
        responses:
            200:
                description: List of all enrollments retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the enrollment
                            student_id:
                                type: integer
                                description: The ID of the student
                            course_id:
                                type: integer
                                description: The ID of the course
                            enrolment_date:
                                type: string
                                format: date-time
                                description: The enrollment date
                            grade:
                                type: string
                                description: The grade received
                            status:
                                type: string
                                description: The enrollment status
            404:
                description: No enrollments found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollments not found!
        """
        enrollments = EnrollmentModel.query.all()
        if not enrollments:
            abort(404, message="Enrollments not found")
        return enrollments

    @marshal_with(enrollment_fields)
    def post(self):
        """Create a new enrollment
        ---
        tags:
            - Enrollments
        summary: Create a new enrollment
        description: This endpoint creates a new enrollment in the system.
        parameters:
            - in: body
              name: enrollment
              description: Enrollment data
              required: true
              schema:
                  type: object
                  required:
                      - student_id
                      - course_id
                  properties:
                      student_id:
                          type: integer
                          description: The ID of the student
                      course_id:
                          type: integer
                          description: The ID of the course
                      enrolment_date:
                          type: string
                          format: date-time
                          description: The enrollment date
                      grade:
                          type: string
                          description: The grade received
                      status:
                          type: string
                          description: The enrollment status
        responses:
            201:
                description: Enrollment created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created enrollment
                        student_id:
                            type: integer
                            description: The ID of the student
                        course_id:
                            type: integer
                            description: The ID of the course
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrollment date
                        grade:
                            type: string
                            description: The grade received
                        status:
                            type: string
                            description: The enrollment status
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = enrollment_args.parse_args()
        try:
            enrollment = EnrollmentModel(
                student_id=args['student_id'],
                course_id=args['course_id'],
                enrolment_date=args['enrolment_date'] if args['enrolment_date'] else datetime.now(timezone.utc),
                grade=args['grade'],
                status=args['status'] if args['status'] else 'enrolled'
            )
            db.session.add(enrollment)
            db.session.commit()
            return enrollment, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error creating enrollment: {str(e)}")
    
class Enrollment(Resource):
    @marshal_with(enrollment_fields)
    def get(self, id):
        """Get a specific enrollment by ID
        ---
        tags:
            - Enrollments
        summary: Retrieve an enrollment by ID
        description: This endpoint retrieves a specific enrollment by its ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the enrollment
        responses:
            200:
                description: Enrollment retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the enrollment
                        student_id:
                            type: integer
                            description: The ID of the student
                        course_id:
                            type: integer
                            description: The ID of the course
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrollment date
                        grade:
                            type: string
                            description: The grade received
                        status:
                            type: string
                            description: The enrollment status
            404:
                description: Enrollment not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollment not found!
        """
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message="Enrollment not found")
        return enrollment
    
    @marshal_with(enrollment_fields)
    def put(self, id):
        """Update an enrollment by ID
        ---
        tags:
            - Enrollments
        summary: Update an enrollment
        description: This endpoint updates an existing enrollment's information.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the enrollment
            - in: body
              name: enrollment
              description: Updated enrollment data
              required: true
              schema:
                  type: object
                  required:
                      - student_id
                      - course_id
                  properties:
                      student_id:
                          type: integer
                          description: The ID of the student
                      course_id:
                          type: integer
                          description: The ID of the course
                      enrolment_date:
                          type: string
                          format: date-time
                          description: The enrollment date
                      grade:
                          type: string
                          description: The grade received
                      status:
                          type: string
                          description: The enrollment status
        responses:
            200:
                description: Enrollment updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the enrollment
                        student_id:
                            type: integer
                            description: The ID of the student
                        course_id:
                            type: integer
                            description: The ID of the course
                        enrolment_date:
                            type: string
                            format: date-time
                            description: The enrollment date
                        grade:
                            type: string
                            description: The grade received
                        status:
                            type: string
                            description: The enrollment status
            404:
                description: Enrollment not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollment not found!
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = enrollment_args.parse_args()
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            enrollment.student_id = args['student_id']
            enrollment.course_id = args['course_id']
            if args['enrolment_date']:
                enrollment.enrolment_date = args['enrolment_date']
            if args['grade']:
                enrollment.grade = args['grade']
            if args['status']:
                enrollment.status = args['status']
            db.session.commit()
            return enrollment
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error updating enrollment: {str(e)}")

    def delete(self, id):
        """Delete an enrollment by ID
        ---
        tags:
            - Enrollments
        summary: Delete an enrollment
        description: This endpoint deletes an enrollment from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the enrollment
        responses:
            204:
                description: Enrollment deleted successfully
            404:
                description: Enrollment not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Enrollment not found!
            400:
                description: Bad request - error deleting enrollment
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            db.session.delete(enrollment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error deleting enrollment: {str(e)}")