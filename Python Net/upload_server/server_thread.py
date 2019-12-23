import threading
from pathlib import Path
from socket import socket
from typing import Tuple

from coder import Coder, Base85Coder
from io_stream.reader import TCPReader
from io_stream.sender import TCPSender
from logger import Logger
from upload_server.error import UnknownCommand
from upload_server.file_receiver import FileReceiver


class ThreadingFileReceiver(threading.Thread):
    client: socket
    save_path: Path
    coder: Coder = Base85Coder()
    logger: Logger

    def __init__(self, client: socket, save_path: Path, logger: Logger):
        super().__init__()
        self.client = client
        self.save_path = save_path
        self.reader = TCPReader(self.client, self.coder)
        self.sender = TCPSender(self.client, self.coder)
        self.logger = logger

    def run(self):
        self.logger.info(f'Starting to receive files from the client.')
        file_receiver = FileReceiver()
        try:
            for line in self.reader.read():
                command, arg = self._get_command(line)

                if command == b'file':
                    filename = arg.decode()
                    file_path = self.save_path / Path(filename)
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_receiver.new_file(file_path)
                    self.logger.info(f'Starting to receive new file {filename}')
                elif command == b'chunk':
                    chunk = arg
                    file_receiver.recv_chunk(chunk)
                    self.logger.debug(f'Received chunk of file.({len(chunk)} bytes)')
                elif command == b'close':
                    break
                else:
                    raise UnknownCommand(command)

            # no error occurred.
            self.sender.send(b'ok')
            self.logger.info('All file transmission has been done.')

        except Exception as e:
            msg = str(e)
            self._send_error(msg)
            self.logger.error(msg)

        finally:
            file_receiver.close()
            self.client.close()
            self.logger.info('Closed the connection.\n')

    def _send_error(self, message):
        self.sender.send(b'error ' + message.encode())

    @staticmethod
    def _get_command(line: bytes) -> Tuple[bytes, bytes]:
        sp = line.index(b' ')
        command = line[:sp]
        arg = line[sp + 1:]
        return command, arg
