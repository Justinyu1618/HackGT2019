from abc import ABC, abstractmethod

class NetworkingDelegate(ABC):

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def received_data(self, name, data):
        pass

    @abstractmethod
    def disconnected(self):
        pass
