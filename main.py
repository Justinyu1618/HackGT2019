from networking import sio
from networking.delegate import NetworkingDelegate

class PongDelegate(NetworkingDelegate):

    def connected(self):
        print("connected!")
        pass

    def received_data(self, data):
        pass

    def disconnected(self):
        pass

d = PongDelegate()
sio.start(d)
