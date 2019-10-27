import socketio
import sys
import threading

sio = socketio.Client()

@sio.event
def connect():
    print("connected")

@sio.on("data")
def received_data(data):
    print(data)

@sio.event
def disconnect():
    print("disconnected")

def start_server():
    sio.connect("http://137.135.122.22:5000")
    sio.emit("match", {"code": sys.argv[1], "status": "join_match", "size": 50})
    sio.wait()

t = threading.Thread(target=start_server)
t.start()
