from abc import ABC, abstractmethod

from patterns import Singleton


class Coder(ABC, Singleton):

    @abstractmethod
    def encode(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> bytes:
        pass
