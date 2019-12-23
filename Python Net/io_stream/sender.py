import socket
from abc import abstractmethod, ABC
from typing import Tuple

from coder import Coder


class Sender(ABC):

    @abstractmethod
    def send(self, data: bytes):
        pass

    def close(self):
        pass


class TCPSender(Sender):

    sock: socket.socket
    coder: Coder

    def __init__(self, sock: socket.socket, coder: Coder):
        self.sock = sock
        self.coder = coder

    def send(self, data: bytes):
        self.sock.sendall(self.coder.encode(data) + b'\n')

    def close(self):
        self.sock.close()


class UDPSender(Sender):
    sock: socket.socket
    address: Tuple[str, int]
    coder: Coder

    def __init__(self, sock: socket.socket, address: Tuple[str, int], coder: Coder):
        self.sock = sock
        self.address = address
        self.coder = coder

    def send(self, data: bytes):
        self.sock.sendto(self.coder.encode(data), self.address)
