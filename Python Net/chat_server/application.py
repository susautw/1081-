from abc import ABC, abstractmethod

from chat_server.error import IllegalOperation
from io_stream.reader import Reader
from io_stream.sender import Sender
from patterns import Singleton


class Application:

    _state: 'ApplicationState'
    _sender: Sender
    _reader: Reader

    # User related
    username: str
    password: str

    # Room related
    name: str

    # Message related
    message: str

    def __init__(self, sender: Sender, reader: Reader):
        self._state = Waiting()
        self._sender = sender
        self._reader = reader

    @property
    def state(self) -> 'ApplicationState':
        return self._state

    @state.setter
    def state(self, state: 'ApplicationState') -> None:
        self._state = state

    def register(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.state.register(self)

    def login(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.state.login(self)

    def logout(self) -> None:
        self.state.logout(self)

    def create(self, name: str) -> None:
        self.name = name
        self.state.create(self)

    def join(self, name: str) -> None:
        self.name = name
        self.state.join(self)

    def leave(self) -> None:
        self.state.leave(self)

    def message(self, message: str) -> None:
        self.message = message
        self.state.message(self)

    def close(self) -> None:
        self.state.close(self)


class ApplicationState(ABC, Singleton):

    @abstractmethod
    def register(self, ctx: Application):
        pass

    @abstractmethod
    def login(self, ctx: Application):
        pass

    @abstractmethod
    def logout(self, ctx: Application):
        pass

    @abstractmethod
    def create(self, ctx: Application):
        pass

    @abstractmethod
    def join(self, ctx: Application):
        pass

    @abstractmethod
    def leave(self, ctx: Application):
        pass

    @abstractmethod
    def message(self, ctx: Application):
        pass

    @abstractmethod
    def close(self, ctx: Application):
        pass


class AbstractApplicationState(ApplicationState):
    def register(self, ctx: Application):
        self.illegal_operation()

    def login(self, ctx: Application):
        self.illegal_operation()

    def logout(self, ctx: Application):
        self.illegal_operation()

    def create(self, ctx: Application):
        self.illegal_operation()

    def join(self, ctx: Application):
        self.illegal_operation()

    def leave(self, ctx: Application):
        self.illegal_operation()

    def message(self, ctx: Application):
        self.illegal_operation()

    def close(self, ctx: Application):
        self.illegal_operation()  # TODO 'all state' has this behavior

    @staticmethod
    def illegal_operation():
        raise IllegalOperation()


class Waiting(AbstractApplicationState):
    def register(self, ctx: Application):
        pass

    def login(self, ctx: Application):
        pass


class LoggedIn(AbstractApplicationState):
    def create(self, ctx: Application):
        pass

    def join(self, ctx: Application):
        pass

    def logout(self, ctx: Application):
        pass


class Chatting(AbstractApplicationState):
    def message(self, ctx: Application):
        pass

    def leave(self, ctx: Application):
        pass
