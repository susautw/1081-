from abc import ABC, abstractmethod
import socket
from typing import Iterator, Optional

from coder import Coder


class Reader(ABC):
    @abstractmethod
    def read(self) -> Iterator[bytes]:
        pass

    def close(self):
        pass

class SocketReader(Reader):
    sock: socket.socket
    lines: Optional[Iterator[bytes]]
    coder: Coder

    def __init__(self, sock: socket.socket, coder: Coder):
        self.sock = sock
        self.lines = None
        self.coder = coder

    def _read_line(self) -> Iterator[bytes]:
        chunks = [b'']
        while not self._socket_is_closed():
            data = chunks[-1] + self.sock.recv(1024)
            chunks = data.split(b'\n')
            for chunk in chunks[:-1]:
                yield chunk

    def read(self) -> Iterator[bytes]:
        for line in self._read_line():
            yield self.coder.decode(line)

    def _socket_is_closed(self):
        return self.sock.__getattribute__('_closed')

    def close(self):
        self.sock.close()