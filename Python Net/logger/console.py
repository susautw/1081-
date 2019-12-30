import sys
from threading import Lock

from logger import Logger, LogType
from patterns import Singleton


class ConsoleLogger(Logger, Singleton):

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


class ThreadSafeConsoleLogger(Logger, Singleton):

    _lock: Lock = Lock()

    def log(self, msg: str) -> None:
        if not LogType.is_enable(LogType.log, self._type):
            return
        self._show(msg)

    def info(self, msg: str) -> None:
        if not LogType.is_enable(LogType.info, self._type):
            return
        self._show(f'[INFO] {msg}')

    def debug(self, msg: str) -> None:
        if not LogType.is_enable(LogType.debug, self._type):
            return
        self._show(f'[DEBUG] {msg}')

    def error(self, msg: str) -> None:
        if not LogType.is_enable(LogType.error, self._type):
            return
        self._show(f'[ERROR] {msg}', file=sys.stderr)

    def _show(self, msg: str, file=sys.stdout):
        with self._lock:
            print(msg, file=file)
