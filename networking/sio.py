import socketio
import threading

SOCKETIO_IP = "137.135.122.22"
SOCKETIO_PORT = 5000

sio = socketio.Client()

connected_callback = None
received_data_callback = None
disconnected_callback = None

@sio.event
def connect():
    if connected_callback is not None:
        connected_callback()

@sio.on("data")
def received_data(data):
    if received_data_callback is not None:
        received_data_callback("data", data)

@sio.on("info")
def received_info(data):
    if received_data_callback is not None:
        received_data_callback("info", data)

@sio.on("match")
def received_match(data):
    if received_data_callback is not None:
        received_data_callback("match", data)

@sio.on("disconnected")
def user_disconnected(data):
    if received_data_callback is not None:
        received_data_callback("disconnected", data)

def start_server():
    sio.connect("http://{}:{}".format(SOCKETIO_IP, SOCKETIO_PORT))
    sio.wait()

def emit(name, data):
    sio.emit(name, data)

def update_callbacks(conn=None, recv=None, disc=None):
    global connected_callback, received_data_callback, disconnected_callback

    connected_callback = conn
    received_data_callback = recv
    disconnected_callback = disc

def start(conn=None, recv=None, disc=None):
    update_callbacks(conn, recv, disc)

    t = threading.Thread(target=start_server)
    t.start()
