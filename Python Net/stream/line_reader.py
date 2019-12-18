from abc import ABC, abstractmethod
import socket
from typing import Iterator


class LineReader(ABC):
    @abstractmethod
    def read_line(self) -> Iterator[bytes]:
        pass


class SocketReader(LineReader):
    sock: socket.socket

    def __init__(self, sock: socket.socket):
        self.sock = sock

    def read_line(self) -> Iterator[bytes]:
        data = self.sock.recv(1024)
        while data != b'':
            chunks = data.split(b'\n')
            for chunk in chunks[:-1]:
                yield chunk

            data = chunks[-1] + self.sock.recv(1024)
