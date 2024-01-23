from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Define the file to store chat messages
CHAT_FILE = 'chat_messages.txt'

# Try to load existing chat messages from file, or create an empty list if the file doesn't exist
try:
    with open(CHAT_FILE, 'r') as file:
        messages = json.load(file)
except FileNotFoundError:
    messages = []

# Define the route for the main page
@app.route('/')
def index():
    return render_template('index.html', messages=messages)

# Define the SocketIO event handler for receiving messages
@socketio.on('message')
def handle_message(data):
    # Append the new message to the list of messages
    messages.append(data)
    
    # Save the updated list of messages to the file
    with open(CHAT_FILE, 'w') as file:
        json.dump(messages, file)
    
    # Broadcast the updated list of messages to all connected clients
    socketio.emit('update_chat', messages)

# Run the app with SocketIO support
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
