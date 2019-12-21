from abc import ABC, abstractmethod

from patterns import Singleton


class LogType:
    log: int = 1
    info: int = 2
    debug: int = 4
    error: int = 8
    all: int = 15

    @staticmethod
    def is_enable(type_: int, unknown: int):
        return type_ & unknown != 0


class Logger(ABC, Singleton):
    _type: int = LogType.all

    @abstractmethod
    def log(self, msg: str) -> None:
        pass

    @abstractmethod
    def info(self, msg: str) -> None:
        pass

    @abstractmethod
    def debug(self, msg: str) -> None:
        pass

    @abstractmethod
    def error(self, msg: str) -> None:
        pass

    def disable_all(self):
        self._type = 0

    def disable(self, type_: int):
        self._type = self._type & LogType.all ^ type_

    def enable_all(self):
        self._type = LogType.all

    def enable(self, type_: int):
        self._type = self._type | type_

