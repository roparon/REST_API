from app import app
from app.extensions import db





with app.app_context():
    db.create_all()
    print("Tables created succesfully")




if __name__ == "__main__":
    app.run(debug=True)