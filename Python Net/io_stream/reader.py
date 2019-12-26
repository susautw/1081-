from abc import ABC, abstractmethod
import socket
from typing import Iterator, Optional, Tuple

from coder import Coder


class Reader(ABC):

    @abstractmethod
    def read(self) -> Iterator[bytes]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class AbstractReader(Reader):

    def read(self) -> Iterator[bytes]:
        for line in self._read_line():
            yield self._decode(line)

    def _read_line(self) -> Iterator[bytes]:
        chunks = [b'']
        while not self.closed():
            data = chunks[-1] + self._recv_data()
            chunks = data.split(b'\n')
            for chunk in chunks[:-1]:
                yield chunk

    @abstractmethod
    def closed(self) -> bool:
        pass

    @abstractmethod
    def _recv_data(self) -> bytes:
        pass

    @abstractmethod
    def _decode(self, data: bytes) -> bytes:
        pass


class TCPReader(AbstractReader):

    sock: socket.socket
    lines: Optional[Iterator[bytes]]
    coder: Coder
    chunk_size: int

    def __init__(self, sock: socket.socket, coder: Coder, chunk_size: int = 1024):
        self.sock = sock
        self.lines = None
        self.coder = coder
        self.chunk_size = chunk_size

    def _recv_data(self) -> bytes:
        return self.sock.recv(self.chunk_size)

    def _decode(self, data: bytes) -> bytes:
        return self.coder.decode(data)

    def closed(self):
        return self.sock.__getattribute__('_closed')

    def close(self) -> None:
        self.sock.close()


class UDPReader(AbstractReader):
    sock: socket.socket
    coder: Coder
    chunk_size: int
    last_client: Optional[Tuple[str, int]]

    def __init__(self, sock: socket.socket, coder: Coder, chunk_size: int = 1024):
        self.sock = sock
        self.coder = coder
        self.chunk_size = chunk_size
        self.last_client = None

    def _recv_data(self) -> bytes:
        data, self.last_client = self.sock.recvfrom(self.chunk_size)
        return data

    def _decode(self, data: bytes) -> bytes:
        return self.coder.decode(data)

    def closed(self) -> bool:
        return self.sock.__getattribute__('_closed')

    def close(self) -> None:
        self.sock.close()

