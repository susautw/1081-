from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Serializable(ABC):

    @abstractmethod
    def serialize(self) -> bytes:
        pass

    @abstractmethod
    def unserialize(self, serialized: bytes):
        pass
