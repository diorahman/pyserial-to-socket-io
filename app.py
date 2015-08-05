from gevent import monkey
monkey.patch_all()

import serial
import time
from threading import Thread
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hihihihi'
socketio = SocketIO(app)
thread = None

port = '/dev/ttyS0'
ser = serial.Serial(port, 115200, timeout=0)

def background_thread():
    while True:
        data = ser.read(9999)
        if len(data) > 0:
            socketio.emit('message', {'data': data}, namespace='/test')
    ser.close()

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])

@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])

if __name__ == '__main__':
    socketio.run(app)
