from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables (such as database URI)
load_dotenv()

# Database configuration (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the ChatHistory model to store question-answer pairs
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ChatHistory {self.question}>'

# Define the route to save the chat history (question and answer) into the database
@app.route('/api/save-chat', methods=['POST'])
def save_chat():
    data = request.get_json()

    # Extract question and answer from the incoming request
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        return jsonify({'error': 'Question and answer are required'}), 400

    # Save the question and answer to the database
    new_chat = ChatHistory(question=question, answer=answer)
    db.session.add(new_chat)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Chat saved successfully'})

# Define the route to get chat history from the database
@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    # Retrieve all chat history from the database
    chats = ChatHistory.query.all()
    chat_data = [{'question': chat.question, 'answer': chat.answer} for chat in chats]
    return jsonify({'messages': chat_data})

# Main entry point for the Flask app
if __name__ == '__main__':
    # Create the database tables if they don't exist
    db.create_all()

    # Run the app
    app.run(debug=True)
