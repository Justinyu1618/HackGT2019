import time
import random

from btio import socket_init


NAME = "rinik-T450s"
SOCKET_CLASS = "CLIENT"


if __name__ == "__main__":
    bio, threads = socket_init(SOCKET_CLASS, name=NAME)

    # start threads
    for t in threads:
        t.start()

    print("starting write tests")
    for i in range(5):
        time_itrv = random.randint(50, 2000)
        bio.write(SOCKET_CLASS + ": " + str(i))
        time.sleep(time_itrv / 1000)

    print("starting read tests")
    for i in range(5):
        time_itrv = random.randint(50, 2000)
        print(bio.read())
        time.sleep(time_itrv / 1000)

