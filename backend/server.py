from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, disconnect
from models import db_session, Message
from models import Base, engine
from flask_socketio import SocketIO, join_room
from datetime import datetime
import sqlite3
import clear

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
socketio = SocketIO(app)
clear.clear()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@socketio.on('join', namespace='/chat')
def join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(f'{username} se ha unido a la sala {room}')

@socketio.on('message', namespace='/chat')
def chat_message(data):
    username = data['username']
    room = data['room']
    message = data['message']

    if message == 'QUIT':
        leave_room(room)
        print(f'{username} ha dejado la sala {room}')
    elif message == 'EXIT':
        disconnect()
        print(f'{username} se desconectó del servidor')
    else:
        new_message = Message(username=username, message=message, room=room)
        db_session.add(new_message)
        db_session.commit()
        socketio.emit('message', data, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    timestamp = datetime.now()
    insert_message(username, message, room, timestamp)

@socketio.on('leave', namespace='/chat')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(f'{username} ha dejado la sala {room}')

def insert_message(username, message, room, timestamp):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (username, message, room, timestamp) VALUES (?, ?, ?, ?)", (username, message, room, timestamp))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    socketio.run(app, debug=True)