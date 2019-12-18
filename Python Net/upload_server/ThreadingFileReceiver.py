import json
import threading
from base64 import b64decode
from pathlib import Path
from socket import socket
from stream.line_reader import SocketReader


class ThreadingFileReceiver(threading.Thread):
    client: socket
    save_path: Path
    lock = threading.Lock()
    complete = False

    def __init__(self, client: socket, save_path: Path):
        super().__init__()
        self.client = client
        self.save_path = save_path

    def run(self):
        reader = SocketReader(self.client)
        lines = reader.read_line()
        for line in lines:
            print(line)
            if line.startswith(b'd:'):
                print(b64decode(line[2:]).decode())

    # def old_run(self):
        # try:
        #     data = self.client.recv(4096)
        #     first = data.index(b'\n')
        #     filename = data[:first]
        #     data = data[first + 1:]
        #     save_path = self.save_path / filename.decode()
        #     save_path.parent.mkdir(parents=True, exist_ok=True)
        #     data = b''
        #     tmp = self.client.recv(1024)
        #     while tmp:
        #         data += tmp
        #         tmp = self.client.recv(1024)
        #         if data.endswith(b'\n\n'):
        #             break
        #         with open(str(save_path), '+wb') as f:
        #             f.write(json.load(data[0:-2].decode()).encode())
        #
        #     self.client.sendall(b'OK')
        # except:
        #     self.client.sendall(b'ERROR')
        #
        # self.client.close()
        # self._complete()

    def _complete(self):
        self.lock.acquire()
        self.complete = True
        self.lock.release()
