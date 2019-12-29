from abc import ABC, abstractmethod


class Model(ABC):

    @abstractmethod
    def store(self) -> None:
        pass


class User(Model):
    def store(self) -> None:
        pass


class Room(Model):
    def store(self) -> None:
        pass
