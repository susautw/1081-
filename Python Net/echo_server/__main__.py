import argparse
import socket

from coder import Base85Coder
from echo_client.threading_echo import TCPThreadingEcho, UDPThreadingEcho


def main():
    args = _arg_parser_factory().parse_args()

    port = args.port

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', port))
    tcp.listen(100)

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('', port))

    coder = Base85Coder()

    tcp_echo = TCPThreadingEcho(tcp, coder)
    udp_echo = UDPThreadingEcho(udp, coder)
    tcp_echo.start()
    udp_echo.start()


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7086)
    return parser


if __name__ == '__main__':
    main()
