import socket
from abc import ABC, abstractmethod
from io import BufferedWriter
from pathlib import Path

from patterns import Singleton
from upload_server.error import ReceivedChunkButNoFileSpecified, TransportInterrupted


class FileReceiver:

    _file: BufferedWriter
    _file_path: Path
    _chunk: bytes

    state: 'FileReceiverState'
    sock: socket.socket

    def __init__(self):
        self.state = Stopped()

    @property
    def file(self) -> BufferedWriter:
        return self._file

    @file.setter
    def file(self, file: BufferedWriter) -> None:
        self._file = file

    @property
    def file_path(self):
        return self._file_path

    @property
    def chunk(self):
        return self._chunk

    def new_file(self, filepath: Path) -> None:
        """
        Starting to receive a new file
        """
        self._file_path = filepath
        self.state.new_file(self)

    def recv_chunk(self, chunk: bytes) -> None:
        """
        Receive a chunk of the file.
        """
        self._chunk = chunk
        self.state.recv_chunk(self)

    def close(self) -> None:
        """
        Release all of holding file resource.
        """
        self.file.close()
        self.state.close(self)


class FileReceiverState(ABC, Singleton):
    @abstractmethod
    def new_file(self, ctx: FileReceiver):
        pass

    @abstractmethod
    def recv_chunk(self, ctx: FileReceiver):
        pass

    @abstractmethod
    def close(self, ctx: FileReceiver):
        pass


class Stopped(FileReceiverState):
    def new_file(self, ctx: FileReceiver):
        ctx.file = ctx.file_path.open('wb')
        ctx.state = Receiving()

    def recv_chunk(self, ctx: FileReceiver):
        ctx.state = Closed()
        raise ReceivedChunkButNoFileSpecified(ctx.chunk)

    def close(self, ctx: FileReceiver):
        ctx.state = Closed()


class Receiving(FileReceiverState):

    def new_file(self, ctx: FileReceiver):
        ctx.state = Closed()
        raise TransportInterrupted(ctx.file_path)

    def recv_chunk(self, ctx: FileReceiver):
        if self._is_empty_chunk(ctx.chunk):
            ctx.file.close()
            ctx.state = Stopped()
        else:
            ctx.file.write(ctx.chunk)

    def close(self, ctx: FileReceiver):
        ctx.state = Closed()
        raise TransportInterrupted(ctx.file_path)

    @staticmethod
    def _is_empty_chunk(chunk: bytes):
        return len(chunk) == 0


class Closed(FileReceiverState):
    def new_file(self, ctx: FileReceiver):
        pass

    def recv_chunk(self, ctx: FileReceiver):
        pass

    def close(self, ctx: FileReceiver):
        pass
