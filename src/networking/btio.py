import sys
import json
import time
import logging
import threading
import collections

from bluetooth import (
    BluetoothSocket,
    discover_devices,
    lookup_name,
    RFCOMM
)

import random
logging.basicConfig(level=logging.DEBUG)


# constants
PORT = 10
BUFFER_SIZE = 1024
WAIT_INTERVAL = 0.005  # 5 milliseconds


# callback functions
connected_callback = None
recv_data_callback = None

 
class BluetoothIO:
    def __init__(self, read_buf, write_buf):
        self.read_buf = read_buf
        self.write_buf = write_buf

    def read(self):
        try:
            data = self.read_buf.pop()
            return data
        except IndexError:
            return

    def write(self, event, data):
        # create a json w/ event + data information
        message = { "event": event, "data": data }
        message = json.dumps(message)
        self.write_buf.appendleft(message)


def update_callbacks(conn=None, recv=None):
    global connected_callback, recv_data_callback

    connected_callback = conn
    recv_data_callback = recv


def server_init():
    """
    initialize server socket
    """
    logging.debug("server initialization")
    server_socket = BluetoothSocket(RFCOMM)
    server_socket.bind(("", PORT))
    server_socket.listen(1)

    return server_socket


def client_init(server_name):
    """
    initialize client socket
    """
    logging.debug("client initialization")
    
    server_address = None

    devices = discover_devices()
    for device_address in devices:
        device_name = lookup_name(device_address)
        logging.debug("found device : %s", device_name)

        if device_name == server_name:
            server_address = device_address
            break

    if server_address is None:
        logging.error("could not connect to %s", server_name)
        sys.exit(0)

    client_socket = BluetoothSocket(RFCOMM)
    client_socket.connect((server_address, PORT))
    
    # handle callback function
    if connected_callback is not None:
        connected_callback()

    return client_socket


def write_handler(socket, buf):
    """
    sends data over bluetooth connection
    """
    while True:
        try:
            message = buf.pop()
            logging.debug("sending data : %s", message)
            socket.send(message)
        except IndexError:
            time.sleep(WAIT_INTERVAL)


def read_handler(socket, buf):
    """
    receives data over bluetooth connection
    """
    while True:
        message = socket.recv(BUFFER_SIZE)
        if not message:
            break
        logging.debug("receiving data : %s", message)

        try:
            message = json.loads(message)
        except JSONDecodeError:
            logging.error("message must be json serialized")

        # handle callback functions
        if data_callback is not None:
            event = message["event"]
            data = message["data"]
            recv_data_callback(event, data)

        buf.appendleft(message)
    socket.close()


def socket_init(socket_class, name=None):
    """
    initializes server/client sockets
    socket_class = SERVER or CLIENT
    returns:
        bio     | BluetoothIO object (read/write)
        threads | threading objects
    """
    # initialize sockets
    if socket_class == "SERVER":
        server_socket = server_init()
        socket, address = server_socket.accept()

    if socket_class == "CLIENT":
        socket = client_init(name)
    
    # initialize buffers
    write_buf = collections.deque()
    read_buf = collections.deque()
    bio = BluetoothIO(read_buf, write_buf)
    
    # initialize threads
    threads = [
        threading.Thread(target=write_handler, kwargs=dict(
            socket=socket,
            buf=write_buf
        )),
        threading.Thread(target=read_handler, kwargs=dict(
            socket=socket,
            buf=read_buf
        ))
    ]

    return bio, threads 
