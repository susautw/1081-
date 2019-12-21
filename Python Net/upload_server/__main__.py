import argparse
import socket
import threading
from pathlib import Path
from time import time

from logger import Logger, ConsoleLogger, LogType
from upload_server.server_thread import ThreadingFileReceiver


class Main:

    logger: Logger = ConsoleLogger()

    def main(self):
        args = self._arg_parser_factory().parse_args()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''  # all interfaces are available
        port = args.port
        backlog = args.backlog
        save = Path(args.save_to)
        sock.bind((host, port))
        sock.listen(backlog)

        self.logger.log(f'Server is on. port={port}')

        if args.debug:
            self.logger.debug('Debugging mode is on.')
        else:
            self.logger.disable(LogType.debug)

        while True:
            self.recv_client(sock, save)

    @staticmethod
    def recv_client(sock: socket.socket, save: Path) -> threading.Thread:
        client, address = sock.accept()
        Main.logger.info(f"connection established from {address}.")
        t = ThreadingFileReceiver(client, save / f'{time()}{address}', Main.logger)
        t.start()
        return t

    @staticmethod
    def _arg_parser_factory():
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', type=int, default=8686)
        parser.add_argument('-b', '--backlog', type=int, default=10)
        parser.add_argument('-s', '--save_to', type=str, default='./download')
        parser.add_argument('-d', '--debug', default=False, action='store_true')
        return parser


if __name__ == '__main__':
    Main().main()
