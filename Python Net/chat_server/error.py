from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from chat_server.models import Model


class DescribedException(ABC, Exception):
    @abstractmethod
    def describe(self) -> str:
        pass


class IllegalOperation(DescribedException):
    def __init__(self):
        super().__init__("Illegal operation.")

    def describe(self) -> str:
        return self.__class__.__name__


class NoDataFound(DescribedException):
    def __init__(self, model: Type['Model']):
        super().__init__(f'can\'t find data in model: {model.model_name})')

    def describe(self) -> str:
        return self.__class__.__name__


class UserAlreadyExists(DescribedException):
    def __init__(self, username: str):
        super().__init__(f'the user {username} has registered.')

    def describe(self) -> str:
        return self.__class__.__name__


class UserNotExists(DescribedException):
    def __init__(self, username: str):
        super().__init__(f'the user {username} not exists.')

    def describe(self) -> str:
        return self.__class__.__name__


class IncorrectPassword(DescribedException):
    def __init__(self):
        super().__init__(f'incorrect password')

    def describe(self) -> str:
        return self.__class__.__name__


class RoomAlreadyExists(DescribedException):
    def __init__(self, name: str):
        super().__init__(f'the room {name} has existed.')

    def describe(self) -> str:
        return self.__class__.__name__


class RoomNotExists(DescribedException):
    def __init__(self, name: str):
        super().__init__(f'the room {name} not exists.')

    def describe(self) -> str:
        return self.__class__.__name__
