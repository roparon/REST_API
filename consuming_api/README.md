# REST API Consumer

This project is a simple Flask-based REST API consumer that interacts with the [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API. It provides endpoints to fetch posts, users, and user-specific posts.

## Features

- Fetch all posts.
- Fetch all users.
- Fetch details of a specific user.
- Fetch posts by a specific user.

## Project Structure
. ├── api.py # Main application file ├── requirement.txt # Python dependencies ├── .api/ # Virtual environment directory


## Endpoints

### 1. Home
**URL:** `/`  
**Method:** `GET`  
**Description:** Returns a welcome message.  

---

### 2. Get All Posts
**URL:** `/posts`  
**Method:** `GET`  
**Description:** Fetches all posts from the API.  
**Response:**
- `200 OK`: Returns a list of posts.
- `404 Not Found`: Returns an error message if no posts are found.

---

### 3. Get All Users
**URL:** `/users`  
**Method:** `GET`  
**Description:** Fetches all users from the API.  
**Response:**
- `200 OK`: Returns a list of users.
- `404 Not Found`: Returns an error message if no users are found.

---

### 4. Get User by ID
**URL:** `/users/<int:user_id>`  
**Method:** `GET`  
**Description:** Fetches details of a specific user by their ID.  
**Response:**
- `200 OK`: Returns user details.
- `404 Not Found`: Returns an error message if the user is not found.

---

### 5. Get Posts by User
**URL:** `/users/<int:user_id>/posts`  
**Method:** `GET`  
**Description:** Fetches posts created by a specific user.  
**Response:**
- `200 OK`: Returns a list of posts by the user.
- `404 Not Found`: Returns an error message if no posts are found for the user.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd REST_API

## 2. Create a virtual environment 
python3 -m venv .api
source .api/bin/activate  # On Windows, use `.api\Scripts\activate`

## 3. Install dependecies
pip install -r requirement.txt

## 4. Run application
python api.py

## 5. Access the application at http://127.0.0.1:5000.

# Dependencies
The project uses the following Python libraries:

Flask: Web framework for building the API.
requests: For making HTTP requests to the JSONPlaceholder API.
# API Reference
This project interacts with the JSONPlaceholder API, a free online REST API for testing and prototyping.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
JSONPlaceholder for providing a free API for testing.
Flask documentation for guidance on building REST APIs.