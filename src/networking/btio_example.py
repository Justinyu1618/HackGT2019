from btio import *


NAME = "rinik-T450s"
SOCKET_CLASS = "SERVER"


def connected_callback():
    print("CONNECTED CALLBACK")


def recv_data_callback(event, data):
    print("RECEIVED DATA CALLBACK: ", event)


if __name__ == "__main__":
    update_callbacks(conn=connected_callback, recv=recv_data_callback)
    bio, threads = socket_init(SOCKET_CLASS, name=NAME)

    bio.write("data",  "test1")
    bio.write("data",  "test2")
    bio.write("match", "test3")
    bio.write("match", "test4")

