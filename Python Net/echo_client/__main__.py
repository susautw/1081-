import argparse
import socket

from coder import Base85Coder
from io_stream.reader import UDPReader, TCPReader
from io_stream.sender import UDPSender, TCPSender
from logger import ConsoleLogger


def main():
    args = _arg_parser_factory().parse_args()

    msg: str = args.msg
    use_udp: bool = args.udp
    host: str = args.host
    port: int = args.port

    coder = Base85Coder()
    logger = ConsoleLogger()

    # create socket
    if use_udp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender = UDPSender(sock, (host, port), coder)
        reader = UDPReader(sock, coder)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender = TCPSender(sock, coder)
        reader = TCPReader(sock, coder)

    sender.send(msg.encode())

    for line in reader.read():
        logger.log(line.decode())


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('msg', type=str)
    parser.add_argument('host', type=str)
    parser.add_argument('-p', '--port', type=int, default=7086)
    parser.add_argument('-u', '--udp', type=bool, action='store_true')
    return parser


if __name__ == '__main__':
    main()