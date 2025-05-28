import unittest
from app import app, db
from app.models import User, Role
from flask_security.utils import hash_password

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Set up the database
        with app.app_context():
            db.create_all()
            user_role = Role(name='user')
            db.session.add(user_role)
            db.session.commit()
            test_user = User(email='test@example.com', password=hash_password('testpass'))
            test_user.roles.append(user_role)
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        # Clean up after tests
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_login_logout(self):
        # Register
        response = self.app.post('/register', data=dict(email='newuser@example.com', password='newpass', password_confirm='newpass'), follow_redirects=True)
        self.assertIn(b'Hello, newuser@example.com', response.data)
        # Logout
        self.logout()
        # Login
        response = self.login('newuser@example.com', 'newpass')
        self.assertIn(b'Hello, newuser@example.com', response.data)

    def test_chatbot_api_authenticated(self):
        self.login('test@example.com', 'testpass')
        response = self.app.post('/api/chat', json={'message': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello! How can I help you today?', response.data)

    def test_chatbot_api_unauthenticated(self):
        response = self.app.post('/api/chat', json={'message': 'hello'})
        # Should still work if API is public, else check for 401/redirect
        self.assertEqual(response.status_code, 200)

    def test_chatbot_rule_based(self):
        self.login('test@example.com', 'testpass')
        # Greeting
        res = self.app.post('/api/chat', json={'message': 'hi'})
        self.assertIn(b'Hello! How can I help you today?', res.data)
        # Farewell
        res = self.app.post('/api/chat', json={'message': 'bye'})
        self.assertIn(b'Goodbye! Have a great day!', res.data)
        # Help
        res = self.app.post('/api/chat', json={'message': 'help'})
        self.assertIn(b"I'm here to help! Ask me anything about this app.", res.data)
        # Unknown
        res = self.app.post('/api/chat', json={'message': 'foobar'})
        self.assertIn(b"I'm not sure how to respond to 'foobar'", res.data)