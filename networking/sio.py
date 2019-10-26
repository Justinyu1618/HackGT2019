import asyncio
import socketio
import threading

SOCKETIO_IP = "137.135.122.22"
SOCKETIO_PORT = 5000

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

connected = False
delegate = None

@sio.event
async def connect():
    connected = True
    delegate.connected()

@sio.on("data")
async def received_data(data):
    delegate.received_data(data)

@sio.event
async def disconnect():
    connected = False
    delegate.disconnected()

async def start_server():
    await sio.connect("http://{}:{}".format(SOCKETIO_IP, SOCKETIO_PORT))
    await sio.wait()

def main(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())

def start(d):
    global delegate
    delegate = d

    t = threading.Thread(target=main, args=(loop,))
    t.start()
