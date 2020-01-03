import argparse
import json
import threading
import os
import socket
import time
from getpass import getpass
from pathlib import Path
from typing import Optional, TextIO

from chat_server.command import Login, Register, Logout, Create, Join, Leave, Close, Message, CommandInvoker
from coder import Base85Coder
from io_stream.reader import TCPReader, Reader
from io_stream.sender import TCPSender
from logger import ConsoleLogger


def main():
    args = _arg_parser_factory().parse_args()

    host = args.host
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    logger = ConsoleLogger()
    coder = Base85Coder()
    reader = TCPReader(sock, coder)
    sender = TCPSender(sock, coder)

    logger.info('Connected to chat server...')

    file = show_messages()
    msg_receiver = ThreadingMessageReceiver(file, reader)
    msg_receiver.start()

    closed = False

    while not closed and not sock.__getattribute__('_closed'):
        try:
            data = input('>> ')
            if data.startswith('/'):
                data = data[1:]

                if data == 'login':
                    command = _login()
                elif data == 'register':
                    command = _register()
                elif data == 'logout':
                    command = _logout()
                elif data == 'create':
                    command = _create()
                elif data == 'join':
                    command = _join()
                elif data == 'leave':
                    command = _leave()
                elif data == 'close':
                    command = _close()
                else:
                    logger.error('unknown command.')
                    raise Exception()
                msg_receiver.command(data)
            else:
                command = _message(data)
                msg_receiver.message(data)
                msg_receiver.command('message')

            invoker = CommandInvoker()
            invoker.store_command(command)

            request = invoker.serialize().encode()
            sender.send(request)
            if isinstance(command, Close):
                sock.close()

        except Exception as e:
            if str(e) != '':
                print(str(e))
                exit()


def show_messages():
    tmp_file_name = f'client_{time.time()}.tmp'
    os.system(f'start python -m chat_message_receiver {tmp_file_name}')
    return Path(tmp_file_name)


class ThreadingMessageReceiver(threading.Thread):
    file: Path
    reader: Reader

    lock: threading.Lock = threading.Lock()
    fp: Optional[TextIO]

    def __init__(self, file: Path, reader: Reader):
        super().__init__()
        self.file = file
        self.reader = reader
        self.fp = None

    def run(self):
        with self.file.open('w') as fp:
            self.fp = fp
            for line in self.reader.read():
                self._write(line.decode())
            self._write_close()

    def _write(self, msg: str):
        with self.lock:
            self.fp.write(msg)
            self.fp.flush()

    def _write_close(self):
        data = {
            'type': 'close'
        }
        self._write(json.dumps(data))

    def message(self, msg: str):
        data = {
            'type': 'reflex_message',
            'content': msg
        }
        self._write(json.dumps(data) + '\n')

    def command(self, command: str):
        data = {
            'type': 'executed_command',
            'command': command
        }
        self._write(json.dumps(data) + '\n')


def _login():
    username = input('username: ')
    password = getpass('password: ')

    command = Login()
    command.username = username
    command.password = password
    return command


def _register():
    username = input('username: ')
    password = getpass('password: ')

    command = Register()
    command.username = username
    command.password = password
    return command


def _logout():
    command = Logout()
    return command


def _create():
    name = input('Room name: ')

    command = Create()
    command.name = name
    return command


def _join():
    name = input('Room name: ')

    command = Join()
    command.name = name
    return command


def _leave():
    command = Leave()
    return command


def _close():
    command = Close()
    return command


def _message(message: str):
    command = Message()
    command.message = message
    return command


def _clear():
    os.system('cls || clear')


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str)
    parser.add_argument('-p', '--port', type=int, default=8526)
    return parser


if __name__ == '__main__':
    main()
