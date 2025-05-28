from flask_restful import Resource
from flask import request

class ChatResource(Resource):
    def post(self):
        user_input = request.json.get('message', '').strip().lower()
        if not user_input:
            return {'response': "Please say something!"}
        # Simple rule-based responses
        if any(greet in user_input for greet in ['hello', 'hi', 'hey']):
            return {'response': "Hello! How can I help you today?"}
        elif any(bye in user_input for bye in ['bye', 'goodbye', 'see you']):
            return {'response': "Goodbye! Have a great day!"}
        elif 'help' in user_input:
            return {'response': "I'm here to help! Ask me anything about this app."}
        else:
            return {'response': f"I'm not sure how to respond to '{user_input}'. Try asking something else!"}
