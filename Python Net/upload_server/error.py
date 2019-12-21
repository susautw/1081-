from pathlib import Path


class UnknownCommand(Exception):
    def __init__(self, command):
        super().__init__(f'Received a Unknown command: {str(command)}')


class TransportInterrupted(Exception):
    def __init__(self, filepath: Path):
        super().__init__(f'Transmission of {str(filepath)} file is interrupted.')


class ReceivedChunkButNoFileSpecified(Exception):
    def __init__(self, chunk: bytes):
        super().__init__(f'Received part as length {len(chunk)} but no file specified.')
