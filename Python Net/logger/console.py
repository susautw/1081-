import sys

from logger import Logger, LogType


class ConsoleLogger(Logger):

    def log(self, msg: str) -> None:
        if not LogType.is_enable(LogType.log, self._type):
            return
        print(msg)

    def info(self, msg: str) -> None:
        if not LogType.is_enable(LogType.info, self._type):
            return
        print(f'[INFO] {msg}')

    def debug(self, msg: str) -> None:
        if not LogType.is_enable(LogType.debug, self._type):
            return
        print(f'[DEBUG] {msg}')

    def error(self, msg: str) -> None:
        if not LogType.is_enable(LogType.error, self._type):
            return
        print(f'[ERROR] {msg}', file=sys.stderr)
