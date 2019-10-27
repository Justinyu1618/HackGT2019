from btio import *


NAME = "rinik-T450s"
SOCKET_CLASS = "SERVER"


def connected_callback():
    print("CONNECTED CALLBACK")


def recv_data_callback(event, data):
    print("RECEIVED DATA CALLBACK: ", event)


if __name__ == "__main__":
    bio = start(
        SOCKET_CLASS, 
        conn=connected_callback, 
        recv=recv_data_callback,
        name=NAME
    )

    bio.write("data",  "test1")
    bio.write("data",  "test2")
    bio.write("match", "test3")
    bio.write("match", "test4")

