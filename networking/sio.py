import asyncio
import socketio
import threading


SOCKETIO_IP = "137.135.122.22"
SOCKETIO_PORT = 5000

sio = socketio.Client()

connected = False
delegate = None

@sio.event
def connect():
    connected = True
    delegate.connected()

@sio.on("data")
def received_data(data):
    if delegate.received_data is not None:
        delegate.received_data("data", data)

@sio.on("match")
def received_match(data):
    if delegate.received_data is not None:
        delegate.received_data("match", data)

@sio.event
def disconnect():
    connected = False
    delegate.disconnected()

def start_server():
    sio.connect("http://{}:{}".format(SOCKETIO_IP, SOCKETIO_PORT))
    sio.wait()

def emit(name, data):
    sio.emit(name, data)

def update_delegate(d):
    global delegate
    delegate = d

def start(d):
    global delegate
    delegate = d

    t = threading.Thread(target=start_server)
    t.start()
