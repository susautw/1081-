import argparse
import socket

from chat_server.server_thread import ServerThread
from coder import Base85Coder
from logger import ThreadSafeConsoleLogger


class Main:
    @staticmethod
    def main() -> None:
        args = Main._arg_parser_factory().parse_args()

        port = args.port
        backlog = args.backlog

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', port))
        sock.listen(backlog)

        coder = Base85Coder()
        logger = ThreadSafeConsoleLogger()

        logger.info('Server is on...')
        while True:
            client, addr = sock.accept()
            logger.info(f'client connected: {addr}')
            ServerThread(client, coder, logger).start()

    @staticmethod
    def _arg_parser_factory() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', type=int, default=8526)
        parser.add_argument('-b', '--backlog', type=int, default=500)
        return parser


if __name__ == '__main__':
    Main.main()
