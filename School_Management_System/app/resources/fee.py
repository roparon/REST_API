from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.fee import FeeModel
from app.extensions import db
from datetime import datetime



# Request Parser
fee_args = reqparse.RequestParser()
fee_args.add_argument("student_id", type=int, required=True, help="Student ID is required")
fee_args.add_argument("amount", type=float, required=True, help="Amount is required and must be a number")
fee_args.add_argument("fee_type", type=str, required=True, choices=("tuition", "accommodation", "graduation"), help="Fee type must be 'tuition', 'accommodation', or 'graduation'")
fee_args.add_argument("semester", type=str, required=False)
fee_args.add_argument("payment_date", type=str, required=False, help="Payment date must be in YYYY-MM-DD format")
fee_args.add_argument("status", type=str, choices=("Pending", "Paid", "Overdue"), required=False, help="Status must be 'Pending', 'Paid', or 'Overdue'")


# Fields for marshalling
fee_fields = {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "amount": fields.Float,
    "fee_type": fields.String,
    "semester": fields.String,
    "payment_date": fields.DateTime,
    "status": fields.String
}


# Fee Resource
class Fees(Resource):
    @marshal_with(fee_fields)
    def get(self):
        fees = FeeModel.query.all()
        if not fees:
            abort(404, message="Fees not found")
        404    
        return fees


    @marshal_with(fee_fields)
    def post(self):
        args = fee_args.parse_args()
        if args.get("payment_date"):
            args["payment_date"] = datetime.strptime(args["payment_date"], "%Y-%m-%d")
        fee = FeeModel(**args)
        db.session.add(fee)
        db.session.commit()
        return fee, 201
    

# Fee Resource by ID
class Fee(Resource):
    @marshal_with(fee_fields)
    def get(self, id):
        fee = FeeModel.query.get(id)
        if not fee:
            abort(404, message="Fee not found")
        return fee
    
    @marshal_with(fee_fields)
    def put(self, id):
        args = fee_args.parse_args()
        fee = FeeModel.query.get(id)
        if not fee:
            abort(404, message="Fee not found")
        for key, value in args.items():
            if key == "payment_date" and value:
                value = datetime.strptime(value, "%Y-%m-%d")
            setattr(fee, key, value)
        db.session.commit()
        return fee
    
    @marshal_with(fee_fields)
    def patch(self, id):
        args = fee_args.parse_args()
        fee = FeeModel.query.get(id)
        if not fee:
            abort(404, message="Fee not found")
        for key, value in args.items():
            if value is not None:
                setattr(fee, key, value)
        db.session.commit()
        return fee
    
    @marshal_with(fee_fields)
    def delete(self, id):
        fee = FeeModel.query.get(id)
        if not fee:
            abort(404, message="Fee not found")
        db.session.delete(fee)
        db.session.commit()
        return '', 204
