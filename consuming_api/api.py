from flask import Flask, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the API!"

API_URL = "https://jsonplaceholder.typicode.com"


# Routes for getting posts
@app.route('/posts')
def get_posts():
    response = requests.get(f'{API_URL}/posts')
    if response.status_code != 200:
        return jsonify({"error": "No posts found!"}), 404
    return jsonify(response.json())

# Routes for getting users
@app.route('/users')
def get_users():
    response = requests.get(f'{API_URL}/users')
    if response.status_code != 200:
        return jsonify({"error": "No users found!"}), 404
    return jsonify(response.json())

#Getting individual user
@app.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    response = requests.get(f'{API_URL}/users/{user_id}')
    if response.status_code != 200:
        return jsonify({'error': 'User not found'})
    return jsonify(response.json())

#Getting posts by user
@app.route('/users/<int:user_id>/posts')
def user_posts(user_id):
    response = requests.get(f'{API_URL}/users/{user_id}/posts')
    if response.status_code != 200:
        return jsonify({'error': 'No posts for the given user!'})
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)