from app.extensions import db


#Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db. Column(db.String(80), unique=True, nullable=False)
    email = db. Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"{self.username} {self.email}"
