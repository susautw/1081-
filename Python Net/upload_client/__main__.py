import argparse
import json
from base64 import b64encode
from pathlib import Path
import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    args = _arg_parser_factory().parse_args()
    filepath = Path(args.file)

    host = args.host
    port = args.port

    sock.connect((host, port))

    sock.sendall((filepath.name + '\n').encode())
    print('transport started...')
    data = b''
    with open(str(filepath), 'rb') as f:
        tmp = f.read(1024)
        while tmp:
            data += tmp
            tmp = f.read(1024)

        sock.sendall(b'd:' + b64encode(data))
    sock.sendall(b'\n\n')
    data = sock.recv(1024)
    if data == b'OK':
        print(f'file {str(filepath)} saved to {host}')
    else:
        print(f'file {str(filepath)} failed to save')
    sock.close()


def _recv_data_and_encode(f):
    return json.dumps(f.read(1024).decode()).encode()


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('host', type=str)
    parser.add_argument('-p', '--port', type=int, default=8686)
    return parser


if __name__ == '__main__':
    main()
