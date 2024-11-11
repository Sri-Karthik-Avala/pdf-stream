import streamlit as st
import socketio
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)

current_page = 1

@app.route('/')
def index():
    return "Backend running"

@sio.event
def connect():
    print("Client connected")

@sio.event
def change_page(data):
    global current_page
    current_page = data
    sio.emit("syncPage", {"page": current_page})

# Start Flask server with SocketIO
if __name__ == '__main__':
    app.run()

# Streamlit app
st.title('PDF Co-Viewer')
st.write('Use WebSockets to sync slides.')

# Add interactivity using Streamlit widgets (e.g., buttons for page navigation)
page = st.slider('Slide Page', min_value=1, max_value=100)
st.write(f"Current page: {page}")
