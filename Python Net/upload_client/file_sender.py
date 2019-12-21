from pathlib import Path

from io_stream.sender import Sender


class FileSender:
    sender: Sender
    chunk_size: int

    def __init__(self, sender: Sender, chunk_size: int = 1024):
        self.sender = sender
        self.chunk_size = chunk_size

    def send_file(self, file: Path, base_path: Path):
        """
        Send a file to the server chunk by chunk
        """
        if not file.exists():
            raise FileNotFoundError(f'File {str(file.absolute())} is not exists.')

        self._send_filename(file.relative_to(base_path))

        with file.open('rb') as f:
            eof = b''
            chunk = None
            while chunk != eof:
                if chunk is not None:
                    self._send_chunk(chunk)
                chunk = f.read(self.chunk_size)

        self._send_eof()

    def _send_filename(self, file: Path):
        self.sender.send(b'file %b' % file.as_posix().encode())

    def _send_chunk(self, chunk: bytes):
        self.sender.send(b'chunk ' + chunk)

    def _send_eof(self):
        self.sender.send(b'chunk ')

    def close(self):
        """
        Tell the server all file delivery is done.
        """
        self.sender.send(b'close ')
