from ap.extensions import db


#Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db. Column(db.String(80), unique=True, nullable=False)
    email = db. Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.username} {self.email}"
