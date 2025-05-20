from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Welcome to RESTful API</h1>'

if __name__ == "__main__":
    app.run(debug=True)