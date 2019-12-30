from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, List

from chat_server.error import NoDataFound


class Model(ABC):
    model_name: str

    @abstractmethod
    def store(self) -> None:
        pass


class User(Model):
    users: Dict[str, 'User'] = {}
    _users_lock = Lock()

    model_name: 'str' = 'user'

    _username: str
    _password: str

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    def store(self) -> None:
        with self._users_lock:
            self.users[self.username] = self

    @staticmethod
    def find(username: str):
        user = User.users.get(username, None)
        if user is None:
            raise NoDataFound(User)
        return user

    @staticmethod
    def has_user(username: str):
        user = User.users.get(username, None)
        return user is not None


class Room(Model):
    rooms: Dict[str, 'Room'] = {}
    _rooms_lock = Lock()
    model_name: str = 'room'

    _name: str
    _users: List[User]

    def __init__(self, name: str):
        self._name = name
        self._users = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def users(self) -> List[User]:
        return self._users

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        self.users.remove(user)

    def store(self) -> None:
        with self._rooms_lock:
            self.rooms[self.name] = self

    def delete(self) -> None:
        with self._rooms_lock:
            self.rooms.pop(self.name)

    @staticmethod
    def find(name: str):
        room = Room.rooms.get(name, None)
        if room is None:
            raise NoDataFound(Room)
        return room

    @staticmethod
    def has_room(name: str):
        room = Room.rooms.get(name, None)
        return room is not None
