import sys
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


PORT = 10
BUFFER_SIZE = 1024
WAIT_INTERVAL = 0.005  # 5 milliseconds

 
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

    def write(self, data):
        self.write_buf.appendleft(data)


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

    return client_socket


def write_handler(socket, buf):
    """
    sends data over bluetooth connection
    """
    while True:
        try:
            data = buf.pop()
            logging.debug("sending data : %s", data)
            socket.send(data)
        except IndexError:
            time.sleep(WAIT_INTERVAL)


def read_handler(socket, buf):
    """
    receives data over bluetooth connection
    """
    while True:
        data = socket.recv(BUFFER_SIZE)
        if not data:
            break
        logging.debug("receiving data : %s", data)
        buf.appendleft(data)
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
