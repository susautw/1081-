import socket
import threading
from abc import ABC, abstractmethod

from coder import Coder
from io_stream.sender import Sender, TCPSender, UDPSender
from io_stream.reader import Reader, TCPReader, UDPReader


class ThreadingEcho(threading.Thread, ABC):

    @abstractmethod
    def get_reader(self) -> Reader:
        pass

    @abstractmethod
    def get_sender(self) -> Sender:
        pass

    @abstractmethod
    def close(self):
        pass

    def run(self) -> None:
        while True:
            reader = self.get_reader()

            for line in reader.read():
                if line.startswith(b'msg:'):
                    sender = self.get_sender()
                    sender.send(line[4:])
                    break
            self.close()


class TCPThreadingEcho(ThreadingEcho):

    sock: socket.socket
    coder: Coder
    sender: Sender

    def __init__(self, sock: socket.socket, coder: Coder):
        super().__init__()
        self.sock = sock
        self.coder = coder

    def get_reader(self) -> Reader:
        client, _ = self.sock.accept()
        self.sender = TCPSender(client, self.coder)
        return TCPReader(client, self.coder)

    def get_sender(self) -> Sender:
        return self.sender

    def close(self):
        self.sender.close()


class UDPThreadingEcho(ThreadingEcho):
    sock: socket.socket
    coder: Coder
    reader: UDPReader

    def __init__(self, sock: socket.socket, coder: Coder):
        super().__init__()
        self.sock = sock
        self.coder = coder

    def get_reader(self) -> Reader:
        self.reader = UDPReader(self.sock, self.coder)
        return self.reader

    def get_sender(self) -> Sender:
        return UDPSender(self.sock, self.reader.last_client, self.coder)

    def close(self):
        pass
