import socket
from abc import abstractmethod, ABC
from typing import Tuple

from coder import Coder


class Sender(ABC):

    @abstractmethod
    def send(self, data: bytes):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def is_closed(self) -> bool:
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

    def is_closed(self) -> bool:
        if self.sock.__getattribute__('_closed'):
            return True
        try:
            self.sock.send(b'')
            return False
        except ConnectionError as e:
            self.sock.close()
            return True


class UDPSender(Sender):
    sock: socket.socket
    address: Tuple[str, int]
    coder: Coder

    def __init__(self, sock: socket.socket, address: Tuple[str, int], coder: Coder):
        self.sock = sock
        self.address = address
        self.coder = coder

    def send(self, data: bytes):
        self.sock.sendto(self.coder.encode(data) + b'\n', self.address)

    def is_closed(self) -> bool:
        return self.sock.__getattribute__('_closed')

    def close(self):
        pass
