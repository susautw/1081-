import json
import socket
import threading

from chat_server.client_handler import ClientHandler
from chat_server.command import CommandInvoker
from chat_server.error import DescribedException
from coder import Coder
from io_stream.reader import Reader, TCPReader
from io_stream.sender import Sender, TCPSender
from logger import Logger


class ServerThread(threading.Thread):

    sock: socket.socket
    _reader: Reader
    _sender: Sender
    _coder: Coder
    logger: Logger

    def __init__(self, sock: socket.socket, coder: Coder, logger: Logger):
        super().__init__()
        self.sock = sock
        self._coder = coder
        self.logger = logger

    def run(self):
        self._reader = TCPReader(self.sock, self._coder)
        self._sender = TCPSender(self.sock, self._coder)

        client_handler = ClientHandler(self._sender, self.logger)
        for line in self._reader.read():
            try:
                invoker = CommandInvoker()
                invoker.set_receiver(client_handler)
                invoker.unserialize(line.decode())
                invoker.send_all()
            except DescribedException as e:
                msg = str(e)
                response = {
                    'type': 'report',
                    'status': 'error',
                    'describe': e.describe(),
                    'message': msg
                }
                self._sender.send(json.dumps(response).encode())
