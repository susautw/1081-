import argparse
import socket
import threading
from pathlib import Path

from upload_server.ThreadingFileReceiver import ThreadingFileReceiver


def main():
    args = _arg_parser_factory().parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''  # all interfaces are available
    port = args.port
    backlog = args.backlog
    save = Path(args.save_to)
    sock.bind((host, port))
    sock.listen(backlog)

    complete = []
    while True:
        t = recv_client(sock, save)
        complete.append(t)
        join_completed(complete)


def recv_client(sock: socket.socket, save: Path) -> threading.Thread:
    client, address = sock.accept()
    print(f"connection established from {address}.")
    t = ThreadingFileReceiver(client, save)
    t.start()
    return t


def join_completed(complete):
    ThreadingFileReceiver.lock.acquire()
    for t in complete:
        if t.complete:
            t.join()
            print(f'{t.save_path} completed and release.')
    ThreadingFileReceiver.lock.release()


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8686)
    parser.add_argument('-b', '--backlog', type=int, default=10)
    parser.add_argument('-s', '--save_to', type=str, default='./download')
    return parser


if __name__ == '__main__':
    main()